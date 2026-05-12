# Uptime Kuma Migrator

CLI script that imports monitors into Uptime Kuma from three sources: UptimeRobot API, a local JSON file, or a remote JSON URL.

## Features

- Import from **UptimeRobot** (paginated API), **local JSON**, or **remote JSON URL**
- Supports HTTP(s), Ping, Keyword, and Port monitor types
- Skips duplicate monitors (by name)
- Optionally skips paused monitors
- Optionally wipes all existing Uptime Kuma monitors before import (with confirmation prompt)

## Installation

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
```

Fill in `.env` with your credentials (see [Environment Variables](#environment-variables) below).

## Usage

Choose an import source by editing `app.py` — uncomment the desired importer:

```python
# Remote JSON (default):
importer = RemoteJsonImporter(api_client)

# Local JSON file (json_data/domains.json):
# importer = JsonImporter(api_client)

# UptimeRobot API:
# importer = UptimeRobotImporter(api_client)
```

Then run:

```bash
python app.py
```

If `CLEAN_EXISTING_MONITORS=TRUE`, the script will ask for confirmation before deleting any data.

## Environment Variables

| Variable | Required for | Description |
|---|---|---|
| `UPTIME_API_URL` | All | WebSocket URL of Uptime Kuma (e.g. `http://127.0.0.1:3001`) |
| `UPTIMEKUMA_USERNAME` | All | Uptime Kuma username |
| `UPTIMEKUMA_PASSWORD` | All | Uptime Kuma password |
| `CLEAN_EXISTING_MONITORS` | All | `TRUE`/`FALSE` — delete all monitors before import |
| `SKIP_PAUSED_MONITORS` | All | `TRUE`/`FALSE` — skip monitors with status paused |
| `EXPIRE_NOTIFICATION` | All | `0` or `1` — SSL expiry notifications on HTTP monitors |
| `MONITOR_INTERVAL` | JSON / Remote JSON | Check interval in seconds (default `20`) |
| `REMOTE_JSON_URL` | RemoteJsonImporter | URL returning `[{"domain": "..."}]` JSON |
| `UPTIMEROBOT_URL` | UptimeRobotImporter | UptimeRobot API endpoint |
| `UPTIMEROBOT_API_KEY` | UptimeRobotImporter | UptimeRobot API key |
| `UPTIMEROBOT_OFFSET` | UptimeRobotImporter | Pagination start offset (usually `0`) |

## Import Sources

### Remote JSON (`RemoteJsonImporter`)

Fetches a JSON array from `REMOTE_JSON_URL`. Expected format:

```json
[
  {"domain": "example.com"},
  {"domain": "another.com"}
]
```

Each domain is imported as an HTTP monitor with `https://` prepended.

### Local JSON (`JsonImporter`)

Same format as above, read from `json_data/domains.json`.

### UptimeRobot (`UptimeRobotImporter`)

Paginates the UptimeRobot v2 API and maps monitor types:

| UptimeRobot type | Uptime Kuma type |
|---|---|
| 1 — HTTP | HTTP |
| 2 — Keyword | Keyword |
| 3 — Ping | Ping |
| 4 — Port | Port |

## License

Released under the [MIT License](LICENSE).
