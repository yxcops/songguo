#!/usr/bin/env python3
"""Initialize an Obsidian shared-memory library without overwriting notes."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from datetime import datetime


DIRS = [
    "01-核心规则",
    "02-可复用经验库",
    "03-候选确认清单",
    "04-聊天摘要",
    "05-项目资料",
    "90-归档废弃",
]


ENTRY = """---
source_platform: User
source_device: Unknown
source_type: 入口说明
created_at: {created_at}
status: 已确认
applies_to:
  - Codex
  - Hermes
  - Claude Code
  - Obsidian
---

# AI智能体共享记忆库入口

这个库用于让多个 AI 智能体共享长期经验和规则。

## 目录

- `01-核心规则`: 长期稳定规则，不能自动修改。
- `02-可复用经验库`: 已确认的可复用经验。
- `03-候选确认清单`: 待确认的新经验和规则建议。
- `04-聊天摘要`: 有价值对话的简短摘要。
- `05-项目资料`: 跨智能体可用的项目背景、模板和索引。
- `90-归档废弃`: 过期、重复、废弃内容。

## 基本原则

简单任务不用查库。复杂任务、长期项目、本机环境、配置修改、自动化、历史规则相关任务应先查库。

新内容先写入 `04-聊天摘要` 或 `03-候选确认清单`。

不能自动修改 `01-核心规则` 或 `02-可复用经验库`。

Codex、Hermes、Claude Code 等平台优先通过 `shared-memory-hub` Skill 接入本库。本地规则只保留短入口或平台适配补丁；如果本地补丁改变了共享记忆库工作方式，应同步更新 Skill。

## 来源字段

`source_platform` 记录内容的原始来源，不记录本次整理者。

候选记忆升级为正式经验时，默认继承原候选的 `source_platform` 和 `source_device`。例如 Codex 只是把 Hermes 产生的候选升级到 `02-可复用经验库`，正式经验仍应写 `source_platform: Hermes`。

`applies_to` 记录适用对象，不等同于来源。
"""


CORE_RULE = """---
source_platform: User
source_device: Unknown
source_type: 核心规则
created_at: {created_at}
status: 已确认
applies_to:
  - Codex
  - Hermes
  - Claude Code
  - Obsidian
---

# 智能体接入规则

## 查库时机

复杂任务、长期项目、本机环境、配置修改、自动化、历史规则相关任务，应先查询共享记忆库。

简单问答、翻译、改写、一次性小操作不用查库。

## 查库顺序

1. `01-核心规则`
2. `02-可复用经验库`
3. `03-候选确认清单`
4. `04-聊天摘要`
5. `05-项目资料`

只读取最相关的 3 到 5 个文件，不全文加载整个库。

## 写入边界

可以自动写入：

- `04-聊天摘要`
- `03-候选确认清单`

不能自动修改：

- `01-核心规则`
- `02-可复用经验库`

升级正式经验或核心规则前必须等待用户确认。

## Skill 优先原则

跨平台共享记忆库逻辑优先沉淀到 `shared-memory-hub` Skill。各平台本地规则只做短入口或临时适配；如果本地规则新增了 Skill 未覆盖的场景，必须同步更新 Skill，避免不同平台各用一套规则。

## 来源字段规则

`source_platform` 表示内容最初来自哪个智能体或人工来源，不表示本次整理入库者。

从 `03-候选确认清单` 升级到 `02-可复用经验库` 时，必须先核对原候选的 `source_platform` 和 `source_device`，并在正式经验中继承原始来源。整理者、升级者或审阅者可以写在正文说明里，不要覆盖来源字段。

`applies_to` 表示这条内容适用于哪些平台、项目或场景，不是来源。
"""


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


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help="AI智能体记忆库保存路径")
    args = parser.parse_args()

    root = resolve_root(args.root)
    root.mkdir(parents=True, exist_ok=True)

    created = []
    for name in DIRS:
        path = root / name
        path.mkdir(exist_ok=True)
        created.append(str(path))

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    if write_if_missing(root / "00-共享记忆库入口.md", ENTRY.format(created_at=created_at)):
        created.append(str(root / "00-共享记忆库入口.md"))
    if write_if_missing(root / "01-核心规则" / "智能体接入规则.md", CORE_RULE.format(created_at=created_at)):
        created.append(str(root / "01-核心规则" / "智能体接入规则.md"))

    print(f"已初始化共享记忆库：{root}")
    print(f"已创建或确认 {len(DIRS)} 个目录。")
    print("已存在的笔记不会被覆盖。")
    print()
    print("下一步提醒：")
    print("请询问用户是否要继续创建自动化任务。")
    print("建议任务：每日聊天摘要整理、每周候选确认审阅。")
    print("用户确认读写范围和运行时间前，不要创建自动化任务。")


if __name__ == "__main__":
    main()
