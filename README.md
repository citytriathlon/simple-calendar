# Simple Calendar

A small web app that displays events from an ICS feed as a single searchable page.
It polls the feed in the background, groups events by day, highlights whatever is
running right now, and scrolls to it on load. Built with Flask, shipped as a Docker
image.

## Running with Docker

```bash
docker run -d \
  --name simple-calendar \
  -p 5000:5000 \
  -e ICS_URL="https://example.com/calendar.ics" \
  ghcr.io/citytriathlon/simple-calendar:latest
```

Then open <http://localhost:5000>.

### With docker compose

Copy `.env.example` to `.env`, set `ICS_URL`, and run:

```bash
docker compose up -d
```

## Configuration

All configuration is via environment variables.

| Variable           | Required | Default         | Description                                                              |
| ------------------ | -------- | --------------- | ------------------------------------------------------------------------ |
| `ICS_URL`          | yes      | –               | URL of the ICS feed to display. The app refuses to start without it.      |
| `APP_LANG`         | no       | `en`            | UI language: `en` or `ctt` (Czech). See `app/i18n.py`.                    |
| `TIMEZONE`         | no       | `Europe/Prague` | IANA timezone used to render event times.                                 |
| `ORGANIZER_DOMAIN` | no       | *(unset)*       | Organizer addresses on this domain render as `First L.` instead of email. |
| `UPDATE_INTERVAL`  | no       | `60`            | Seconds between feed refreshes.                                           |
| `FETCH_TIMEOUT`    | no       | `30`            | HTTP timeout in seconds when fetching the feed.                           |
| `LOG_LEVEL`        | no       | `INFO`          | `DEBUG`, `INFO`, `WARNING`, or `ERROR`.                                   |

## Endpoints

| Path      | Description                                                                            |
| --------- | -------------------------------------------------------------------------------------- |
| `/`       | The calendar page.                                                                      |
| `/health` | Feed freshness. `200` while healthy or starting up, `503` once the feed has gone stale. |

`/health` reports the age of the last *successful* fetch, so a feed that has been
failing for hours is distinguishable from a healthy one — the page itself keeps
serving the last known good data rather than blanking.

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

ICS_URL="https://example.com/calendar.ics" python app/app.py
```

This runs the Flask development server on port 5000. Production uses gunicorn via
`app/wsgi.py`.

Run the checks:

```bash
ruff check .
ruff format --check .
pytest -q
```

## Notes

- The app has no authentication. It serves the full contents of whatever calendar you
  point it at, so put it behind a proxy or access control if the feed is not public.
- Event descriptions are HTML-escaped; newlines are preserved with CSS. Do not
  reintroduce `{% autoescape off %}` — feed content is untrusted.
- `ics` 0.7.x does not expand `RRULE`, so recurring events may only appear at their
  first occurrence.

## License

MIT — see [LICENSE](LICENSE).
