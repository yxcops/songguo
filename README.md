# songguo

这里收集我自用并逐步公开的 AI Skills。

## Skills

### shared-memory-hub

用于让 Codex、Hermes、Claude Code、OpenClaw 等智能体共用一套 Obsidian 或本地 Markdown 共享记忆库。

它支持：

- 核心规则
- 可复用经验库
- 候选确认清单
- 聊天摘要
- 项目资料
- 归档废弃

安装链接：

```text
https://github.com/yxcops/songguo/tree/main/shared-memory-hub
```

### 小松鼠配图

用于为中文文章、帖子、小红书、公众号、Notion 文档、工作流说明生成带固定小松鼠 IP 的正文配图。

它支持：

- 固定小松鼠角色参考图
- 中文正文配图策略
- 单张生图提示词
- 小红书、公众号、视频封面等比例建议
- 生成后质量检查

安装链接：

```text
https://github.com/yxcops/songguo/tree/main/xiao-songshu-peitu
```

### Codex Skill 启动台

用于把一组 Codex Skills 整理成 Codex 客户端里的可视化入口项目：每个 Skill 一个入口文件夹，每个入口一个专属对话。

它支持：

- 全局安装 Skill 后集中做可视化入口
- 新建专门启动台项目
- 放进已有 Codex 项目
- 为每个入口写 `AGENTS.md`
- 为每个 Skill 创建专属 Codex 对话
- 检查入口文件里是否混入账号、API key、token 等隐私信息

安装链接：

```text
https://github.com/yxcops/songguo/tree/main/codex-skill-launchpad
```

## shared-memory-hub 怎么启动

安装 Skill 后，它不会自动创建共享记忆库，也不会自动创建定时任务。

你可以对 AI 说：

```text
请使用 shared-memory-hub Skill，帮我创建一个 AI智能体共享记忆库。

创建前先问我保存位置。可以保存在 Obsidian 库里，也可以保存在普通本地文件夹里。

不要自动写入未确认的路径。

创建后请运行检查脚本，确认目录完整、入口文件存在、核心规则存在、没有旧目录名残留。

创建完成后，请提醒我是否继续创建自动化任务，但不要直接创建。
```

## 怎么创建自动化任务

创建共享记忆库后，可以继续对 AI 说：

```text
请使用 shared-memory-hub Skill，根据模板帮我创建两个自动化任务：

1. 每日聊天摘要整理
2. 每周候选确认审阅

创建前请先说明：
- 每个任务会读取什么
- 每个任务会写入什么
- 每个任务什么时候运行
- 哪些目录不能自动修改

等我明确确认后再创建。
```

## 小松鼠配图怎么启动

安装 Skill 后，可以对 AI 说：

```text
请使用 小松鼠配图（xiao-songshu-peitu）Skill，帮我为这篇中文内容设计 3 张小松鼠风格正文配图。

先给配图策略，不要直接生成图片。
每张图说明放在哪个段落后、表达什么、画面里小松鼠在做什么、建议比例是多少。
```

如果要直接生成图片，可以说：

```text
请使用 小松鼠配图（xiao-songshu-peitu）Skill，为这篇内容生成 1 张公众号正文配图。

请使用 Skill 里的小松鼠参考图保持角色一致。
```

## Codex Skill 启动台怎么启动

这个 Skill 只面向 Codex 客户端。它不会替你上传 GitHub，也不会自动发布内容。

安装后，可以对 Codex 说：

```text
请使用 codex-skill-launchpad Skill，把下面这些 Skill 整理成一个可视化入口项目。

要求：
1. Skill 本体全局安装。
2. 入口放到 Codex/workspaces/我的Skill启动台。
3. 每个 Skill 一个入口文件夹。
4. 每个入口写 AGENTS.md。
5. 每个 Skill 创建一个专属 Codex 对话。
6. 发布、抓取、扣费生成类入口必须默认先确认，不要直接执行。
7. 完成后检查新文件里没有账号、API key、token、cookie。

Skill 列表：
- 文章封面图：baoyu-cover-image
- 信息图：baoyu-infographic
- 发微博：baoyu-post-to-weibo
```

## 平台兼容

不同 Skill 的平台兼容范围不同：

- `shared-memory-hub` 面向 Codex、Hermes、Claude Code、OpenClaw，以及其他能读取和写入本地 Markdown 文件的 AI Agent。
- `xiao-songshu-peitu` 面向能读取 Skill 并调用图片生成能力的 AI Agent。
- `codex-skill-launchpad` 只面向 Codex 客户端，因为它依赖 Codex 的项目、文件夹入口和专属对话。

不同平台的自动化能力不一样。这些 Skill 提供规则、模板或脚本，但不会在安装后自动启动后台任务。
