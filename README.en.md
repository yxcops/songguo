# 🧩 Songguo Skills

[中文](./README.md) | English

This repository collects AI Skills that I use, refine, and gradually publish. Each Skill is a structured workflow that an Agent can read and follow to perform recurring tasks more reliably.

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-5-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square)
![Hermes](https://img.shields.io/badge/Hermes-Skill-3B82F6?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8B5CF6?style=flat-square)

---

## ⭐ Featured Skills

The Skills I use most and consider easiest for others to inspect and install.

### 📝 Notes & Journaling

**Obsidian Diary**

[obsidian-diary](#obsidian-diary) - Turn Obsidian or local Markdown diary writing, historical backfill, format checks, and export into a stable Agent workflow.

### 🧠 AI Memory & Collaboration

**Shared Memory Hub**

[shared-memory-hub](#shared-memory-hub) - Create and maintain a shared Obsidian or local Markdown memory vault for Codex, Hermes, Claude Code, OpenClaw, and other Agents.

### 📚 Reading & Learning

**Daily Reading**

[daily-reading](#daily-reading) - Enter reading mode, maintain a reading profile from authorized memory and project materials, and generate a personalized weekly book list.

### 🎨 Content & Visuals

**Squirrel Illustration**

[xiao-songshu-peitu](#xiao-songshu-peitu) - Create fixed squirrel-IP illustration plans and prompts for Chinese articles, posts, WeChat articles, Xiaohongshu notes, and workflow docs.

### 🚀 Codex Workflow

**Codex Skill Launchpad**

[codex-skill-launchpad](#codex-skill-launchpad) - Turn installed Codex Skills into visible entry folders and dedicated Codex chats.

---

## 📦 Full Catalog

| Name | Skill | Category | One-liner | Install |
|---|---|---|---|---|
| Obsidian Diary | [obsidian-diary](#obsidian-diary) | Notes & Journaling | Write current-day diary entries, backfill old entries explicitly, check format, and export text | [Install](https://github.com/yxcops/songguo-skills/tree/main/obsidian-diary) |
| Shared Memory Hub | [shared-memory-hub](#shared-memory-hub) | Memory & Collaboration | Build a shared Obsidian or Markdown memory vault for multiple AI Agents | [Install](https://github.com/yxcops/songguo-skills/tree/main/shared-memory-hub) |
| Daily Reading | [daily-reading](#daily-reading) | Reading & Learning | Enter reading mode, maintain a memory-aware profile, and generate a weekly book list | [Install](https://github.com/yxcops/songguo-skills/tree/main/daily-reading) |
| Squirrel Illustration | [xiao-songshu-peitu](#xiao-songshu-peitu) | Content & Visuals | Create fixed squirrel-IP illustration plans and prompts for Chinese content | [Install](https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu) |
| Codex Skill Launchpad | [codex-skill-launchpad](#codex-skill-launchpad) | Codex Workflow | Turn Codex Skills into visible entry folders and dedicated Codex chats | [Install](https://github.com/yxcops/songguo-skills/tree/main/codex-skill-launchpad) |

---

## ⚙️ Installation

In Codex, Claude Code, Hermes, OpenClaw, or another Agent that supports Skills, say:

```text
Install this skill: https://github.com/yxcops/songguo-skills/tree/main/<skill-name>
```

Replace `<skill-name>` with the folder name you want to install. For example:

```text
Install this skill: https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu
```

Different Agents use different installation paths and permissions. Before installing, ask the Agent to read `SKILL.md` and summarize what the Skill does and does not do.

## Publishing Rules

This repository is for Skills that are ready to be inspected and shared. Each Skill should:

- come from a real repeated workflow, not catalog filling;
- explain what it is for and what it is not for in `SKILL.md`;
- avoid real private paths, accounts, tokens, cookies, raw chats, or real diaries;
- verify representative flows in a temporary folder when scripts are included;
- make platform automation, channel delivery, and external access opt-in and separately configured.

<a id="skills"></a>

---

## 🧰 Skills

<a id="obsidian-diary"></a>

### Obsidian Diary (obsidian-diary)

Turns Obsidian or local Markdown diary handling into a reusable workflow: current-day entries go to today, historical entries require explicit backfill intent, old imports do not fake live timestamps, and checks or exports can be handled by the bundled script.

It is not a private Hermes configuration package and contains no real diary content. After installation, the user still needs to confirm the Obsidian vault path and diary root.

**Best for**

- Writing Obsidian diary entries with an AI Agent.
- Separating "write today's diary" from "backfill an old date".
- Importing old diary text into dated Markdown files.
- Checking file names, month folders, weekdays, and basic format.
- Exporting a day's diary text for review or sharing.

**Not for**

- Letting an Agent read all private diary files by default.
- Automatically taking over Hermes, Telegram, Feishu, WeChat, or other channel configuration.
- Turning a diary workflow into a database, daemon, or fully automated platform.

**Example prompts**

```text
Use obsidian-diary to write today's Obsidian diary entry.
```

```text
Use obsidian-diary to backfill my diary for 2021-09-20.
```

```text
Use obsidian-diary to check my diary folder format.
```

Install link:

```text
https://github.com/yxcops/songguo-skills/tree/main/obsidian-diary
```

<a id="shared-memory-hub"></a>

### Shared Memory Hub (shared-memory-hub)

Builds a shared Obsidian or local Markdown memory vault for Codex, Hermes, Claude Code, OpenClaw, and other Agents.

It is not a raw chat-log dump. It is designed for long-term reusable rules, experience, project material, candidate notes, and structured review.

**Best for**

- You use multiple AI Agents and want them to share long-term operating rules.
- You want memory split into core rules, reusable experience, candidate notes, chat summaries, and project material.
- You want daily or weekly memory review without letting Agents freely rewrite core rules.

**Not for**

- Saving one temporary sentence.
- Dumping every chat transcript into memory.
- Creating a Notion database. This Skill works with local Markdown or Obsidian folders by default.

**Example prompts**

```text
Use the shared-memory-hub Skill to create an AI Agent shared memory vault.
```

```text
Use the shared-memory-hub Skill to check whether this shared memory vault structure is complete.
```

Install link:

```text
https://github.com/yxcops/songguo-skills/tree/main/shared-memory-hub
```

<a id="daily-reading"></a>

### Daily Reading (daily-reading)

Turns reading into a sustainable workflow: enter reading mode, discuss what you are reading, keep useful notes, maintain a reading profile, and generate a weekly list of 5 personalized books.

It is a general-purpose Skill, not a platform-specific automation. Codex, Hermes, Claude Code, and OpenClaw can all use the core workflow. Scheduling, channel delivery, diary access, history access, and shared-memory access depend on each platform's capabilities and explicit user permission.

On first use, it guides the user to confirm a local reading directory before creating or reusing `读书笔记`, `每周推荐书单`, `阅读画像.md`, and `设置.md`. With permission, it can also read project docs, shared-memory summaries, or history summaries to initialize a reading profile before weekly recommendations.

**Best for**

- Reading with an AI assistant while preserving useful thoughts and discussions.
- Keeping long-term reading notes in Obsidian or local Markdown.
- Connecting an existing reading-notes folder without moving existing files.
- Generating 5 weekly book recommendations from recent goals, reading notes, and a reading profile.
- Letting recommendations reflect current projects, long-term memory, or summarized past conversations.
- Sharing one reading workflow across multiple AI Agents.

**Not for**

- Automatically taking over platform-level scheduled tasks after installation. Scheduling must be configured separately.
- Reading diaries, chat history, or private folders by default. These need explicit user permission.
- One-off generic book summaries.

**Example prompts**

```text
Use the daily-reading Skill. Start reading mode.
```

```text
Use daily-reading to generate this week's recommended book list.
```

```text
Use daily-reading to initialize my reading profile from the project materials I authorize.
```

Install link:

```text
https://github.com/yxcops/songguo-skills/tree/main/daily-reading
```

<a id="xiao-songshu-peitu"></a>

### Squirrel Illustration (xiao-songshu-peitu)

Creates article illustration plans and prompts for Chinese articles, posts, Xiaohongshu notes, WeChat articles, Notion docs, and workflow explainers using a fixed squirrel character IP.

The default squirrel character has orange-brown plush fur, cream cheeks, a dark green curled tail, and blue glowing circuit lines. It behaves more like an information organizer than a generic cute avatar.

**Best for**

- Designing illustrations for Chinese long-form content.
- Creating visual explanations for WeChat, Xiaohongshu, Notion, and methodology docs.
- Keeping the same squirrel IP consistent across images.
- Producing an illustration strategy, shot list, or image-generation prompt first.

**Not for**

- Generic random AI images.
- Posting directly to social platforms.
- Simple illustrations that do not need character consistency.

**Example prompts**

```text
Use the xiao-songshu-peitu Skill to design 3 squirrel-style illustrations for this Chinese article.
```

```text
Use xiao-songshu-peitu to create one WeChat article illustration prompt and keep the squirrel character consistent.
```

Install link:

```text
https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu
```

<a id="codex-skill-launchpad"></a>

### Codex Skill Launchpad (codex-skill-launchpad)

Organizes globally installed Codex Skills into a visible Codex desktop entry project: one entry folder per Skill, and one dedicated chat per entry.

It solves a practical problem: once many Skills are installed, they are hard to see and inconvenient to open directly.

**Best for**

- You installed many Skills in Codex desktop and want a visible entry point.
- You want each Skill to have its own folder and dedicated chat.
- You want the entry project created in a dedicated folder or inside an existing Codex project.

**Not for**

- Hermes or Claude Code, because they do not have the same Codex desktop project and dedicated-chat structure.
- Generating images, posting to Weibo or WeChat, or capturing X content. This Skill only organizes entry points.
- Hard-locking a Skill to a chat at the system level. It provides a workflow convention, not a platform-level lock.

**Example prompt**

```text
Use the codex-skill-launchpad Skill to organize these Skills into a visible entry project and create one dedicated chat for each Skill.
```

Install link:

```text
https://github.com/yxcops/songguo-skills/tree/main/codex-skill-launchpad
```

---

## 🧪 Compatibility

| Skill | Codex | Claude Code | Hermes | OpenClaw | Notes |
|---|---|---|---|---|---|
| obsidian-diary | Supported | Supported | Supported | Supported | Needs a confirmed local diary path; channel automation is platform-specific |
| shared-memory-hub | Supported | Supported | Supported | Supported | Needs access to local Markdown files |
| daily-reading | Supported | Supported | Supported | Supported | Core workflow is portable; scheduling and channel delivery are platform-dependent |
| xiao-songshu-peitu | Supported | Supported | Tool-dependent | Tool-dependent | Needs image-generation ability, or can deliver prompts only |
| codex-skill-launchpad | Supported | Not recommended | Not recommended | Not recommended | Depends on Codex desktop projects and dedicated chats |

---

## 📌 About

Songguo Skills is a collection of AI workflows I repeatedly use, organized into installable, reviewable, and shareable Skills.

It prioritizes real usage over catalog size. Each Skill should clearly explain what it is for, what it is not for, and how to trigger it.

This repository will gradually collect AI Skills that are useful, reusable, and suitable for public sharing.

To share one Skill, send its direct install link. To share the whole collection, send this repository homepage.

MIT License. You can use, modify, and redistribute these Skills freely.
