# 🧩 Songguo Skills

[中文](./README.md) | English

This repository collects AI Skills that I use, refine, and gradually publish. Each Skill is a structured workflow that an Agent can read and follow to perform recurring tasks more reliably.

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square)
![Hermes](https://img.shields.io/badge/Hermes-Skill-3B82F6?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8B5CF6?style=flat-square)

---

## ⭐ Featured Skills

The Skills I use most and consider easiest for others to inspect and install.

### 🧠 AI Memory & Collaboration

[**🧠 shared-memory-hub**](#shared-memory-hub) - Create and maintain a shared Obsidian or local Markdown memory vault for Codex, Hermes, Claude Code, OpenClaw, and other Agents.

### 🎨 Content & Visuals

[**🐿️ xiao-songshu-peitu**](#xiao-songshu-peitu) - Create fixed squirrel-IP illustration plans and prompts for Chinese articles, posts, WeChat articles, Xiaohongshu notes, and workflow docs.

### 🚀 Codex Workflow

[**🚀 codex-skill-launchpad**](#codex-skill-launchpad) - Turn installed Codex Skills into visible entry folders and dedicated Codex chats.

---

## 📦 Full Catalog

| Skill | One-liner | Best for | Install |
|---|---|---|---|
| [🧠 shared-memory-hub](#shared-memory-hub) | Build a shared Obsidian or Markdown memory vault for multiple AI Agents | Long-term rules, reusable experience, multi-Agent collaboration | [Install](https://github.com/yxcops/songguo-skills/tree/main/shared-memory-hub) |
| [🐿️ xiao-songshu-peitu](#xiao-songshu-peitu) | Create fixed squirrel-IP illustration plans and prompts for Chinese content | WeChat articles, Xiaohongshu, Notion docs, workflow explainers | [Install](https://github.com/yxcops/songguo-skills/tree/main/xiao-songshu-peitu) |
| [🚀 codex-skill-launchpad](#codex-skill-launchpad) | Turn Codex Skills into visible entry folders and dedicated Codex chats | Codex desktop Skill management | [Install](https://github.com/yxcops/songguo-skills/tree/main/codex-skill-launchpad) |

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

<a id="skills"></a>

---

## 🧰 Skills

<a id="shared-memory-hub"></a>

### 🧠 shared-memory-hub

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

<a id="xiao-songshu-peitu"></a>

### 🐿️ xiao-songshu-peitu

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

### 🚀 codex-skill-launchpad

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
| shared-memory-hub | Supported | Supported | Supported | Supported | Needs access to local Markdown files |
| xiao-songshu-peitu | Supported | Supported | Tool-dependent | Tool-dependent | Needs image-generation ability, or can deliver prompts only |
| codex-skill-launchpad | Supported | Not recommended | Not recommended | Not recommended | Depends on Codex desktop projects and dedicated chats |

---

## 📌 About

Songguo Skills is a collection of AI workflows I repeatedly use, organized into installable, reviewable, and shareable Skills.

It prioritizes real usage over catalog size. Each Skill should clearly explain what it is for, what it is not for, and how to trigger it.

This repository will gradually collect AI Skills that are useful, reusable, and suitable for public sharing.

To share one Skill, send its direct install link. To share the whole collection, send this repository homepage.

MIT License. You can use, modify, and redistribute these Skills freely.
