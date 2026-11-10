# ntv-mcp 📺

mcp-name: io.github.mohammad-abbasi-sh/ntv-mcp

سرور MCP غیررسمی و **فقط‌خواندنی** برای **[n-tv.de](https://www.n-tv.de)** — اخبار n-tv از فیدهای RSS رسمی: تازه‌ترین تیترها بر اساس بخش، اخبار بازار، تازه‌ترین ویدیوها، جست‌وجوی کلیدواژه و متن کامل مقاله. بدون کلید، بدون ورود. بدون کلید، بدون ورود.

> ساختهٔ محمد عباسی، بخشی از «کارخانهٔ MCP آلمان». وابسته به n-tv.de نیست.

## برای ایجنت‌های هوش مصنوعی

به پیکربندی MCP کلاینت اضافه کنید (stdio):

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

یا به‌صورت محلی اجرا کنید: `python -m ntv_mcp.server` (نیازمند `mcp<2` و `httpx`).

## ابزارها

| ابزار | توضیح |
|------|-------|
| `ntv_headlines` | تازه‌ترین تیترهای n-tv بر اساس بخش |
| `ntv_markets` | تازه‌ترین اخبار بازار n-tv |
| `ntv_videos` | تازه‌ترین ویدیوهای n-tv |
| `ntv_search_news` | جست‌وجوی تیترهای اخیر n-tv با کلیدواژه |
| `ntv_get_article` | متن کامل یک مقالهٔ n-tv |
| `ntv_health` | بررسی دسترس‌پذیری (ok / blocked / error) — یک درخواست مؤدبانه |

## توسعه

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## لایسنس

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
