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
写入或沉淀这条内容的智能体或人工来源。常见值：`Codex`、`Hermes`、`Claude Code`、`User`、`Mixed`。

`source_device`
写入这条内容时所在的设备。常见值：`Mac mini`、`MacBook Pro`、`Windows desktop`。

`source_type`
内容类型。常见值：`聊天摘要`、`候选记忆`、`可复用经验`、`核心规则`、`项目资料`、`模板`。

`created_at`
创建时间。推荐格式：`YYYY-MM-DD HH:MM`。

`status`
当前状态。常见值：`已整理`、`待用户确认`、`已确认`、`待验证`、`已归档`。

`applies_to`
适用对象，可以是智能体、工具、项目或场景。

## 规则

- 不要把飞书、微信等渠道写成额外 YAML 字段。渠道可以写在文件名或正文中。
- 不要默认添加 tags，除非用户明确要求。
- 不要写入密码、Token、Cookie、账号恢复码或未脱敏的敏感配置。
