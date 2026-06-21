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
from datetime import datetime
from pathlib import Path
from typing import Optional


DEFAULT_RELATIVE_DIR = "每日读书"
DEFAULT_PROJECT_DIR = "每日读书"
NOTES_DIR_NAME = "读书笔记"
WEEKLY_DIR_NAMES = ("每周推荐书单", "每周推荐清单")
STATE_FILE_NAME = ".daily-reading-state.json"


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


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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

- 每周自动推荐：未配置
- 渠道提醒：未配置
- 读取日记或历史记录：未授权

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

## 近期关注的问题


## 正在补的能力


## 更适合的书籍类型


## 暂时不适合继续堆的书


## 下一阶段阅读建议


## 本周变化

"""


def ensure_layout(layout: dict) -> None:
    layout["root"].mkdir(parents=True, exist_ok=True)
    layout["notes_dir"].mkdir(parents=True, exist_ok=True)
    layout["weekly_dir"].mkdir(parents=True, exist_ok=True)

    if not layout["profile_path"].exists():
        layout["profile_path"].write_text(profile_content(), encoding="utf-8")

    if not layout["settings_path"].exists():
        layout["settings_path"].write_text(settings_content(layout), encoding="utf-8")


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

## 一句话判断


## 主要内容


## 对我的用处


## 阅读记录


## 可执行行动


## 待确认

"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
    path.write_text(new_text, encoding="utf-8")


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


def current_iso_week() -> str:
    today = datetime.now().date()
    year, week, _ = today.isocalendar()
    return f"{year}-W{week:02d}"


def weekly_template(week: str) -> str:
    return f"""---
week: {quote_yaml(week)}
created_at: {quote_yaml(now_iso())}
status: draft
---

# {week} 每周推荐书单

## 本周判断依据


## 推荐书

### 1. 《书名》

- 作者：
- 推荐版本：
- 出版社：
- 出版日期：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 2. 《书名》

- 作者：
- 推荐版本：
- 出版社：
- 出版日期：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 3. 《书名》

- 作者：
- 推荐版本：
- 出版社：
- 出版日期：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 4. 《书名》

- 作者：
- 推荐版本：
- 出版社：
- 出版日期：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

### 5. 《书名》

- 作者：
- 推荐版本：
- 出版社：
- 出版日期：
- 为什么推荐：
- 适合解决的问题：
- 推荐读法：
- 优先级：

## 本周读法

"""


def cmd_recommendation(args: argparse.Namespace) -> int:
    layout = resolve_layout(args)
    ensure_layout(layout)
    week = args.week or current_iso_week()
    path = layout["weekly_dir"] / f"{week} 每周推荐书单.md"
    if not path.exists():
        path.write_text(weekly_template(week), encoding="utf-8")
    print(f"已准备每周推荐书单：{path}")
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

    recommendation = subparsers.add_parser("recommendation", help="创建每周推荐书单草稿")
    recommendation.add_argument("--week", help="ISO 周，例如 2026-W25")

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
        "recommendation": cmd_recommendation,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
