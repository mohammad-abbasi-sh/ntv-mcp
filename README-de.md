# ntv-mcp 📺

mcp-name: io.github.mohammad-abbasi-sh/ntv-mcp

Inoffizieller **nur lesender** MCP-Server für **[n-tv.de](https://www.n-tv.de)** — n-tv-Nachrichten über die offiziellen RSS-Feeds: neueste Schlagzeilen nach Ressort, Börsennachrichten, neueste Videos, Stichwortsuche und Volltexte. Kein Schlüssel, kein Login. Kein Schlüssel, keine Anmeldung.

> Gebaut von Mohammad Abbasi als Teil der "Germany MCP factory". Nicht mit n-tv.de verbunden.

## Für KI-Agenten

Zur MCP-Client-Konfiguration hinzufügen (stdio):

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

Oder lokal starten: `python -m ntv_mcp.server` (benötigt `mcp<2`, `httpx`).

## Tools

| Tool | Beschreibung |
|------|-------------|
| `ntv_headlines` | Neueste n-tv-Schlagzeilen nach Ressort |
| `ntv_markets` | Neueste n-tv-Börsennachrichten |
| `ntv_videos` | Neueste n-tv-Videos |
| `ntv_search_news` | Neueste n-tv-Schlagzeilen nach Stichwort suchen |
| `ntv_get_article` | Volltext eines n-tv-Artikels |
| `ntv_health` | Erreichbarkeitsprüfung (ok / blocked / error) — eine höfliche Anfrage |

## Entwicklung

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## Lizenz

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
