# 🧩 松果 Skills

[English](./README.en.md) | 中文

这里收集我自用并逐步公开的 AI Skills。每个 Skill 都是一个可以被 Agent 读取的结构化工作流，用来把重复任务做得更稳、更省心。

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-4-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square)
![Hermes](https://img.shields.io/badge/Hermes-Skill-3B82F6?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8B5CF6?style=flat-square)

---

## ⭐ 精选 Skill

最常用、最适合别人直接查看和安装的几个 Skill。

### 🧠 记忆与协作

**共享记忆库**

[shared-memory-hub](#shared-memory-hub) - 给 Codex、Hermes、Claude Code、OpenClaw 等多个 AI Agent 共用一套 Obsidian 或本地 Markdown 共享记忆库。

### 📚 阅读与学习

**每日读书**

[daily-reading](#daily-reading) - 进入读书模式，基于授权平台记忆和项目资料维护阅读画像，并按周生成个性化推荐书单。

### 🎨 内容与配图

**小松鼠配图**

[xiao-songshu-peitu](#xiao-songshu-peitu) - 用固定小松鼠 IP 为中文文章、帖子、小红书、公众号和工作流文档生成配图方案和提示词。

### 🚀 Codex 工作流

**Codex Skill 启动台**

[codex-skill-launchpad](#codex-skill-launchpad) - 把已经安装的 Codex Skills 做成可见、可点击、可复用的入口文件夹和专属对话。

---

## 📦 完整目录

| 中文名 | Skill | 分类 | 一句话 | 安装链接 |
|---|---|---|---|---|
| 共享记忆库 | [shared-memory-hub](#shared-memory-hub) | 记忆与协作 | 给多个 AI Agent 共用一套 Obsidian 或本地 Markdown 共享记忆库 | [安装](https://github.com/yxcops/songguo-skills/tree/main/shared-memory-hub) |
| 每日读书 | [daily-reading](#daily-reading) | 阅读与学习 | 进入读书模式，基于授权记忆维护阅读画像并生成每周推荐书单 | [安装](https://github.com/yxcops/songguo-skills/tree/main/daily-reading) |
| 小松鼠配图 | [xiao-songshu-peitu](#xiao-songshu-peitu) | 内容与配图 | 用固定小松鼠 IP 为中文内容生成正文配图方案和提示词 | [安装](https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu) |
| Codex Skill 启动台 | [codex-skill-launchpad](#codex-skill-launchpad) | Codex 工作流 | 把 Codex Skills 做成可视化入口项目和专属对话 | [安装](https://github.com/yxcops/songguo-skills/tree/main/codex-skill-launchpad) |

---

## ⚙️ 安装方式

在 Codex、Claude Code、Hermes、OpenClaw 等支持 Skill 的 Agent 里，直接说：

```text
帮我安装这个 skill：https://github.com/yxcops/songguo-skills/tree/main/<skill-name>
```

把 `<skill-name>` 换成你想安装的目录名，例如：

```text
帮我安装这个 skill：https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu
```

不同 Agent 的安装目录和权限不同。安装前建议让 Agent 先读取 `SKILL.md`，确认它会做什么、不会做什么。

<a id="skills"></a>

---

## 🧰 Skills

<a id="shared-memory-hub"></a>

### 共享记忆库（shared-memory-hub）

让 Codex、Hermes、Claude Code、OpenClaw 等智能体共用一套 Obsidian 或本地 Markdown 共享记忆库。

它不是原始聊天记录垃圾桶，而是用来保存长期可复用的规则、经验、项目资料和候选沉淀。

**适合**

- 你同时使用多个 AI Agent，希望它们共享一套长期规则。
- 你想把经验分成核心规则、可复用经验、候选清单、聊天摘要和项目资料。
- 你希望每天或每周定期整理 AI 对话，但不想让 Agent 乱改核心规则。

**不适合**

- 只想临时记一句话。
- 想把所有聊天记录原封不动塞进记忆库。
- 想自动创建 Notion 数据库。这个 Skill 默认只处理本地 Markdown 或 Obsidian 文件夹。

**怎么触发**

```text
请使用 shared-memory-hub Skill，帮我创建一个 AI 智能体共享记忆库。
```

```text
请使用 shared-memory-hub Skill，检查这个共享记忆库结构是否完整。
```

安装链接：

```text
https://github.com/yxcops/songguo-skills/tree/main/shared-memory-hub
```

<a id="daily-reading"></a>

### 每日读书（daily-reading）

把读书过程整理成一个可持续的系统：进入读书模式、讨论书中内容、沉淀读书笔记、基于授权平台记忆和项目资料维护阅读画像，并按周生成 5 本个性化推荐书单。

它是通用 Skill，不绑定某一个平台。Codex、Hermes、Claude Code、OpenClaw 都可以使用核心规则；自动定时、渠道推送、读取日记、历史记录或共享记忆，需要对应平台额外配置和用户授权。

首次使用时，它会先引导用户确认每日读书目录；确认后再创建或复用 `读书笔记`、`每周推荐书单`、`阅读画像.md` 和 `设置.md`。如果用户授权，它还会读取当前平台的项目说明、共享记忆摘要或历史摘要，先生成阅读画像，再用于后续书单推荐。

**适合**

- 读书时想让 AI 陪你讨论，并把有价值的内容沉淀下来。
- 想在 Obsidian 或本地 Markdown 里维护长期读书笔记。
- 已经有读书笔记目录，想在不移动原文件的前提下接入。
- 想每周基于近期目标、阅读画像和已读内容推荐 5 本书。
- 想让推荐书单参考自己当前项目、长期记忆或过往会话摘要。
- 想把同一套读书规则分享给不同 AI Agent 使用。

**不适合**

- 希望安装后自动接管所有平台定时任务。定时任务需要平台单独配置。
- 希望默认读取日记、历史对话或私人目录。读取这些内容必须经过用户授权。
- 只想做一次普通书籍摘要。

**怎么触发**

```text
请使用 daily-reading Skill，开始读书。
```

```text
请使用 daily-reading，帮我生成本周推荐书单。
```

```text
请使用 daily-reading，基于我授权的项目资料初始化阅读画像。
```

安装链接：

```text
https://github.com/yxcops/songguo-skills/tree/main/daily-reading
```

<a id="xiao-songshu-peitu"></a>

### 小松鼠配图（xiao-songshu-peitu）

为中文文章、帖子、小红书、公众号、Notion 文档和工作流说明生成带固定小松鼠 IP 的正文配图方案和提示词。

默认小松鼠形象是橙棕色毛绒身体、奶油脸颊、深绿色卷曲尾巴和蓝色发光线路。它更像一个信息整理员，而不是普通可爱头像。

**适合**

- 给中文长文设计正文配图。
- 给公众号、小红书、Notion、方法论文档做视觉解释。
- 想保持同一个小松鼠 IP 的角色一致性。
- 先要配图策略、shot list 或单张生图提示词。

**不适合**

- 想要完全随机风格的普通 AI 图片。
- 想直接发布到社交平台。
- 不需要固定角色一致性的简单配图。

**怎么触发**

```text
请使用 小松鼠配图（xiao-songshu-peitu）Skill，帮我为这篇中文内容设计 3 张小松鼠风格正文配图。
```

```text
请使用 xiao-songshu-peitu，为这篇内容生成 1 张公众号正文配图，并保持小松鼠角色一致。
```

安装链接：

```text
https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu
```

<a id="codex-skill-launchpad"></a>

### Codex Skill 启动台（codex-skill-launchpad）

把一组全局安装的 Codex Skills 整理成 Codex 客户端里的可视化入口项目：每个 Skill 一个入口文件夹，每个入口一个专属对话。

它解决的问题是：Skill 装多以后不容易看见，也不方便直接点进固定对话使用。

**适合**

- 你在 Codex 客户端里安装了很多 Skill，想做一个可视化入口。
- 你希望每个 Skill 有一个固定文件夹和一个专属对话。
- 你想把入口放到一个专门项目，或者放进已有的 Codex 项目。

**不适合**

- Hermes、Claude Code 这类没有 Codex 桌面项目和专属对话结构的平台。
- 真实生成图片、发微博、发公众号、抓取 X 内容。它只负责入口编排，不负责执行这些业务动作。
- 想把 Skill 系统级锁死到某个对话。这个 Skill 提供的是使用约定，不是系统锁。

**怎么触发**

```text
请使用 codex-skill-launchpad Skill，把下面这些 Skill 整理成一个可视化入口项目，并为每个 Skill 创建专属对话。
```

安装链接：

```text
https://github.com/yxcops/songguo-skills/tree/main/codex-skill-launchpad
```

---

## 🧪 平台兼容

| Skill | Codex | Claude Code | Hermes | OpenClaw | 说明 |
|---|---|---|---|---|---|
| shared-memory-hub | 支持 | 支持 | 支持 | 支持 | 需要能读写本地 Markdown 文件 |
| daily-reading | 支持 | 支持 | 支持 | 支持 | 核心规则通用；自动定时和渠道推送取决于平台 |
| xiao-songshu-peitu | 支持 | 支持 | 视工具而定 | 视工具而定 | 需要图片生成能力或可交付提示词 |
| codex-skill-launchpad | 支持 | 不推荐 | 不推荐 | 不推荐 | 依赖 Codex 客户端项目和专属对话 |

---

## 📌 关于

松果 Skills 是我把自己反复使用的 AI 工作流整理成可安装、可审阅、可分享的 Skill 合集。

它优先服务真实使用，不追求数量堆砌；每个 Skill 都应该说清楚适合什么、不适合什么、怎么触发。

这个仓库会逐步收集我自己常用、可复用、适合公开分享的 AI Skills。

如果你要单独分享某一个 Skill，推荐直接发它的安装链接；如果你要分享整个合集，发这个仓库首页即可。

MIT License，自由使用、修改和再分发。
