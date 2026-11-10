# ntv-mcp 📺

mcp-name: io.github.mohammad-abbasi-sh/ntv-mcp

Unofficial **read-only** MCP server for **[n-tv.de](https://www.n-tv.de)** — n-tv news from its official RSS feeds: latest headlines by section, market news, latest videos, keyword search and full article text. No key, no login. No key, no login.

> Built by Mohammad Abbasi as part of the "Germany MCP factory". Not affiliated with n-tv.de.

## For AI agents

Add to your MCP client config (stdio):

```json
{
  "mcpServers": {
    "ntv": {
      "command": "uvx",
      "args": ["ntv-mcp==0.1.0"]
    }
  }
}
```

Or run locally: `python -m ntv_mcp.server` (needs `mcp<2`, `httpx`).

## Tools

| Tool | Description |
|------|-------------|
| `ntv_headlines` | Latest n-tv headlines — `section` (all/politik/wirtschaft/sport/technik/panorama/wissen/der_tag), `limit` 1..50 |
| `ntv_markets` | Latest n-tv market news (Börse feed) — `limit` 1..50 |
| `ntv_videos` | Latest n-tv videos — `limit` 1..50 |
| `ntv_search_news` | Keyword search over the latest n-tv headlines — `query`, `limit` 1..50 |
| `ntv_get_article` | Full text of one n-tv article — `url` (an n-tv.de article link) |
| `ntv_health` | Reachability probe (ok / blocked / error) — one polite request |

## Notes

- All data comes from **n-tv's official RSS feeds** (free, no key, no login).
- There is **no dedicated breaking-news feed** — `/eilmeldungen/rss` 404s (verified 2026-11-10) — so no breaking-news tool is offered.
- The Börse feed carries market **news**, not live quotes.
- Article bodies are extracted from n-tv's server-rendered pages (JSON-LD headline/date + cleaned `<p>` text); video pages may return little or no body text.

Tests: 22/22 green (15 offline + 7 live, 2026-11-10).

## Development

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## License

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
