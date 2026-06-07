#!/usr/bin/env python3
"""Check an Obsidian shared-memory library for structure and common mistakes."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


REQUIRED = [
    "00-共享记忆库入口.md",
    "01-核心规则",
    "02-可复用经验库",
    "03-候选确认清单",
    "04-聊天摘要",
    "05-项目资料",
    "90-归档废弃",
]

OLD_NAMES = [
    "01-聊天摘要",
    "02-可复用经验",
    "03-核心规则",
    "04-项目资料",
    "05-候选记忆",
    "00-Codex（Mac mini）-总说明",
]

FIELDS = [
    "source_platform:",
    "source_device:",
    "source_type:",
    "created_at:",
    "status:",
    "applies_to:",
]

SENSITIVE_PATTERNS = [
    re.compile(r"api[_-]?key\\s*[:=]", re.I),
    re.compile(r"token\\s*[:=]", re.I),
    re.compile(r"cookie\\s*[:=]", re.I),
    re.compile(r"password\\s*[:=]", re.I),
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
]


def resolve_root(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    env_root = os.environ.get("AI_MEMORY_VAULT_PATH")
    if env_root:
        return Path(env_root).expanduser().resolve()
    obsidian = os.environ.get("OBSIDIAN_VAULT_PATH")
    if obsidian:
        return (Path(obsidian).expanduser() / "AI智能体记忆库").resolve()
    raise SystemExit("请提供 --root，或设置 AI_MEMORY_VAULT_PATH / OBSIDIAN_VAULT_PATH。")


def has_required_fields(text: str) -> bool:
    if not text.startswith("---"):
        return False
    end = text.find("---", 3)
    if end == -1:
        return False
    frontmatter = text[:end]
    return all(field in frontmatter for field in FIELDS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help="AI智能体记忆库保存路径")
    parser.add_argument("--strict", action="store_true", help="发现警告时也返回失败")
    args = parser.parse_args()

    root = resolve_root(args.root)
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        errors.append(f"缺少根目录：{root}")
    else:
        for name in REQUIRED:
            path = root / name
            if not path.exists():
                errors.append(f"缺少必需项目：{name}")

        for old in OLD_NAMES:
            if (root / old).exists():
                warnings.append(f"发现旧目录或旧文件名：{old}")

        for note in root.rglob("*.md"):
            rel = note.relative_to(root)
            text = note.read_text(encoding="utf-8", errors="replace")
            if rel.name != "00-共享记忆库入口.md" and not has_required_fields(text):
                warnings.append(f"缺少标准属性字段：{rel}")
            for pattern in SENSITIVE_PATTERNS:
                if pattern.search(text):
                    warnings.append(f"可能包含敏感信息或机器专属路径：{rel}")
                    break

    print(f"已检查：{root}")
    if errors:
        print("\n错误：")
        for item in errors:
            print(f"- {item}")
    else:
        print("\n错误：无")

    if warnings:
        print("\n警告：")
        for item in warnings:
            print(f"- {item}")
    else:
        print("\n警告：无")

    if errors or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
