# Privacy and Configuration

`obsidian-diary` is designed for public sharing. Keep private runtime details outside the Skill.

## Do Not Publish

Do not put these into `SKILL.md`, examples, scripts, templates, screenshots, or changelogs:

- real diary text;
- real Obsidian vault paths;
- chat IDs, channel IDs, user IDs, bot IDs;
- tokens, cookies, API keys, auth headers;
- raw platform logs;
- private automation URLs;
- exact message IDs or attachment IDs from a private platform.

## Configuration

Use runtime arguments or private environment variables:

```bash
export OBSIDIAN_DIARY_VAULT="/path/to/vault"
export OBSIDIAN_DIARY_ROOT="日记本"
```

Do not commit a filled settings file. If a settings example is needed, use `templates/settings.example.yaml`.

## Platform Adapters

Codex, Hermes, Claude Code, OpenClaw, and other Agents may expose different abilities:

| Ability | If available | If unavailable |
|---|---|---|
| local file read/write | write and check diary files | output manual steps |
| shell script | run `scripts/diary_tool.py` | explain the target format |
| image attachment access | append explicit image embeds | ask the user for the path or link |
| channel state | resolve "刚才那张" carefully | ask which entry to attach |
| scheduled task | configure outside this Skill | do not claim scheduling is configured |

## Public Examples

Use synthetic examples:

```text
今天整理了日记规则。
```

Avoid examples that reveal real dates, relationships, places, work details, accounts, or identifiable life events.

## Before Publishing

Run a sensitive-info scan over the Skill directory. At minimum check for:

```text
home-directory prefixes
token or cookie assignments
API key assignments
channel or chat ID values
real private diary text
```

The scan cannot prove there is no sensitive content, but it catches the common mistakes before pushing.
