# 🧩 松果 Skills

[English](./README.en.md) | 中文

这里收集我自用并逐步公开的 AI Skills。每个 Skill 都是一个可以被 Agent 读取的结构化工作流，用来把重复任务做得更稳、更省心。

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square)
![Hermes](https://img.shields.io/badge/Hermes-Skill-3B82F6?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8B5CF6?style=flat-square)

---

## ⭐ 精选 Skill

最常用、最适合别人直接查看和安装的几个 Skill。

### 🧠 AI 记忆与协作

[**🧠 shared-memory-hub**](#shared-memory-hub) - 给 Codex、Hermes、Claude Code、OpenClaw 等多个 AI Agent 共用一套 Obsidian 或本地 Markdown 共享记忆库。

### 🎨 中文内容与配图

[**🐿️ xiao-songshu-peitu**](#xiao-songshu-peitu) - 用固定小松鼠 IP 为中文文章、帖子、小红书、公众号和工作流文档生成配图方案和提示词。

### 🚀 Codex 工作流

[**🚀 codex-skill-launchpad**](#codex-skill-launchpad) - 把已经安装的 Codex Skills 做成可见、可点击、可复用的入口文件夹和专属对话。

---

## 📦 完整目录

| Skill | 一句话 | 适合 | 安装链接 |
|---|---|---|---|
| [🧠 shared-memory-hub](#shared-memory-hub) | 给多个 AI Agent 共用一套 Obsidian 或本地 Markdown 共享记忆库 | 长期规则、经验沉淀、多 Agent 协作 | [安装](https://github.com/yxcops/songguo-skills/tree/main/shared-memory-hub) |
| [🐿️ xiao-songshu-peitu](#xiao-songshu-peitu) | 用固定小松鼠 IP 为中文内容生成正文配图方案和提示词 | 公众号、小红书、Notion、工作流文档配图 | [安装](https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu) |
| [🚀 codex-skill-launchpad](#codex-skill-launchpad) | 把 Codex Skills 做成可视化入口项目和专属对话 | Codex 客户端 Skill 管理 | [安装](https://github.com/yxcops/songguo-skills/tree/main/codex-skill-launchpad) |

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

### 🧠 shared-memory-hub（共享记忆库）

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

<a id="xiao-songshu-peitu"></a>

### 🐿️ xiao-songshu-peitu（小松鼠配图）

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

### 🚀 codex-skill-launchpad（Codex Skill 启动台）

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
| xiao-songshu-peitu | 支持 | 支持 | 视工具而定 | 视工具而定 | 需要图片生成能力或可交付提示词 |
| codex-skill-launchpad | 支持 | 不推荐 | 不推荐 | 不推荐 | 依赖 Codex 客户端项目和专属对话 |

---

## 📌 关于

松果 Skills 是我把自己反复使用的 AI 工作流整理成可安装、可审阅、可分享的 Skill 合集。

它优先服务真实使用，不追求数量堆砌；每个 Skill 都应该说清楚适合什么、不适合什么、怎么触发。

这个仓库会逐步收集我自己常用、可复用、适合公开分享的 AI Skills。

如果你要单独分享某一个 Skill，推荐直接发它的安装链接；如果你要分享整个合集，发这个仓库首页即可。

MIT License，自由使用、修改和再分发。
