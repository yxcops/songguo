# Changelog

## v1.2 - 2026-06-22

### Changed

- 推荐前的事实核验从“尽量核对”升级为硬规则：能联网或能查资料时，必须核对作者、原书名、译者或版本、出版社、出版日期和可获得性。
- 每本推荐书新增核验来源、未核验原因、质量依据和质量风险字段。
- 推荐质量判断增加豆瓣、Goodreads、出版社页、图书馆目录、课程书单、可靠书评、奖项、引用情况或长期读者口碑等信号；评分不能作为唯一理由。
- `context` 命令新增 `--profile-max-chars`，阅读画像默认不截断；其他文件仍按 `--max-chars` 摘要。
- 推荐上下文包新增“截断提醒”，列出被脚本截断的文件，避免阅读画像或关键依据被遗漏。

### Verified

- `SKILL.md` frontmatter 可解析。
- `agents/openai.yaml` 可解析。
- `scripts/reading_tool.py` 语法检查通过。
- 已用长阅读画像验证默认 `context` 不再截断阅读画像。
- 已用短 `--profile-max-chars` 验证截断提醒会列出被截断的阅读画像。
- 已用临时目录验证 `plan`、`init`、`start`、`note`、`context`、`recommendation-draft`、`profile-context`。

### Not Included

- 未安装到本机 Codex 可发现目录。
- 未配置自动定时任务或外部推送渠道。

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
