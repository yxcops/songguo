# Changelog

## v1.0 - 2026-06-22

### Added

- Created the first public `obsidian-diary` Skill.
- Added rules for current-day diary entries, explicit historical backfill, image attachment boundaries, export, and format checks.
- Added `scripts/diary_tool.py` for local-only writing, backfilling, checking, and exporting.
- Added reference docs for Obsidian diary format, workflow routing, and privacy/configuration.
- Added a settings example template without private values.

### Verified

- Skill structure validation passed with the official quick validator.
- Script syntax check passed.
- Representative temporary-vault flows passed: current-day entry, explicit backfill, missing-date backfill rejection, diary check, and export.
- Sensitive-info scan passed for private paths, IDs, and secret assignment patterns.

### Not Included

- No real diary content.
- No private Obsidian path.
- No Hermes runtime configuration.
- No tokens, cookies, channel IDs, or API keys.
