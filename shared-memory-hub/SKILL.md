---
name: shared-memory-hub
description: 用于创建、检查和使用 Obsidian 或本地 Markdown 共享记忆库的 Skill。适用于 Codex、Hermes、Claude Code、OpenClaw 或其他能读写本地 Markdown 文件的 AI Agent。Use this skill when setting up or using an Obsidian/shared Markdown memory hub for AI agents.
---

# 共享记忆库

这个 Skill 用来帮助 AI 智能体创建、检查和使用一套基于 Obsidian 或本地 Markdown 文件夹的共享记忆库。

共享记忆库用于多个智能体之间沉淀长期经验和规则。它不是原始聊天记录垃圾桶。

## 接入口径

优先通过本 Skill 执行共享记忆库的创建、检查、查询、摘要、候选审阅和来源字段判断。Codex、Hermes、Claude Code、OpenClaw 等平台的本地规则只保留短入口或平台适配说明。

如果某个平台暂时不能安装或加载 Skill，可以把本 Skill 的核心规则写入本地规则；但只要本地规则补充了新场景、修正了判断或发现了本 Skill 没覆盖的边界，就要同步更新本 Skill，避免平台规则长期分叉。

## 兼容平台

默认兼容：

- Codex
- Hermes
- Claude Code
- OpenClaw
- 其他能读取和写入本地 Markdown 文件的 AI Agent

各平台的安装方式、自动化能力和常驻规则位置不一样。接入前先读 `references/platform-compatibility.md`。

## 支持范围

当前默认支持：

1. Obsidian 库里的 Markdown 文件夹
2. 普通本地 Markdown 文件夹

暂不支持自动创建 Notion 数据库。

如果用户想用 Notion，先给方案，不要运行 `init_vault.py`。Notion 需要单独设计数据库、字段、授权和 API 流程。

## 初始化规则

安装这个 Skill 后，**不会自动创建共享记忆库**。

只有用户明确要求创建或初始化时，才可以执行初始化。

如果用户没有明确给出保存位置，必须先询问：

```text
你想把共享记忆库保存在哪里？是 Obsidian 库里，还是普通本地文件夹？
```

如果用户已经给出明确路径，可以直接使用：

```bash
python3 scripts/init_vault.py --root /path/to/AI智能体记忆库
```

不要猜测用户的私人目录，也不要把共享记忆库写到未确认的位置。

初始化完成后，要提醒用户是否继续创建自动化任务，但不要擅自创建：

```text
共享记忆库已经创建好。是否要继续创建两个自动化任务：
1. 每日聊天摘要整理
2. 每周候选确认审阅

如果同意，我会先说明任务会读取什么、写入什么、什么时候运行，然后等你确认后再创建。
```

## 标准目录

默认共享记忆库文件夹名为：

```text
AI智能体记忆库
```

标准结构：

```text
AI智能体记忆库/
├── 00-共享记忆库入口.md
├── 01-核心规则/
├── 02-可复用经验库/
├── 03-候选确认清单/
├── 04-聊天摘要/
├── 05-项目资料/
└── 90-归档废弃/
```

创建或解释目录结构时，按需读取 `references/vault-structure.md`。

## 什么时候查库

以下情况需要查共享记忆库：

- 用户提到“之前”“上次”“照旧”“按原来的规则”
- 涉及 Codex、Hermes、Claude Code、Obsidian、本机环境、网络、自动化或长期项目
- 涉及项目背景、重复流程、配置修改、故障排查
- 任务失败后需要复盘
- 智能体不确定是否已有相关经验或规则

以下情况通常不用查：

- 简单问候
- 翻译、改写、润色
- 一次性小问答
- 不涉及历史规则、本机环境或长期项目的问题

只检索共享记忆库，不检索整个 Obsidian。

默认查库顺序：

1. `01-核心规则`
2. `02-可复用经验库`
3. `03-候选确认清单`
4. `04-聊天摘要`
5. `05-项目资料`

如果任务明确属于某个长期项目，可以把 `05-项目资料` 提前到 `02-可复用经验库` 后面查。

最多读取 3 到 5 个最相关文件，不要全文加载整个库。

## 回答中的查库说明

复杂任务回答时，要简短说明是否查过共享记忆库。

如果查了，要说明命中的文件名。

查到的内容只是历史线索，不一定是当前事实。涉及版本、端口、账号状态、价格、网页链接、运行状态和配置内容时，必须重新核对当前状态。

## 写入边界

智能体可以自动写入：

- `04-聊天摘要`
- `03-候选确认清单`

智能体不能自动修改：

- `01-核心规则`
- `02-可复用经验库`

从候选确认清单升级到可复用经验库，必须等待用户明确确认。

修改核心规则必须等待用户明确确认，而且应该非常克制。

## 新文件字段

新建文件必须包含这 6 个字段：

```yaml
---
source_platform: Codex
source_device: Mac mini
source_type: 聊天摘要
created_at: 2026-06-07 12:00
status: 已整理
applies_to:
  - Codex
---
```

字段说明和示例见 `references/frontmatter-template.md`。

## 来源字段规则

`source_platform` 表示这条内容最初来自哪个智能体或人工来源，不表示谁在本轮负责整理入库。

常见判断：

- Codex 会话整理出的摘要或经验，写 `Codex`。
- Hermes 会话、Hermes 定时任务或 Hermes 候选记忆升级出的经验，写 `Hermes`。
- Claude Code 会话整理出的内容，写 `Claude Code`。
- 用户手动整理出的内容，写 `User`。
- 多个平台共同产生、无法明确拆分时，写 `Mixed`。

如果 Codex 只是把 Hermes 产生的候选记忆升级到 `02-可复用经验库`，正式经验仍应写 `source_platform: Hermes`。整理者、升级者或审阅者可以写在正文的“整理说明”里，不要改写来源字段。

`source_device` 表示原始来源发生在哪台设备上。`applies_to` 表示这条内容适用于哪些平台或场景，不是来源。

文件名、一级标题和 `source_platform` 应保持一致。候选升级为正式经验时，文件名前缀和一级标题继承原候选来源平台；来源冲突时先标记为“来源待确认”，不要直接升级。

## 自动化提示词

自动化提示词只是模板，不包含用户私人数据。

- Codex 每日记忆整理：`references/codex-automation-prompts.md`
- 每周候选确认审阅：`references/codex-automation-prompts.md`
- Hermes 每日整理任务：`references/hermes-cron-prompt.md`
- 候选确认判断标准：`references/review-rules.md`
- 安装后的启动提示词：`references/startup-prompts.md`
- 平台兼容说明：`references/platform-compatibility.md`

## 脚本

初始化共享记忆库：

```bash
python3 scripts/init_vault.py --root /path/to/AI智能体记忆库
```

检查共享记忆库：

```bash
python3 scripts/check_vault.py --root /path/to/AI智能体记忆库
```

如果没有传入 `--root`，脚本会依次尝试：

1. `AI_MEMORY_VAULT_PATH`
2. `OBSIDIAN_VAULT_PATH/AI智能体记忆库`

脚本不会覆盖已经存在的笔记。
