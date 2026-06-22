# Obsidian Diary Format

This reference defines the portable diary layout used by `obsidian-diary`.

## Folder Layout

Default root:

```text
日记本/
```

Default month folder:

```text
YYYY-MM
```

Default date file:

```text
YYYY年M月D日，星期X.md
```

Example:

```text
日记本/2026-06/2026年6月22日，星期一.md
```

Use the real weekday for the target date. If the weekday and date conflict, fix the file name before writing.

## First Line

Keep the first line for the lunar date or a clear placeholder:

```markdown
农历：五月初八
```

If lunar calculation is unavailable, use:

```markdown
农历：未配置
```

Do not block diary writing only because lunar calculation is unavailable. The user can fill this line later.

## Current-Day Entry

Use an Obsidian callout with the current write time:

```markdown
农历：未配置

> [!NOTE] 14:30
> 今天整理了日记本规则。
```

Current-day entries may have multiple callouts in one file.

## Backfilled Entry

Backfilled or imported old diary text uses a section heading, not a current-time callout:

```markdown
农历：未配置

## 补写

这是旧日记原文。
```

The reason is simple: a historical entry is not written at that old moment. Do not fake a timestamp.

## Images

Use regular Obsidian embeds:

```markdown
![[image-name.png]]
```

If the platform only has a Markdown link, keep the link:

```markdown
![caption](path-or-url.png)
```

Do not move image files unless the user asks for an attachment organization workflow.

## Export

When exporting for reading or sharing:

- remove the lunar first line if the user does not need it;
- convert callout body lines by removing `> `;
- keep `## 补写` when it is meaningful;
- do not rewrite the user's diary text.
