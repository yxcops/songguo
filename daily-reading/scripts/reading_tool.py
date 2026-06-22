#!/usr/bin/env python3
"""Portable helper for the daily-reading skill.

It prepares a local Markdown reading workspace and records lightweight reading
mode state. It does not install platform automations.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional


DEFAULT_RELATIVE_DIR = "每日读书"
DEFAULT_PROJECT_DIR = "每日读书"
NOTES_DIR_NAME = "读书笔记"
WEEKLY_DIR_NAMES = ("每周推荐书单", "每周推荐清单")
STATE_FILE_NAME = ".daily-reading-state.json"
PROFILE_CONTEXT_FILE_NAME = "阅读画像初始化资料包.md"
PROJECT_DOC_FILE_NAMES = (
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "README.zh-CN.md",
    "项目说明.md",
    "会话迁移摘要.md",
    "问题清单.md",
    "诊断记录.md",
    "处理记录.md",
    "验证记录.md",
)
PROJECT_DOC_DIR_NAMES = ("Docs", "docs")


def now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def sanitize_filename(value: str, fallback: str = "未命名") -> str:
    clean = re.sub(r"[\\/:*?\"<>|\n\r\t]+", " ", value).strip()
    clean = re.sub(r"\s+", " ", clean)
    return clean[:90] or fallback


def quote_yaml(value: Optional[str]) -> str:
    if not value:
        return ""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def existing_weekly_dir(root: Path) -> Optional[Path]:
    for name in WEEKLY_DIR_NAMES:
        path = root / name
        if path.exists():
            return path
    return None


def has_root_signature(path: Path) -> bool:
    return (path / NOTES_DIR_NAME).is_dir() and existing_weekly_dir(path) is not None


def looks_like_notes_dir(path: Path) -> bool:
    if has_root_signature(path):
        return False
    return path.name == NOTES_DIR_NAME


def build_layout(root: Path, notes_dir: Path, mode: str) -> dict:
    weekly_dir = existing_weekly_dir(root) or (root / WEEKLY_DIR_NAMES[0])
    return {
        "mode": mode,
        "root": root,
        "notes_dir": notes_dir,
        "weekly_dir": weekly_dir,
        "profile_path": root / "阅读画像.md",
        "settings_path": root / "设置.md",
        "state_path": root / STATE_FILE_NAME,
    }


def layout_from_root(path: Path) -> dict:
    path = path.expanduser()
    if looks_like_notes_dir(path):
        return build_layout(path, path, "existing-notes-dir")
    if has_root_signature(path):
        return build_layout(path, path / NOTES_DIR_NAME, "existing-root")
    return build_layout(path, path / NOTES_DIR_NAME, "root")


def layout_from_parent(path: Path) -> dict:
    path = path.expanduser()
    if path.name == DEFAULT_PROJECT_DIR or has_root_signature(path):
        return layout_from_root(path)
    root = path / DEFAULT_PROJECT_DIR
    return build_layout(root, root / NOTES_DIR_NAME, "parent")


def layout_from_notes_dir(path: Path) -> dict:
    path = path.expanduser()
    if has_root_signature(path):
        return layout_from_root(path)
    return build_layout(path, path, "existing-notes-dir")


def resolve_layout(args: argparse.Namespace, require: bool = True) -> Optional[dict]:
    if getattr(args, "notes_dir", None):
        return layout_from_notes_dir(Path(args.notes_dir))

    env_notes = os.environ.get("DAILY_READING_NOTES_DIR")
    if env_notes:
        return layout_from_notes_dir(Path(env_notes))

    if getattr(args, "parent", None):
        return layout_from_parent(Path(args.parent))

    env_parent = os.environ.get("DAILY_READING_PARENT")
    if env_parent:
        return layout_from_parent(Path(env_parent))

    if getattr(args, "root", None):
        return layout_from_root(Path(args.root))

    env_root = os.environ.get("DAILY_READING_ROOT")
    if env_root:
        return layout_from_root(Path(env_root))

    vault = os.environ.get("OBSIDIAN_VAULT_PATH")
    if vault:
        rel = os.environ.get("DAILY_READING_RELATIVE_DIR", DEFAULT_RELATIVE_DIR)
        return layout_from_root(Path(vault).expanduser() / rel)

    if require:
        raise SystemExit(
            "还没有配置每日读书目录。请先让用户指定上级目录、每日读书根目录，或现有读书笔记目录。"
        )
    return None


def state_path(args: argparse.Namespace, layout: Optional[dict]) -> Path:
    if getattr(args, "state", None):
        return Path(args.state).expanduser()

    env_state = os.environ.get("DAILY_READING_STATE")
    if env_state:
        return Path(env_state).expanduser()

    if layout:
        return layout["state_path"]

    return Path.home() / STATE_FILE_NAME


def describe_layout(layout: dict) -> str:
    mode_labels = {
        "parent": "在上级目录下创建每日读书",
        "root": "使用指定目录作为每日读书根目录",
        "existing-root": "复用已有每日读书结构",
        "existing-notes-dir": "复用已有读书笔记目录",
    }
    lines = [
        "每日读书目录计划",
        f"模式：{mode_labels.get(layout['mode'], layout['mode'])}",
        f"根目录：{layout['root']}",
        f"读书笔记：{layout['notes_dir']}",
        f"每周推荐：{layout['weekly_dir']}",
        f"阅读画像：{layout['profile_path']}",
        f"设置文件：{layout['settings_path']}",
    ]
    lines.append("")
    lines.append("将处理的内容：")
    seen_paths = set()
    for key in ("root", "notes_dir", "weekly_dir"):
        path = layout[key]
        if path in seen_paths:
            continue
        seen_paths.add(path)
        action = "复用" if path.exists() else "创建"
        lines.append(f"- {action}：{path}")
    for key in ("profile_path", "settings_path"):
        path = layout[key]
        if path in seen_paths:
            continue
        seen_paths.add(path)
        action = "保留" if path.exists() else "创建"
        lines.append(f"- {action}：{path}")
    lines.append("")
    lines.append("不会移动、改名或整理已有文件。")
    return "\n".join(lines)


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    return parts[2].lstrip()


def compact_markdown_with_status(text: str, max_chars: int) -> tuple[str, bool]:
    text = strip_frontmatter(text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if max_chars <= 0:
        return text, False
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars].rstrip() + "\n\n...（已截断）", True


def compact_markdown(text: str, max_chars: int) -> str:
    return compact_markdown_with_status(text, max_chars)[0]


def safe_read_markdown(path: Path, max_chars: int) -> str:
    try:
        return compact_markdown(path.read_text(encoding="utf-8"), max_chars)
    except UnicodeDecodeError:
        return "无法按 UTF-8 读取，已跳过正文。"
    except OSError as exc:
        return f"读取失败：{exc}"


def safe_read_markdown_with_status(path: Path, max_chars: int) -> tuple[str, bool]:
    try:
        return compact_markdown_with_status(path.read_text(encoding="utf-8"), max_chars)
    except UnicodeDecodeError:
        return "无法按 UTF-8 读取，已跳过正文。", False
    except OSError as exc:
        return f"读取失败：{exc}", False


def recent_markdown_files(path: Path, *, days: int, max_files: int) -> list[Path]:
    if not path.exists():
        return []
    cutoff = datetime.now().timestamp() - timedelta(days=days).total_seconds()
    files = []
    for item in path.rglob("*.md"):
        if item.name.startswith("."):
            continue
        try:
            stat = item.stat()
        except OSError:
            continue
        if stat.st_mtime >= cutoff:
            files.append((stat.st_mtime, item))
    files.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in files[:max_files]]


def file_mtime_iso(path: Path) -> str:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).astimezone().replace(microsecond=0).isoformat()
    except OSError:
        return "未知"


def render_file_excerpt(
    path: Path,
    *,
    title: str,
    max_chars: int,
    truncated_files: list[str] | None = None,
) -> str:
    body, was_truncated = safe_read_markdown_with_status(path, max_chars)
    if was_truncated and truncated_files is not None:
        truncated_files.append(f"{title}（上限 {max_chars} 字）")
    return "\n".join(
        [
            f"### {title}",
            f"- 路径：{path}",
            f"- 更新时间：{file_mtime_iso(path)}",
            "",
            body,
        ]
    )


def is_hidden_path(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts if part not in (".", ".."))


def unique_paths(paths: list[Path]) -> list[Path]:
    result = []
    seen = set()
    for path in paths:
        resolved = path.expanduser()
        try:
            stat = resolved.stat()
            key = (stat.st_dev, stat.st_ino)
        except OSError:
            key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        result.append(resolved)
    return result


def project_context_files(project_dir: Path, *, max_files: int) -> tuple[list[Path], list[str]]:
    project_dir = project_dir.expanduser()
    warnings = []
    if not project_dir.exists():
        return [], [f"{project_dir} 不存在，已跳过。"]
    if not project_dir.is_dir():
        return [], [f"{project_dir} 不是目录，已跳过。"]

    candidates = []
    for name in PROJECT_DOC_FILE_NAMES:
        path = project_dir / name
        if path.is_file():
            candidates.append(path)

    for dir_name in PROJECT_DOC_DIR_NAMES:
        docs_dir = project_dir / dir_name
        if not docs_dir.is_dir():
            continue
        for item in sorted(docs_dir.rglob("*.md")):
            if item.is_file() and not is_hidden_path(item.relative_to(project_dir)):
                candidates.append(item)

    files = unique_paths(candidates)
    if len(files) > max_files:
        warnings.append(f"{project_dir} 匹配到 {len(files)} 个项目文档，只读取前 {max_files} 个。")
        files = files[:max_files]
    if not files:
        warnings.append(f"{project_dir} 未找到常见项目说明文件或 Docs/*.md。")
    return files, warnings


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_state(path: Path, state: dict) -> None:
    atomic_write_text(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def settings_content(layout: dict) -> str:
    return f"""---
created_at: {quote_yaml(now_iso())}
updated_at: {quote_yaml(now_iso())}
status: active
---

# 设置

## 目录

- 根目录：{layout['root']}
- 读书笔记：{layout['notes_dir']}
- 每周推荐：{layout['weekly_dir']}
- 阅读画像：{layout['profile_path']}

## 状态

- 阅读画像初始化：未完成
- 每周自动推荐：未配置
- 渠道提醒：未配置
- 发送渠道：
- 发送目标：
- 读取日记或历史记录：未授权
- 读取共享记忆或项目摘要：未授权

## 自动任务

- 运行时间：每周一 06:00（未确认）
- 推荐数量：5
- 输出目录：每周推荐书单
- 发送内容：书单摘要和文件位置

## 授权记忆来源

<!-- 只记录用户明确授权的文件路径或摘要来源，不要默认写入私人目录。 -->

## 项目资料来源

<!-- 只记录用户明确授权的项目目录或项目摘要文件。 -->

## 说明

这个文件记录每日读书 Skill 的本地目录设置。自动定时、渠道发送、读取日记或历史记录，需要在所在平台单独配置并经过用户确认。
"""


def profile_content() -> str:
    return f"""---
created_at: {quote_yaml(now_iso())}
updated_at: {quote_yaml(now_iso())}
status: active
---

# 阅读画像

## 来源与边界

- 初始化状态：未初始化
- 最近更新时间：
- 已读取来源：
- 未读取或未授权来源：
- 可信度：

## 稳定画像

长期有效，除非多次证据推翻。

## 用户现在在做什么


## 阶段画像

最近 4-8 周有效。

## 近期关注的问题


## 反复出现的困难


## 正在补的能力


## 临时信号

最近 1-2 周出现，暂不写成稳定结论。

## 更适合的书籍类型


## 暂时不适合继续堆的书


## 下一阶段推荐策略


## 优先推荐方向


## 暂不推荐方向


## 本周变化


## 画像变更记录

| 日期 | 变更 | 依据 | 可信度 |
|---|---|---|---|

"""


def ensure_layout(layout: dict) -> None:
    layout["root"].mkdir(parents=True, exist_ok=True)
    layout["notes_dir"].mkdir(parents=True, exist_ok=True)
    layout["weekly_dir"].mkdir(parents=True, exist_ok=True)

    if not layout["profile_path"].exists():
        atomic_write_text(layout["profile_path"], profile_content())

    if not layout["settings_path"].exists():
        atomic_write_text(layout["settings_path"], settings_content(layout))


def book_note_path(layout: dict, book: Optional[str], timestamp: Optional[str] = None) -> Path:
    if book:
        name = f"《{sanitize_filename(book)}》.md"
    else:
        stamp = timestamp or datetime.now().strftime("%Y-%m-%d-%H%M")
        name = f"未命名读书记录-{stamp}.md"
    return layout["notes_dir"] / name


def create_book_note(
    path: Path,
    *,
    book: Optional[str],
    edition: Optional[str],
    author: Optional[str],
    translator: Optional[str],
    publisher: Optional[str],
    published_at: Optional[str],
    source: Optional[str],
) -> None:
    if path.exists():
        return

    title = f"《{book}》" if book else "未命名读书记录"
    content = f"""---
book: {quote_yaml(book)}
edition: {quote_yaml(edition)}
author: {quote_yaml(author)}
translator: {quote_yaml(translator)}
publisher: {quote_yaml(publisher)}
published_at: {quote_yaml(published_at)}
source: {quote_yaml(source or "daily-reading")}
status: reading
created_at: {quote_yaml(now_iso())}
updated_at: {quote_yaml(now_iso())}
---

# {title}

## 基本信息

| 项目 | 内容 |
|---|---|
| 作者 | {author or ""} |
| 版本 | {edition or ""} |
| 译者 | {translator or ""} |
| 出版社 | {publisher or ""} |
| 出版日期 | {published_at or ""} |
| 来源 | {source or ""} |
| 推荐来源 | {source or ""} |
| 本书解决的问题 |  |
| 版本可信度 |  |

## 一句话判断


## 我为什么读这本书

- 当前问题：
- 期待解决：
- 不期待解决：

## 主要内容


## 对我的用处


## 阅读记录


## 可执行行动


## 反对意见

我不同意、怀疑或需要验证的地方：

## 复读索引

未来什么情况下值得重看：

## 待确认

"""
    atomic_write_text(path, content)


def touch_updated_at(path: Path) -> None:
    text = read_text_if_exists(path)
    if not text.startswith("---"):
        return
    parts = text.split("---", 2)
    if len(parts) < 3:
        return
    frontmatter = parts[1]
    lines = frontmatter.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith("updated_at:"):
            lines[index] = f"updated_at: {quote_yaml(now_iso())}"
            replaced = True
            break
    if not replaced:
        lines.append(f"updated_at: {quote_yaml(now_iso())}")
    new_text = "---" + "\n".join(lines) + "\n---" + parts[2]
    atomic_write_text(path, new_text)


def append_note(path: Path, *, kind: str, section: Optional[str], text: str) -> None:
    labels = {
        "excerpt": "摘录",
        "thought": "想法",
        "question": "问题",
        "summary": "讨论结论",
        "action": "行动",
    }
    label = labels.get(kind, kind)
    section_line = f"\n关联位置：{section}\n" if section else ""
    block = f"\n### {now_iso()}｜{label}\n{section_line}\n{text.strip()}\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(block)
    touch_updated_at(path)


def cmd_check(args: argparse.Namespace) -> int:
    layout = resolve_layout(args, require=False)
    spath = state_path(args, layout)
    print("daily-reading 检查结果")
    if not layout:
        print("每日读书目录：未配置")
        print("首次使用时，应先让用户指定上级目录、每日读书根目录，或现有读书笔记目录。")
    else:
        print(describe_layout(layout))
    print(f"状态文件：{spath}")
    print("核心功能：读书模式、读书笔记、阅读画像、每周推荐书单")
    print("阅读画像初始化：可用 profile-context 命令基于授权记忆和项目文档生成资料包")
    print("推荐上下文包：可用 context 命令基于阅读画像、近期笔记、历史书单和授权记忆生成")
    print("自动定时和渠道推送：需要由所在平台单独配置")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    print(describe_layout(layout))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    ensure_layout(layout)
    print("已准备每日读书目录。")
    print(describe_layout(layout))
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    ensure_layout(layout)
    note_path = book_note_path(layout, args.book)
    create_book_note(
        note_path,
        book=args.book,
        edition=args.edition,
        author=args.author,
        translator=args.translator,
        publisher=args.publisher,
        published_at=args.published_at,
        source=args.source,
    )
    state = {
        "active": True,
        "book": args.book,
        "edition": args.edition,
        "author": args.author,
        "translator": args.translator,
        "publisher": args.publisher,
        "published_at": args.published_at,
        "source": args.source,
        "note_path": str(note_path),
        "root": str(layout["root"]),
        "notes_dir": str(layout["notes_dir"]),
        "weekly_dir": str(layout["weekly_dir"]),
        "started_at": now_iso(),
        "last_active_at": now_iso(),
    }
    save_state(state_path(args, layout), state)
    if args.book:
        print(f"已进入读书模式：{args.book}")
    else:
        print("已进入读书模式。当前书名未填写，后续可补充。")
    print(f"读书笔记：{note_path}")
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    layout = resolve_layout(args, require=False)
    spath = state_path(args, layout)
    state = load_state(spath)
    if not state.get("active"):
        print("当前没有活动中的读书模式。")
        return 0
    state["active"] = False
    state["ended_at"] = now_iso()
    state["last_active_at"] = now_iso()
    save_state(spath, state)
    print("已退出读书模式。")
    if state.get("note_path"):
        print(f"读书笔记：{state['note_path']}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    layout = resolve_layout(args, require=False)
    spath = state_path(args, layout)
    state = load_state(spath)
    if not state:
        print("还没有读书模式状态。")
        return 0
    status = "进行中" if state.get("active") else "已结束"
    print(f"读书模式：{status}")
    print(f"书名：{state.get('book') or '未填写'}")
    print(f"版本：{state.get('edition') or '未填写'}")
    print(f"作者：{state.get('author') or '未填写'}")
    print(f"最近活动：{state.get('last_active_at') or '未知'}")
    if state.get("note_path"):
        print(f"读书笔记：{state['note_path']}")
    return 0


def cmd_expire(args: argparse.Namespace) -> int:
    layout = resolve_layout(args, require=False)
    spath = state_path(args, layout)
    state = load_state(spath)
    if not state.get("active"):
        print("当前没有需要自动退出的读书模式。")
        return 0

    last_active = parse_iso(state.get("last_active_at")) or parse_iso(state.get("started_at"))
    if not last_active:
        print("状态文件缺少有效时间，未自动退出。")
        return 0

    elapsed = (datetime.now().astimezone() - last_active).total_seconds() / 60
    if elapsed >= args.minutes:
        state["active"] = False
        state["ended_at"] = now_iso()
        state["expire_reason"] = f"inactive_for_{int(elapsed)}_minutes"
        save_state(spath, state)
        print(f"已因 {int(elapsed)} 分钟无活动自动退出读书模式。")
    else:
        print(f"仍在读书模式中，距离自动退出还差约 {int(args.minutes - elapsed)} 分钟。")
    return 0


def read_note_text(args: argparse.Namespace) -> str:
    if args.stdin:
        text = sys.stdin.read()
    else:
        text = args.text or ""
    if not text.strip():
        raise SystemExit("没有收到要写入的笔记内容。请传入 --text，或使用 --stdin。")
    return text


def cmd_note(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    ensure_layout(layout)
    spath = state_path(args, layout)
    state = load_state(spath)
    book = args.book or state.get("book")
    note_path_value = state.get("note_path")
    if args.book:
        note_path = book_note_path(layout, args.book)
    elif note_path_value:
        note_path = Path(note_path_value)
    else:
        note_path = book_note_path(layout, None)

    create_book_note(
        note_path,
        book=book,
        edition=args.edition or state.get("edition"),
        author=args.author or state.get("author"),
        translator=args.translator or state.get("translator"),
        publisher=args.publisher or state.get("publisher"),
        published_at=args.published_at or state.get("published_at"),
        source=args.source or state.get("source"),
    )
    append_note(note_path, kind=args.kind, section=args.section, text=read_note_text(args))

    if state.get("active"):
        state["last_active_at"] = now_iso()
        if args.book:
            state["book"] = args.book
            state["note_path"] = str(note_path)
        save_state(spath, state)

    print(f"已写入读书笔记：{note_path}")
    return 0


def week_start_for(day: date) -> date:
    return day - timedelta(days=day.weekday())


def format_chinese_date(day: date, *, include_year: bool) -> str:
    if include_year:
        return f"{day.year}年{day.month}月{day.day}日"
    return f"{day.month}月{day.day}日"


def format_week_period(start_date: date) -> str:
    end_date = start_date + timedelta(days=6)
    return (
        f"{format_chinese_date(start_date, include_year=True)}~"
        f"{format_chinese_date(end_date, include_year=end_date.year != start_date.year)}"
    )


def parse_week_start(value: Optional[str]) -> date:
    if not value:
        return week_start_for(datetime.now().date())

    text = value.strip()
    iso_week = re.fullmatch(r"(\d{4})-W(\d{1,2})", text)
    if iso_week:
        year = int(iso_week.group(1))
        week = int(iso_week.group(2))
        try:
            return date.fromisocalendar(year, week, 1)
        except ValueError as exc:
            raise SystemExit(f"无法识别周参数：{value}") from exc

    try:
        return week_start_for(datetime.strptime(text, "%Y-%m-%d").date())
    except ValueError as exc:
        raise SystemExit("无法识别日期。请使用 --start-date 2026-06-22，或兼容旧参数 --week 2026-W26。") from exc


def weekly_template(period: str, start_date: date, end_date: date) -> str:
    return f"""---
period: {quote_yaml(period)}
start_date: {quote_yaml(start_date.isoformat())}
end_date: {quote_yaml(end_date.isoformat())}
created_at: {quote_yaml(now_iso())}
status: draft
---

# {period} 每周推荐书单

## 本周判断依据

- 阅读画像：
- 近期读书笔记：
- 历史推荐书单：
- 历史推荐反馈：
- 额外授权记忆：
- 未读取或未授权来源：
- 是否出现上下文截断：
- 本周推荐策略：

## 历史推荐反馈

- 已推荐但未读：
- 已推荐且已开始：
- 已推荐且读完：
- 明确不感兴趣：
- 暂缓原因：

## 本周去重和冷却

- 过去 8 周已推荐过的书：
- 本周避免重复的主题：
- 本周最多推荐 1 本重型理论书：
- 本周至少推荐 1 本短平快可执行书：

## 本周配比

- 主线能力书：
- 当前项目工具书：
- 判断力/管理/商业书：
- 轻量补充书：
- 储备书：

## 推荐书

### 1. 《书名》

- 作者：
- 原书名：
- 译者或版本说明：
- 推荐版本：
- 出版社：
- 出版日期：
- 事实核验状态：
- 核验来源：
- 未核验原因：
- 质量依据：
- 质量风险：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 2. 《书名》

- 作者：
- 原书名：
- 译者或版本说明：
- 推荐版本：
- 出版社：
- 出版日期：
- 事实核验状态：
- 核验来源：
- 未核验原因：
- 质量依据：
- 质量风险：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 3. 《书名》

- 作者：
- 原书名：
- 译者或版本说明：
- 推荐版本：
- 出版社：
- 出版日期：
- 事实核验状态：
- 核验来源：
- 未核验原因：
- 质量依据：
- 质量风险：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 4. 《书名》

- 作者：
- 原书名：
- 译者或版本说明：
- 推荐版本：
- 出版社：
- 出版日期：
- 事实核验状态：
- 核验来源：
- 未核验原因：
- 质量依据：
- 质量风险：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 5. 《书名》

- 作者：
- 原书名：
- 译者或版本说明：
- 推荐版本：
- 出版社：
- 出版日期：
- 事实核验状态：
- 核验来源：
- 未核验原因：
- 质量依据：
- 质量风险：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

## 本周读法

- 本周最应该先读：
- 如果只有 30 分钟：
- 读完后应该产出：

## 发送记录

- 是否已发送：
- 发送渠道：
- 发送时间：
- 发送摘要：

"""


def cmd_recommendation(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    ensure_layout(layout)
    start_date = parse_week_start(args.start_date or args.week)
    end_date = start_date + timedelta(days=6)
    period = format_week_period(start_date)
    path = layout["weekly_dir"] / f"{period} 每周推荐书单.md"
    if not path.exists():
        atomic_write_text(path, weekly_template(period, start_date, end_date))
    print(f"已准备每周推荐书单草稿：{path}")
    print("注意：这里只创建草稿；还需要 Agent 读取上下文包后填入 5 本具体推荐书。")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    profile_path = layout["profile_path"]
    settings_path = layout["settings_path"]
    notes = recent_markdown_files(layout["notes_dir"], days=args.days, max_files=args.max_notes)
    weekly = recent_markdown_files(layout["weekly_dir"], days=args.days, max_files=args.max_weekly)
    truncated_files: list[str] = []

    lines = [
        "# 每周推荐上下文包",
        "",
        f"- 生成时间：{now_iso()}",
        f"- 读取天数：最近 {args.days} 天",
        f"- 根目录：{layout['root']}",
        f"- 读书笔记目录：{layout['notes_dir']}",
        f"- 每周推荐目录：{layout['weekly_dir']}",
        "",
        "## 读取范围",
        "",
        "- 默认读取：阅读画像、设置文件、近期读书笔记、近期每周推荐书单。",
        "- 阅读画像默认完整读取；如需限制，可设置 `--profile-max-chars`。",
        "- 额外记忆：只读取通过 `--extra-source` 明确传入的文件。",
        "- 未授权内容：日记、聊天历史、私人目录、微信读书数据等不会自动读取。",
        "",
    ]

    if settings_path.exists():
        lines.extend(
            [
                "## 设置摘要",
                "",
                render_file_excerpt(
                    settings_path,
                    title=settings_path.name,
                    max_chars=args.max_chars,
                    truncated_files=truncated_files,
                ),
                "",
            ]
        )

    if profile_path.exists():
        lines.extend(
            [
                "## 阅读画像",
                "",
                render_file_excerpt(
                    profile_path,
                    title=profile_path.name,
                    max_chars=args.profile_max_chars,
                    truncated_files=truncated_files,
                ),
                "",
            ]
        )
    else:
        lines.extend(["## 阅读画像", "", "未找到阅读画像。", ""])

    lines.extend(["## 近期读书笔记", ""])
    if notes:
        for path in notes:
            lines.append(
                render_file_excerpt(
                    path,
                    title=path.name,
                    max_chars=args.max_chars,
                    truncated_files=truncated_files,
                )
            )
            lines.append("")
    else:
        lines.extend(["最近范围内没有读书笔记。", ""])

    lines.extend(["## 近期推荐书单", ""])
    if weekly:
        for path in weekly:
            lines.append(
                render_file_excerpt(
                    path,
                    title=path.name,
                    max_chars=args.max_chars,
                    truncated_files=truncated_files,
                )
            )
            lines.append("")
    else:
        lines.extend(["最近范围内没有历史推荐书单。", ""])

    lines.extend(["## 额外授权记忆", ""])
    if args.extra_source:
        for value in args.extra_source:
            path = Path(value).expanduser()
            if path.is_dir():
                lines.extend(
                    [
                        f"### {path}",
                        "这是目录，不是明确文件。为避免越界读取，已跳过；请改传具体 Markdown 文件。",
                        "",
                    ]
                )
                continue
            if not path.exists():
                lines.extend([f"### {path}", "文件不存在，已跳过。", ""])
                continue
            lines.append(
                render_file_excerpt(
                    path,
                    title=path.name,
                    max_chars=args.max_chars,
                    truncated_files=truncated_files,
                )
            )
            lines.append("")
    else:
        lines.extend(["未提供额外授权记忆文件。", ""])

    lines.extend(["## 截断提醒", ""])
    if truncated_files:
        lines.append("以下文件因为字符上限被截断：")
        lines.extend(f"- {item}" for item in truncated_files)
        lines.append("")
        lines.append("正式推荐前先确认截断是否影响判断；如果阅读画像被截断，必须重新生成更完整的上下文包。")
    else:
        lines.append("未发现上下文文件被脚本截断。")
    lines.append("")

    lines.extend(
        [
            "## 生成书单时必须遵守",
            "",
            "- 固定推荐 5 本书。",
            "- 在“本周判断依据”里列出读取范围和未授权来源。",
            "- 如果当前平台能联网或能查资料，推荐前必须核对作者、原书名、译者或版本、出版社、出版日期和当前可获得性。",
            "- 每本书必须写核验来源；无法核验时写清未核验原因，不确定的作者、版本、译本、出版社、出版日期和可获得性写“不确定，需核验”。",
            "- 每本书必须写质量依据，可参考豆瓣、Goodreads、出版社页、图书馆目录、课程书单、可靠书评、奖项、引用情况或长期读者口碑。",
            "- 评分不能作为唯一理由；样本少、版本混乱、争议大或口碑分裂时，写入质量风险。",
            "- 未完成事实核验或质量判断的书，不能作为本周最优先阅读项。",
            "- 推荐理由要连接用户近期问题、阅读画像或读书笔记，不要只写泛泛好书。",
            "- 过去 8 周已推荐过的书，除非用户明确要求，不重复推荐。",
            "- 同一主题每周最多推荐 2 本；每周至少 1 本短平快可执行书，最多 1 本重型理论书。",
            "- 写清本周最应该先读哪一本，以及只有 30 分钟时该读哪里。",
            "- 如果没有配置发送渠道，只写入文件，不声称已发送。",
        ]
    )

    output = "\n".join(lines).rstrip() + "\n"
    if args.output:
        out_path = Path(args.output).expanduser()
        atomic_write_text(out_path, output)
        print(f"已写入推荐上下文包：{out_path}")
    else:
        print(output, end="")
    return 0


def cmd_profile_context(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    ensure_layout(layout)
    profile_path = layout["profile_path"]
    settings_path = layout["settings_path"]

    lines = [
        "# 阅读画像初始化资料包",
        "",
        f"- 生成时间：{now_iso()}",
        f"- 根目录：{layout['root']}",
        f"- 阅读画像：{profile_path}",
        "",
        "## 使用方式",
        "",
        "`profile-context` 只生成资料包，不等于已经完成阅读画像初始化。",
        "把下面资料归纳进 `阅读画像.md`，用于以后每周推荐书单。",
        "只保留稳定偏好、当前项目方向、反复出现的问题和需要补的能力。",
        "不要把原始聊天、私密配置、账号、Token、Cookie、代理细节写入阅读画像。",
        "写入后还要在 `设置.md` 记录阅读画像初始化状态和已授权来源。",
        "",
        "## 读取范围",
        "",
        "- 默认读取：设置文件、现有阅读画像。",
        "- 授权记忆：只读取通过 `--source` 明确传入的文件。",
        "- 授权项目：只读取通过 `--project-dir` 指定目录下的常见说明文件和 Docs/*.md。",
        "- 未授权内容：不会自动读取日记、聊天历史、私人目录、微信读书、NAS 或整个平台历史。",
        "",
    ]

    if settings_path.exists():
        lines.extend(
            [
                "## 设置摘要",
                "",
                render_file_excerpt(settings_path, title=settings_path.name, max_chars=args.max_chars),
                "",
            ]
        )

    if profile_path.exists():
        lines.extend(
            [
                "## 现有阅读画像",
                "",
                render_file_excerpt(profile_path, title=profile_path.name, max_chars=args.max_chars),
                "",
            ]
        )

    lines.extend(["## 授权项目文件", ""])
    if args.project_dir:
        for value in args.project_dir:
            project_dir = Path(value).expanduser()
            files, warnings = project_context_files(project_dir, max_files=args.max_project_files)
            lines.extend([f"### 项目：{project_dir}", ""])
            for warning in warnings:
                lines.append(f"- {warning}")
            if warnings:
                lines.append("")
            for path in files:
                lines.append(render_file_excerpt(path, title=path.name, max_chars=args.max_chars))
                lines.append("")
    else:
        lines.extend(["未提供项目目录。", ""])

    lines.extend(["## 授权记忆和历史摘要", ""])
    if args.source:
        for value in args.source:
            path = Path(value).expanduser()
            if path.is_dir():
                lines.extend(
                    [
                        f"### {path}",
                        "这是目录，不是明确文件。为避免越界读取，已跳过；请改传具体文件。",
                        "",
                    ]
                )
                continue
            if not path.exists():
                lines.extend([f"### {path}", "文件不存在，已跳过。", ""])
                continue
            lines.append(render_file_excerpt(path, title=path.name, max_chars=args.max_chars))
            lines.append("")
    else:
        lines.extend(["未提供授权记忆或历史摘要文件。", ""])

    lines.extend(
        [
            "## 写入阅读画像时必须形成的结论",
            "",
            "- 用户现在在做什么。",
            "- 稳定画像：长期有效，除非多次证据推翻。",
            "- 阶段画像：最近 4-8 周有效。",
            "- 临时信号：最近 1-2 周出现，暂不写成稳定结论。",
            "- 近期反复关注的问题。",
            "- 正在补的能力。",
            "- 更适合的书籍类型。",
            "- 暂时不适合继续堆的书。",
            "- 下一阶段推荐策略。",
            "- 优先推荐方向。",
            "- 暂不推荐方向。",
            "- 画像变更记录。",
            "- 已读取来源、未读取来源和可信度。",
            "",
            "## 后续每周推荐规则",
            "",
            "- 每周推荐优先读取更新后的 `阅读画像.md`，而不是反复读取原始历史。",
            "- 只有用户再次明确授权时，才补读新的项目资料或平台记忆。",
            "- 推荐书单里要写清楚依据来自阅读画像、读书笔记、历史书单还是额外授权记忆。",
        ]
    )

    output = "\n".join(lines).rstrip() + "\n"
    if args.output and args.save:
        raise SystemExit("请在 --output 和 --save 中选择一个，不要同时使用。")
    if args.output:
        out_path = Path(args.output).expanduser()
    elif args.save:
        out_path = layout["root"] / PROFILE_CONTEXT_FILE_NAME
    else:
        out_path = None

    if out_path:
        atomic_write_text(out_path, output)
        print(f"已写入阅读画像初始化资料包：{out_path}")
        print("注意：这里只生成资料包；还需要 Agent 归纳后写入阅读画像并更新设置文件。")
    else:
        print(output, end="")
    return 0


def add_location_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", help="每日读书根目录；如果已有读书笔记和每周推荐目录，会直接复用")
    parser.add_argument("--parent", help="上级目录；会在下面创建或复用“每日读书”目录")
    parser.add_argument("--notes-dir", help="现有读书笔记目录；不会再嵌套新的“读书笔记”")
    parser.add_argument("--state", help="状态文件路径")


def add_book_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--book", help="书名")
    parser.add_argument("--edition", help="版本")
    parser.add_argument("--author", help="作者")
    parser.add_argument("--translator", help="译者")
    parser.add_argument("--publisher", help="出版社")
    parser.add_argument("--published-at", help="出版日期")
    parser.add_argument("--source", help="来源")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="daily-reading helper")
    add_location_args(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="检查配置")
    subparsers.add_parser("plan", help="只预览将创建或复用的目录，不写入文件")
    subparsers.add_parser("init", help="创建或补齐每日读书目录结构")

    start = subparsers.add_parser("start", help="进入读书模式")
    add_book_args(start)

    subparsers.add_parser("stop", help="退出读书模式")
    subparsers.add_parser("status", help="查看读书模式状态")

    expire = subparsers.add_parser("expire", help="超过指定分钟数无活动后退出")
    expire.add_argument("--minutes", type=int, default=60)

    note = subparsers.add_parser("note", help="追加读书笔记")
    add_book_args(note)
    note.add_argument("--section", help="章节或关联位置")
    note.add_argument(
        "--kind",
        choices=("excerpt", "thought", "question", "summary", "action"),
        default="thought",
    )
    note.add_argument("--text", help="笔记内容")
    note.add_argument("--stdin", action="store_true", help="从标准输入读取笔记内容")

    recommendation_draft = subparsers.add_parser("recommendation-draft", help="创建每周推荐书单草稿")
    recommendation_draft.add_argument("--start-date", help="自然周内任一天，例如 2026-06-22；输出为周一到周日日期范围")
    recommendation_draft.add_argument("--week", help="兼容旧参数：ISO 周，例如 2026-W25；输出仍使用周一到周日日期范围")

    recommendation = subparsers.add_parser("recommendation", help="兼容旧命令：创建每周推荐书单草稿")
    recommendation.add_argument("--start-date", help="自然周内任一天，例如 2026-06-22；输出为周一到周日日期范围")
    recommendation.add_argument("--week", help="兼容旧参数：ISO 周，例如 2026-W25；输出仍使用周一到周日日期范围")

    context = subparsers.add_parser("context", help="生成每周推荐用的上下文包")
    context.add_argument("--days", type=int, default=45, help="读取最近多少天的读书笔记和历史书单")
    context.add_argument("--max-notes", type=int, default=12, help="最多读取多少篇近期读书笔记")
    context.add_argument("--max-weekly", type=int, default=4, help="最多读取多少篇近期历史书单")
    context.add_argument("--max-chars", type=int, default=1800, help="每个文件最多摘取多少字符")
    context.add_argument(
        "--profile-max-chars",
        type=int,
        default=0,
        help="阅读画像最多摘取多少字符；0 表示不截断",
    )
    context.add_argument(
        "--extra-source",
        action="append",
        help="用户明确授权的额外记忆 Markdown 文件，可重复传入；不要传整个私人目录",
    )
    context.add_argument("--output", help="把上下文包写入指定文件；不传则输出到终端")

    profile_context = subparsers.add_parser("profile-context", help="生成阅读画像初始化资料包")
    profile_context.add_argument(
        "--project-dir",
        action="append",
        help="用户授权读取的项目目录，可重复传入；只读取常见说明文件和 Docs/*.md",
    )
    profile_context.add_argument(
        "--source",
        action="append",
        help="用户明确授权的记忆、历史摘要或平台资料文件，可重复传入；不要传整个私人目录",
    )
    profile_context.add_argument("--max-project-files", type=int, default=16, help="每个项目最多读取多少个文档")
    profile_context.add_argument("--max-chars", type=int, default=2200, help="每个文件最多摘取多少字符")
    profile_context.add_argument("--output", help="把资料包写入指定文件；不传则输出到终端")
    profile_context.add_argument(
        "--save",
        action="store_true",
        help=f"写入每日读书根目录下的 {PROFILE_CONTEXT_FILE_NAME}",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    commands = {
        "check": cmd_check,
        "plan": cmd_plan,
        "init": cmd_init,
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "expire": cmd_expire,
        "note": cmd_note,
        "recommendation-draft": cmd_recommendation,
        "recommendation": cmd_recommendation,
        "context": cmd_context,
        "profile-context": cmd_profile_context,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
