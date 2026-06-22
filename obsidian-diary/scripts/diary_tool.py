#!/usr/bin/env python3
"""Small helper for Obsidian diary files.

The script intentionally stays local-only. It does not read platform logs,
chat history, network resources, or private configs unless the caller passes
an explicit vault path.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable


WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
TODAY_TRIGGERS = [
    "写个日记",
    "写一篇日记",
    "记个日记",
    "记一条日记",
    "记到日记",
    "今天日记",
    "帮我记录一下今天",
]
BACKFILL_TRIGGERS = ["补写", "补记", "补一篇历史日记", "导入旧日记", "旧日记"]


@dataclass
class DiaryResult:
    path: Path
    mode: str
    diary_date: date
    text: str

    def to_dict(self) -> dict[str, str]:
        return {
            "path": str(self.path),
            "mode": self.mode,
            "date": self.diary_date.isoformat(),
            "text": self.text,
        }


def parse_now(raw: str | None) -> datetime:
    if not raw:
        return datetime.now()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(raw, fmt)
            if fmt == "%Y-%m-%d":
                return datetime.combine(parsed.date(), datetime.min.time())
            return parsed
        except ValueError:
            continue
    raise SystemExit(f"Unsupported --now value: {raw}")


def resolve_vault(raw: str | None) -> Path:
    value = raw or os.environ.get("OBSIDIAN_DIARY_VAULT")
    if not value:
        raise SystemExit("Missing --vault or OBSIDIAN_DIARY_VAULT.")
    return Path(value).expanduser().resolve()


def diary_root(vault: Path, raw_root: str | None) -> Path:
    root_name = raw_root or os.environ.get("OBSIDIAN_DIARY_ROOT") or "日记本"
    root = Path(root_name).expanduser()
    if root.is_absolute():
        return root.resolve()
    return (vault / root).resolve()


def diary_path(root: Path, target_date: date) -> Path:
    month_dir = root / f"{target_date.year}-{target_date.month:02d}"
    filename = f"{target_date.year}年{target_date.month}月{target_date.day}日，{WEEKDAYS[target_date.weekday()]}.md"
    return month_dir / filename


def lunar_line(_: date) -> str:
    try:
        from lunardate import LunarDate  # type: ignore
    except Exception:
        return "农历：未配置"

    lunar = LunarDate.fromSolarDate(_.year, _.month, _.day)
    months = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
    days = [
        "初一",
        "初二",
        "初三",
        "初四",
        "初五",
        "初六",
        "初七",
        "初八",
        "初九",
        "初十",
        "十一",
        "十二",
        "十三",
        "十四",
        "十五",
        "十六",
        "十七",
        "十八",
        "十九",
        "二十",
        "廿一",
        "廿二",
        "廿三",
        "廿四",
        "廿五",
        "廿六",
        "廿七",
        "廿八",
        "廿九",
        "三十",
    ]
    leap = "闰" if getattr(lunar, "isLeapMonth", False) else ""
    return f"农历：{leap}{months[lunar.month - 1]}{days[lunar.day - 1]}"


def ensure_file(path: Path, target_date: date) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(f"{lunar_line(target_date)}\n\n", encoding="utf-8")


def append_block(path: Path, block: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    prefix = ""
    if existing and not existing.endswith("\n"):
        prefix = "\n"
    if existing and not existing.endswith("\n\n"):
        prefix += "\n"
    path.write_text(existing + prefix + block.rstrip() + "\n", encoding="utf-8")


def is_backfill_intent(text: str) -> bool:
    return any(trigger in text for trigger in BACKFILL_TRIGGERS)


def strip_prefixes(text: str, prefixes: Iterable[str]) -> str:
    value = text.strip()
    changed = True
    while changed:
        changed = False
        for prefix in prefixes:
            if value.startswith(prefix):
                value = value[len(prefix) :].strip(" ，,：:")
                changed = True
    return value.strip()


def parse_date(raw: str, now: datetime) -> date | None:
    value = raw.strip()
    if value in {"今天", "今日"}:
        return now.date()
    if value == "昨天":
        return now.date() - timedelta(days=1)
    if value == "前天":
        return now.date() - timedelta(days=2)

    patterns = [
        r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})",
        r"(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})",
        r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日?",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if not match:
            continue
        return date(int(match.group("year")), int(match.group("month")), int(match.group("day")))
    return None


def strip_date_phrase(text: str) -> str:
    value = text
    value = re.sub(r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?", "", value)
    value = value.replace("日期是", "").replace("日期：", "").replace("日期:", "")
    return re.sub(r"\s+", " ", value).strip(" ，,：:")


def format_callout(now: datetime, text: str, images: list[str]) -> str:
    lines = [f"> [!NOTE] {now.strftime('%H:%M')}"]
    for image in images:
        lines.append(f"> {format_image(image)}")
    for line in text.strip().splitlines() or [""]:
        lines.append(f"> {line}".rstrip())
    return "\n".join(lines)


def format_backfill(text: str, images: list[str]) -> str:
    body: list[str] = ["## 补写", ""]
    for image in images:
        body.append(format_image(image))
    if images and text.strip():
        body.append("")
    body.extend(text.strip().splitlines() or [""])
    return "\n".join(body)


def format_image(raw: str) -> str:
    image = raw.strip()
    if image.startswith("![") or image.startswith("![["):
        return image
    name = Path(image).name
    return f"![[{name}]]"


def write_today(root: Path, now: datetime, text: str, images: list[str]) -> DiaryResult:
    cleaned = strip_prefixes(text, TODAY_TRIGGERS)
    if not cleaned and not images:
        raise SystemExit("Empty diary text.")
    path = diary_path(root, now.date())
    ensure_file(path, now.date())
    append_block(path, format_callout(now, cleaned, images))
    return DiaryResult(path=path, mode="today", diary_date=now.date(), text=cleaned)


def write_backfill(root: Path, target_date: date, text: str, images: list[str]) -> DiaryResult:
    cleaned = strip_prefixes(strip_date_phrase(text), BACKFILL_TRIGGERS)
    if not cleaned and not images:
        raise SystemExit("Empty backfill text.")
    path = diary_path(root, target_date)
    ensure_file(path, target_date)
    append_block(path, format_backfill(cleaned, images))
    return DiaryResult(path=path, mode="backfill", diary_date=target_date, text=cleaned)


def command_record(args: argparse.Namespace) -> DiaryResult:
    vault = resolve_vault(args.vault)
    root = diary_root(vault, args.diary_root)
    now = parse_now(args.now)
    if is_backfill_intent(args.text):
        target = parse_date(args.text, now)
        if args.date:
            target = parse_date(args.date, now)
        if not target:
            raise SystemExit("Backfill intent detected, but no explicit date was found. Pass --date YYYY-MM-DD.")
        return write_backfill(root, target, args.text, args.image)
    return write_today(root, now, args.text, args.image)


def command_backfill(args: argparse.Namespace) -> DiaryResult:
    vault = resolve_vault(args.vault)
    root = diary_root(vault, args.diary_root)
    now = parse_now(args.now)
    target = parse_date(args.date, now)
    if not target:
        raise SystemExit("Backfill needs --date YYYY-MM-DD, YYYY年M月D日, 今天, 昨天, or 前天.")
    return write_backfill(root, target, args.text, args.image)


def command_info(args: argparse.Namespace) -> dict[str, str]:
    vault = resolve_vault(args.vault)
    root = diary_root(vault, args.diary_root)
    now = parse_now(args.now)
    return {
        "vault": str(vault),
        "diary_root": str(root),
        "today_path": str(diary_path(root, now.date())),
    }


def command_init(args: argparse.Namespace) -> dict[str, str]:
    vault = resolve_vault(args.vault)
    root = diary_root(vault, args.diary_root)
    root.mkdir(parents=True, exist_ok=True)
    return {"created_or_existing": str(root)}


def command_check(args: argparse.Namespace) -> dict[str, object]:
    vault = resolve_vault(args.vault)
    root = diary_root(vault, args.diary_root)
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0
    if not root.exists():
        return {"root": str(root), "checked": 0, "errors": [f"Diary root does not exist: {root}"], "warnings": []}

    pattern = re.compile(r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日，(?P<weekday>星期[一二三四五六日])\.md$")
    for path in sorted(root.rglob("*.md")):
        checked += 1
        match = pattern.match(path.name)
        if not match:
            warnings.append(f"Unexpected filename: {path}")
            continue
        target = date(int(match.group("year")), int(match.group("month")), int(match.group("day")))
        expected_month = f"{target.year}-{target.month:02d}"
        if path.parent.name != expected_month:
            errors.append(f"Month directory mismatch: {path}")
        expected_weekday = WEEKDAYS[target.weekday()]
        if match.group("weekday") != expected_weekday:
            errors.append(f"Weekday mismatch: {path.name} should use {expected_weekday}")
        text = path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if not first_line.startswith("农历："):
            warnings.append(f"Missing lunar first line: {path}")

    return {"root": str(root), "checked": checked, "errors": errors, "warnings": warnings}


def strip_export(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("农历："):
        lines = lines[1:]
    output: list[str] = []
    for line in lines:
        if line.startswith("> [!"):
            time_match = re.search(r"(\d{1,2}:\d{2})", line)
            if time_match:
                output.append(time_match.group(1))
            continue
        if line.startswith("> "):
            output.append(line[2:])
        elif line == ">":
            output.append("")
        else:
            output.append(line)
    return "\n".join(output).strip() + "\n"


def command_export(args: argparse.Namespace) -> str:
    vault = resolve_vault(args.vault)
    root = diary_root(vault, args.diary_root)
    now = parse_now(args.now)
    target = parse_date(args.date, now)
    if not target:
        raise SystemExit("Export needs --date YYYY-MM-DD, YYYY年M月D日, 今天, 昨天, or 前天.")
    path = diary_path(root, target)
    if not path.exists():
        raise SystemExit(f"Diary file not found: {path}")
    return strip_export(path.read_text(encoding="utf-8"))


def emit(value: object, json_output: bool) -> None:
    if isinstance(value, DiaryResult):
        value = value.to_dict()
    if json_output:
        print(json.dumps(value, ensure_ascii=False, indent=2))
        return
    if isinstance(value, str):
        print(value, end="" if value.endswith("\n") else "\n")
        return
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write, backfill, check, and export Obsidian diary files.")
    parser.add_argument("--vault", help="Obsidian vault path. Can also use OBSIDIAN_DIARY_VAULT.")
    parser.add_argument("--diary-root", default=None, help="Diary root folder inside the vault. Default: 日记本.")
    parser.add_argument("--now", default=None, help="Override current time for tests, e.g. 2026-06-22T14:30.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON where applicable.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("info", help="Show resolved diary paths.")
    subparsers.add_parser("init", help="Create the diary root folder if needed.")
    subparsers.add_parser("check", help="Check diary filenames, month folders, and first lines.")

    record = subparsers.add_parser("record", help="Write a current-day diary entry unless explicit backfill intent is detected.")
    record.add_argument("--text", required=True)
    record.add_argument("--date", help="Optional explicit date used only for backfill intent.")
    record.add_argument("--image", action="append", default=[], help="Image/link to add as an Obsidian embed. Can repeat.")

    backfill = subparsers.add_parser("backfill", help="Write a historical diary entry.")
    backfill.add_argument("--date", required=True)
    backfill.add_argument("--text", required=True)
    backfill.add_argument("--image", action="append", default=[], help="Image/link to add as an Obsidian embed. Can repeat.")

    export = subparsers.add_parser("export", help="Export a diary file as plain Markdown-ish text.")
    export.add_argument("--date", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        if args.command == "info":
            emit(command_info(args), args.json)
        elif args.command == "init":
            emit(command_init(args), args.json)
        elif args.command == "check":
            emit(command_check(args), args.json)
        elif args.command == "record":
            emit(command_record(args), args.json)
        elif args.command == "backfill":
            emit(command_backfill(args), args.json)
        elif args.command == "export":
            emit(command_export(args), args.json)
        else:
            raise SystemExit(f"Unknown command: {args.command}")
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
