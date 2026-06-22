# Changelog

## v1.4 - 2026-06-22

### Changed

- 新增 `书目索引.md`，用于记录想读、在读、暂停、已读和放弃。
- `start --book` 创建或复用读书笔记时，同步把书目状态标记为在读。
- 新增 `want`、`pause`、`resume`、`finish`、`abandon` 和 `profile-reviewed` 命令，用于管理读书生命周期。
- `note` 写入笔记后会把对应书目标记为“画像待审视”，但不直接改写稳定阅读画像。
- `context` 推荐上下文包新增书目索引读取，用于推荐前检查已读、在读、暂停、放弃和画像待审视书目。
- 更新 `SKILL.md`、平台接入说明、笔记与推荐格式、阅读画像模板、每周推荐模板和 OpenAI 展示文案。

### Verified

- `SKILL.md` frontmatter 可解析。
- `agents/openai.yaml` 可解析。
- `scripts/reading_tool.py` 语法检查通过。
- 官方 Skill 校验通过。
- 已用临时目录验证 `plan`、`init`、`want`、`start`、`note`、`pause`、`resume`、`finish`、`profile-reviewed`、`context` 和 `recommendation-draft`。
- 已确认 `context` 推荐上下文包包含 `书目索引.md`。

### Not Included

- 未安装到本机 Codex 可发现目录。
- 未同步到 Hermes 本机运行版。
- 未配置自动定时任务、外部推送渠道或微信读书自动读取。

## v1.3 - 2026-06-22

### Changed

- 每周推荐书单标题、文件名和 frontmatter 改用周一到周日的自然周日期范围，例如 `2026年6月22日~6月28日`。
- `recommendation-draft` 和兼容旧命令 `recommendation` 新增 `--start-date` 参数，可传入自然周内任一天并自动换算为周一到周日。
- 保留旧参数 `--week 2026-W26` 作为兼容入口，但输出仍使用自然周日期范围。
- 每周推荐模板 frontmatter 从 `week` 改为 `period`、`start_date` 和 `end_date`。

### Verified

- 已验证 `--start-date 2026-06-22` 生成 `2026年6月22日~6月28日 每周推荐书单.md`。
- 已验证兼容旧参数 `--week 2026-W26` 也生成同样的自然周日期范围。
- 已验证传入周中日期 `--start-date 2026-06-24` 会自动归到 `2026年6月22日~6月28日`。

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
