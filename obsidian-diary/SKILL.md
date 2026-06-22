---
name: obsidian-diary
description: 用于在 Obsidian 或本地 Markdown 日记本中记录当天日记、明确补写历史日记、导出日记文本、检查日记文件结构和沉淀日记写入规则的 Skill。Use when the user explicitly asks to write, backfill, inspect, export, or standardize an Obsidian diary/journal; do not trigger for generic note taking, general life advice, or private diary reading without permission.
---

# Obsidian Diary

这个 Skill 帮 Agent 稳定处理 Obsidian 日记本：写今天的日记、明确补写历史日记、检查格式、导出文本，并在不同平台之间保持同一套边界。

它是公开可分享版本，不绑定任何私人 Obsidian 路径、Hermes 配置、渠道账号或真实日记内容。

## 核心边界

只处理这些任务：

1. 用户明确要求写入、补写、检查、导出或整理日记本。
2. 用户已经给出或确认日记本位置。
3. 当前平台具备读取或写入 Markdown 文件的能力。

不要做这些事：

- 不猜测用户私人路径。
- 不默认读取已有日记全文。
- 不把普通聊天内容自动写入日记。
- 不把“写个日记，昨天……”理解为补写昨天。
- 不伪造历史日期的实时写入时间线。
- 不公开真实日记、Token、Cookie、账号、渠道 ID 或本机绝对路径。

## 意图分流

按用户原话判断任务类型。

### 当天日记

用户说“写个日记”“记到日记”“今天日记”“帮我记录一下今天”时，写入今天的日期文件。

即使正文里出现“昨天”“前几天”“小时候”，只要用户没有明确说“补写”，也仍然写入今天。

当天日记使用时间线 callout：

```markdown
农历：...

> [!NOTE] 14:30
> 今天把日记系统整理清楚了。
```

### 明确补写

只有用户明确说“补写”“补记”“补一篇历史日记”“导入旧日记”，才进入补写流程。

补写必须有明确日期。没有日期时先问清楚，不要自己猜。

历史补写使用 `## 补写` 区块，不添加实时 callout：

```markdown
农历：...

## 补写

这是旧日记原文。
```

### 历史导入

较早年份的旧日记可以按目标日期直接创建文件。要保留原文，不改写成总结，不伪造当天时间线。

如果工具脚本无法覆盖某个导入需求，可以按 `references/obsidian-format.md` 手动创建文件。

### 图片和附件

图片、截图或语音转写只在用户明确要求“也放进日记”“加到刚才那条”时写入。

如果当前平台无法确认附件归属，先问用户要放到哪一天、哪一条记录。不要把相邻文件或历史附件自动塞进日记。

附件规则见 `references/workflow-rules.md`。

## 首次使用

先确认日记本位置。不要猜测。

推荐用户提供 Obsidian 库路径和日记根目录：

```text
Obsidian 库：/path/to/vault
日记根目录：日记本
```

如果当前平台能运行脚本，可先检查：

```bash
python3 scripts/diary_tool.py --vault /path/to/vault --diary-root 日记本 info
python3 scripts/diary_tool.py --vault /path/to/vault --diary-root 日记本 check
```

如果用户只想看方案，不要创建或修改文件。

## 标准结构

默认日记根目录：

```text
日记本/
├── 2026-06/
│   └── 2026年6月22日，星期一.md
└── 2026-07/
    └── 2026年7月1日，星期三.md
```

文件名、月份目录、正文格式、农历行和导出规则见 `references/obsidian-format.md`。

## 工具脚本

脚本只使用本地文件，不访问网络。

初始化或查看位置：

```bash
python3 scripts/diary_tool.py --vault /path/to/vault --diary-root 日记本 info
python3 scripts/diary_tool.py --vault /path/to/vault --diary-root 日记本 init
```

写当天日记：

```bash
python3 scripts/diary_tool.py --vault /path/to/vault record --text "写个日记，今天把日记 Skill 做成了公开版。"
```

明确补写：

```bash
python3 scripts/diary_tool.py --vault /path/to/vault backfill --date 2021-09-20 --text "旧日记原文。"
```

检查日记本：

```bash
python3 scripts/diary_tool.py --vault /path/to/vault check
```

导出某天文本：

```bash
python3 scripts/diary_tool.py --vault /path/to/vault export --date 2026-06-22
```

## 平台接入

Codex、Hermes、Claude Code、OpenClaw 等平台都可以使用本 Skill 的规则；自动触发、渠道消息、图片接收、定时任务和长期状态要按平台另行配置。

平台接入前读：

- `references/workflow-rules.md`
- `references/privacy-and-config.md`

## 验证清单

完成日记任务前检查：

- 日期、星期、月份目录和文件名一致。
- 当天记录使用实时 callout。
- 历史补写使用 `## 补写`，没有伪造实时 callout。
- 用户原文被保留，没有被改写成空泛总结。
- 未经授权没有读取其他日期日记。
- 输出和公开文件没有包含敏感路径、账号、密钥或真实私人内容。
