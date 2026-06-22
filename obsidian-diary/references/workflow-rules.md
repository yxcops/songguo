# Diary Workflow Rules

## Intent Routing

Treat the user's wording as the source of truth.

### Today

Use today's file when the user says:

- 写个日记
- 记个日记
- 记到日记
- 今天日记
- 帮我记录一下今天

Important boundary: if the user says "写个日记，昨天..." this is still a current-day diary entry. The word "昨天" is part of the story, not a date-routing command.

### Backfill

Use backfill only when the user says:

- 补写
- 补记
- 补一篇历史日记
- 导入旧日记

Backfill needs a target date. If the date is missing, ask for it. Do not infer.

### Historical Import

For older diaries:

1. calculate the exact date, weekday, month folder, and file name;
2. create the file if it does not exist;
3. keep the original text;
4. write under `## 补写`;
5. do not add a fake real-time callout.

## Image and Attachment Appending

Only append an image when the user explicitly says it belongs in the diary.

If the current platform can track a conversation or channel, a practical rule is:

- same conversation or channel;
- near the diary request;
- user wording clearly links the image to the diary.

If any of these are unclear, ask which date or entry the image belongs to.

## Reading Existing Diaries

Read only the date or file needed for the current task.

Do not scan the whole diary vault unless the user asks for a broad audit, migration, export, or cleanup.

## Conflict Handling

If the target file already exists:

- append new current-day entries as a new callout;
- append historical backfill under a new `## 补写` block when needed;
- do not overwrite existing diary text;
- if the file format is unusual, report the difference before changing it.

## Finishing Criteria

A diary task is complete only after checking:

- the target path is correct;
- the date and weekday match;
- the content landed in the intended file;
- the write mode matches the user's intent;
- no unauthorized diary files were read or modified.
