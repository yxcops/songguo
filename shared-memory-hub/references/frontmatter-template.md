# 属性字段模板

每个新生成的笔记都应该包含以下 6 个字段。

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

## 字段含义

`source_platform`
这条内容的原始来源。它回答“这条经验最初来自谁”，不是“这次由谁整理入库”。常见值：`Codex`、`Hermes`、`Claude Code`、`User`、`Mixed`。

`source_device`
原始来源发生时所在的设备。常见值：`Mac mini`、`MacBook Pro`、`Windows desktop`。

`source_type`
内容类型。常见值：`聊天摘要`、`候选记忆`、`可复用经验`、`核心规则`、`项目资料`、`模板`。

`created_at`
创建时间。推荐格式：`YYYY-MM-DD HH:MM`。

`status`
当前状态。常见值：`已整理`、`待用户确认`、`已确认`、`待验证`、`已归档`。

`applies_to`
适用对象，可以是智能体、工具、项目或场景。

## 规则

- 候选记忆升级为正式经验时，优先继承原候选的 `source_platform` 和 `source_device`。
- 如果 Codex 只是把 Hermes 产生的候选升级为正式经验，`source_platform` 仍应写 `Hermes`。
- 如果一条经验由多个平台共同产生，且无法明确拆分，`source_platform` 写 `Mixed`。
- 整理者、审阅者、升级者可以写在正文说明里，不要用它们覆盖 `source_platform`。
- `applies_to` 只表示适用对象；一条内容可以来源于 Hermes，同时适用于 Codex、Hermes 或 Obsidian。
- 不要把飞书、微信等渠道写成额外 YAML 字段。渠道可以写在文件名或正文中。
- 不要默认添加 tags，除非用户明确要求。
- 不要写入密码、Token、Cookie、账号恢复码或未脱敏的敏感配置。

## 示例

Hermes 候选记忆由 Codex 审阅后升级为正式经验：

```yaml
---
source_platform: Hermes
source_device: Mac mini
source_type: 可复用经验
created_at: 2026-06-22 12:00
status: 已确认
applies_to:
  - Hermes
  - Obsidian
---
```

正文中可以补充：

```text
整理说明：本条由 Codex 根据 Hermes 候选记忆整理为正式经验。
```
