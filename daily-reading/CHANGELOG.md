# Changelog

## v1.1 - 2026-06-22

### Changed

- 保留“开始读书”“开始读《书名》”“开始读某本书”作为进入读书模式的触发方式。
- 收紧普通读书建议和正式记录流程的边界，避免泛泛推荐书时误进入写文件流程。
- 明确 `profile-context` 只生成阅读画像资料包，`context` 只生成推荐上下文包，`recommendation-draft` 只生成每周推荐书单草稿。
- 增强阅读画像、单本书笔记和每周推荐书单模板。
- 统一推荐书单中的不确定事实标注为“不确定，需核验”。

### Verified

- `SKILL.md` frontmatter 可解析。
- `agents/openai.yaml` 可解析。
- `scripts/reading_tool.py` 语法检查通过。
- 已用临时目录验证 `plan`、`init`、`start`、`note`、`context`、`recommendation-draft`、`profile-context`。
- 已检查并清理 Python 缓存文件。

### Not Included

- 未安装到本机 Codex 可发现目录。
- 未配置自动定时任务或外部推送渠道。
- 官方 quick validate 未运行成功，原因是当前 Python 环境缺少 `yaml` 依赖；已用等效解析和代表流程测试替代验证。
