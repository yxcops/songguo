#!/usr/bin/env python3
"""Small portable helper for the daily-reading skill.

It manages a Markdown reading root and a lightweight reading-mode state file.
It intentionally does not install platform automations by itself.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


DEFAULT_RELATIVE_DIR = "微信读书/每日读书"
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


def resolve_root(args: argparse.Namespace, require: bool = True) -> Optional[Path]:
    candidates = []

    if args.root:
        candidates.append(Path(args.root).expanduser())

    env_root = os.environ.get("DAILY_READING_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser())

    vault = os.environ.get("OBSIDIAN_VAULT_PATH")
    if vault:
        rel = os.environ.get("DAILY_READING_RELATIVE_DIR", DEFAULT_RELATIVE_DIR)
        candidates.append(Path(vault).expanduser() / rel)

    if candidates:
        return candidates[0]

    if require:
        raise SystemExit(
            "未配置读书目录。请设置 DAILY_READING_ROOT，或设置 OBSIDIAN_VAULT_PATH。"
        )
    return None


def state_path(args: argparse.Namespace, root: Optional[Path]) -> Path:
    if args.state:
        return Path(args.state).expanduser()

    env_state = os.environ.get("DAILY_READING_STATE")
    if env_state:
        return Path(env_state).expanduser()

    if root:
        return root / STATE_FILE_NAME

    return Path.home() / STATE_FILE_NAME


def ensure_root(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for name in ("读书笔记", "每周推荐书单", "附件"):
        (root / name).mkdir(parents=True, exist_ok=True)


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


def book_note_path(root: Path, book: Optional[str], timestamp: Optional[str] = None) -> Path:
    if book:
        name = f"《{sanitize_filename(book)}》.md"
    else:
        stamp = timestamp or datetime.now().strftime("%Y-%m-%d-%H%M")
        name = f"未命名读书记录-{stamp}.md"
    return root / "读书笔记" / name


def create_book_note(
    path: Path,
    *,
    book: Optional[str],
    edition: Optional[str],
    author: Optional[str],
    source: Optional[str],
) -> None:
    if path.exists():
        return

    title = f"《{book}》" if book else "未命名读书记录"
    content = f"""---
book: {quote_yaml(book)}
edition: {quote_yaml(edition)}
author: {quote_yaml(author)}
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


def cmd_check(args: argparse.Namespace) -> int:
    root = resolve_root(args, require=False)
    spath = state_path(args, root)
    print("daily-reading 检查结果")
    print(f"读书目录：{root if root else '未配置'}")
    print(f"状态文件：{spath}")
    if root:
        print(f"读书笔记目录：{root / '读书笔记'}")
        print(f"每周推荐目录：{root / '每周推荐书单'}")
    print("核心功能：读书模式、读书笔记、阅读画像、每周推荐书单")
    print("自动定时和渠道推送：需要由所在平台单独配置")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    ensure_root(root)
    profile = root / "阅读画像.md"
    if not profile.exists():
        profile.write_text(
            f"""---
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


""",
            encoding="utf-8",
        )
    print(f"已准备每日读书目录：{root}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    ensure_root(root)
    note_path = book_note_path(root, args.book)
    create_book_note(
        note_path,
        book=args.book,
        edition=args.edition,
        author=args.author,
        source=args.source,
    )
    state = {
        "active": True,
        "book": args.book,
        "edition": args.edition,
        "author": args.author,
        "source": args.source,
        "note_path": str(note_path),
        "started_at": now_iso(),
        "last_active_at": now_iso(),
    }
    save_state(state_path(args, root), state)
    if args.book:
        print(f"已进入读书模式：{args.book}")
    else:
        print("已进入读书模式。当前书名未填写，后续可补充。")
    print(f"读书笔记：{note_path}")
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    root = resolve_root(args, require=False)
    spath = state_path(args, root)
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
    root = resolve_root(args, require=False)
    spath = state_path(args, root)
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
    root = resolve_root(args, require=False)
    spath = state_path(args, root)
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
    root = resolve_root(args)
    ensure_root(root)
    spath = state_path(args, root)
    state = load_state(spath)
    book = args.book or state.get("book")
    note_path_value = state.get("note_path")
    if args.book:
        note_path = book_note_path(root, args.book)
    elif note_path_value:
        note_path = Path(note_path_value)
    else:
        note_path = book_note_path(root, None)

    create_book_note(
        note_path,
        book=book,
        edition=args.edition or state.get("edition"),
        author=args.author or state.get("author"),
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


def cmd_recommendation(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    ensure_root(root)
    week = args.week or current_iso_week()
    path = root / "每周推荐书单" / f"{week} 每周推荐书单.md"
    if not path.exists():
        path.write_text(
            f"""---
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


""",
            encoding="utf-8",
        )
    print(f"已准备每周推荐书单：{path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="daily-reading helper")
    parser.add_argument("--root", help="每日读书根目录")
    parser.add_argument("--state", help="状态文件路径")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="检查配置")
    subparsers.add_parser("init", help="创建每日读书目录结构")

    start = subparsers.add_parser("start", help="进入读书模式")
    start.add_argument("--book", help="书名")
    start.add_argument("--edition", help="版本")
    start.add_argument("--author", help="作者")
    start.add_argument("--source", help="来源")

    subparsers.add_parser("stop", help="退出读书模式")
    subparsers.add_parser("status", help="查看读书模式状态")

    expire = subparsers.add_parser("expire", help="超过指定分钟数无活动后退出")
    expire.add_argument("--minutes", type=int, default=60)

    note = subparsers.add_parser("note", help="追加读书笔记")
    note.add_argument("--book", help="书名")
    note.add_argument("--edition", help="版本")
    note.add_argument("--author", help="作者")
    note.add_argument("--source", help="来源")
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
