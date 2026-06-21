---
name: daily-reading
description: 用于初始化每日读书目录、进入读书模式、沉淀读书笔记、维护阅读画像，并按周生成个性化推荐书单的通用 Skill。适用于用户说“开始读书”“读书模式”“初始化每日读书”“设置读书目录”“生成每周推荐书单”等场景，兼容 Codex、Hermes、Claude Code、OpenClaw 或其他能读写本地 Markdown 文件的 AI Agent。
---

# 每日读书

这个 Skill 帮用户把读书过程变成可持续的记录系统：开始读书、讨论内容、记录笔记、更新阅读画像、每周推荐下一批适合读的书。

它默认不绑定任何单一平台。自动定时、渠道推送、读取日记、历史对话或共享记忆，都属于平台增强能力，接入前先读 `references/platform-setup.md`。

## 触发方式

用户说出以下意思时，进入读书模式：

- `开始读书`
- `读书模式`
- `我要读书`
- `进入读书模式`

用户说出以下意思时，进入首次设置或目录设置流程：

- `初始化每日读书`
- `设置读书目录`
- `把每日读书放到这个目录`
- `我已经有读书笔记目录`

用户说出以下意思时，退出读书模式：

- `退出读书模式`
- `结束读书`
- `今天先读到这里`

如果平台支持会话状态，一小时没有新消息时自动退出读书模式。通用做法见 `scripts/reading_tool.py` 的 `expire` 命令。

## 首次设置

第一次使用时，如果还没有每日读书目录，不要猜测用户的私人路径，也不要直接创建文件。先提醒用户选择一种目录方式：

1. 上级目录：在用户给的目录下创建或复用 `每日读书`。
2. 每日读书根目录：直接在用户给的目录下放 `读书笔记`、`每周推荐书单`、`阅读画像.md`、`设置.md`。
3. 现有读书笔记目录：把用户给的目录当作书籍笔记所在位置，不再嵌套新的 `读书笔记`。

创建前先展示将要创建或复用的结构，等用户确认后再创建。可用脚本先预览：

```bash
python3 scripts/reading_tool.py --parent /path/to/folder plan
python3 scripts/reading_tool.py --root /path/to/每日读书 plan
python3 scripts/reading_tool.py --notes-dir /path/to/读书笔记 plan
```

用户确认后再运行对应的 `init`。

默认结构：

```text
每日读书/
├── 读书笔记/
├── 每周推荐书单/
├── 阅读画像.md
└── 设置.md
```

如果用户给的目录里已经有 `读书笔记` 加 `每周推荐书单` 或 `每周推荐清单`，判断它已经是每日读书根目录，直接复用，不要再新建第二层 `每日读书` 或 `读书笔记`。

## 读书模式

进入读书模式后，所有回复都围绕当前阅读材料进行：

1. 先识别当前读的是哪本书、哪个版本、作者是谁。
2. 如果用户没有说书名，不要反复追问；先继续讨论，并在合适时提醒补充。
3. 如果能从上下文推测书名，先给出猜测，等用户确认后再写入正式书名。
4. 用户可以不按章节顺序读，只记录对他有用的部分。
5. 用户只是讨论时，不自动写笔记；只有用户明确说“记一下”“写进读书笔记”“生成读书笔记”“总结并记录”时才写入文件。

读书笔记目标不是流水账，而是让用户以后值得重看。笔记格式参考 `references/note-and-recommendation-formats.md` 和 `templates/book-note.md`。

如果用户明确要求把这次讨论写入笔记，可使用脚本追加：

```bash
python3 scripts/reading_tool.py --root /path/to/每日读书 note --kind thought --text "用户的想法或讨论结论"
```

常用类型：

- `excerpt`：摘录或用户转述的原文。
- `thought`：用户自己的想法。
- `question`：用户想继续追问的问题。
- `summary`：讨论后得到的结论。
- `action`：读完后要做的事。

## 笔记原则

写读书笔记时遵守这些规则：

- 保留用户自己的判断、疑问和表达，不要把它改成空泛总结。
- 摘要要短，重点回答“这本书讲什么、对我有什么用、我该怎么用”。
- 区分书中观点、用户观点、AI 补充判断。
- 不确定的版本、出版社、出版日期要标注“不确定”，不要补编。
- 遇到网上信息、最新版、购买渠道等易变事实时，要重新核对来源。

## 每周推荐书单

每周推荐书单固定推荐 5 本书。推荐依据应包含：

1. 用户近期正在做的事和反复提到的问题。
2. 用户已有读书记录和阅读画像。
3. 书本身的质量、版本可靠性和可获得性。
4. 这本书适合解决的问题。
5. 建议读法：精读、跳读、查阅，或先读指定章节。

生成格式见 `templates/weekly-books.md`。

每周推荐前，先生成“推荐上下文包”：

```bash
python3 scripts/reading_tool.py --root /path/to/每日读书 context --days 45
```

上下文包默认只读取每日读书目录里的阅读画像、近期读书笔记和近期推荐书单。只有用户明确授权时，才用 `--extra-source` 读取额外记忆文件：

```bash
python3 scripts/reading_tool.py --root /path/to/每日读书 context \
  --extra-source /path/to/已授权的记忆摘要.md
```

生成推荐时要把“本周判断依据”写清楚：读取了哪些读书笔记、阅读画像里有哪些变化、额外记忆提供了什么线索、哪些来源未授权或不确定。

Skill 只提供推荐逻辑、上下文整理和模板，不会自己常驻运行。每周一早上 6 点自动生成并发送，需要由 Hermes、OpenClaw、Codex 自动化或系统任务接入。配置自动发送前必须先读 `references/platform-setup.md`。

## 阅读画像

阅读画像用于记录用户长期阅读需求，不是评价用户。

它应每周更新一次，内容包括：

- 近期关注的问题
- 正在补的能力
- 更适合的书籍类型
- 不适合继续堆的书
- 下一阶段阅读建议

格式见 `templates/reading-profile.md`。

## 可选脚本

如果平台允许运行本地脚本，可使用：

```bash
python3 scripts/reading_tool.py check
```

这个脚本可以创建 `每日读书/读书笔记`、`每日读书/每周推荐书单` 等目录，追加读书笔记，并记录读书模式状态。

常用命令：

```bash
python3 scripts/reading_tool.py --root /path/to/每日读书 check
python3 scripts/reading_tool.py --root /path/to/每日读书 start --book "书名"
python3 scripts/reading_tool.py --root /path/to/每日读书 note --kind summary --text "今天的讨论结论"
python3 scripts/reading_tool.py --root /path/to/每日读书 context --days 45
python3 scripts/reading_tool.py --root /path/to/每日读书 recommendation
```

脚本通过这些环境变量定位用户的读书目录：

- `DAILY_READING_PARENT`：指定上级目录，在下面创建或复用 `每日读书`。
- `DAILY_READING_ROOT`：直接指定“每日读书”根目录。
- `DAILY_READING_NOTES_DIR`：指定现有 `读书笔记` 目录，不再嵌套新的 `读书笔记`。
- `OBSIDIAN_VAULT_PATH`：指定 Obsidian 库，再配合 `DAILY_READING_RELATIVE_DIR`，默认相对目录为 `每日读书`。

不要默认猜测用户的私人目录。没有路径时，先提醒用户配置。
