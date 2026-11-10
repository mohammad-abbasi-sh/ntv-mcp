"""Domain logic: shape n-tv RSS feeds + article HTML into compact dicts
(stdlib only).

Data source: n-tv's official RSS feeds (https://www.n-tv.de/rss and
per-section /{section}/rss, /wirtschaft/boerse/rss,
/mediathek/videos/rss) and n-tv.de article pages — free, no key, no
login. There is NO dedicated breaking-news feed (/eilmeldungen/rss
404s, verified 2026-11-10), so no breaking-news tool is offered.
"""
from __future__ import annotations

import html as _html
import json
import re
import xml.etree.ElementTree as ET

BASE = "https://www.n-tv.de"

SECTIONS = {
    "all", "politik", "wirtschaft", "sport", "technik", "panorama",
    "wissen", "der_tag",
}

_LD_RE = re.compile(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', re.S)
_P_RE = re.compile(r'<p[^>]*>(.*?)</p>', re.S)
_TAG_RE = re.compile(r'<[^>]+>')


def validate_section(section: str) -> str:
    key = (section or "").strip().lower()
    if key not in SECTIONS:
        raise ValueError(
            f"unsupported section: {section!r} "
            f"(use one of: {', '.join(sorted(SECTIONS))})"
        )
    return key


def validate_limit(limit: int) -> int:
    if not 1 <= limit <= 50:
        raise ValueError(f"limit out of range: {limit} (expected 1..50)")
    return limit


def feed_url(section: str) -> str:
    if section == "all":
        return f"{BASE}/rss"
    return f"{BASE}/{section}/rss"


BOERSE_URL = f"{BASE}/wirtschaft/boerse/rss"
VIDEOS_URL = f"{BASE}/mediathek/videos/rss"


def _parse_xml(text: str, what: str) -> ET.Element:
    try:
        return ET.fromstring(text)
    except ET.ParseError as e:
        raise ValueError(f"invalid {what}: {e}") from e


def parse_feed(text: str) -> list[dict]:
    """[{title, url, published, description, category}] — feed order."""
    root = _parse_xml(text, "RSS feed")
    channel = root.find("channel")
    if channel is None:
        raise ValueError("invalid RSS feed: no channel element")
    out = []
    for item in channel.findall("item"):
        out.append({
            "title": item.findtext("title") or "",
            "url": item.findtext("link") or item.findtext("guid") or "",
            "published": item.findtext("pubDate") or "",
            "description": (item.findtext("description") or "").strip(),
            "category": item.findtext("category") or "",
        })
    return out


def parse_article(html_text: str) -> dict:
    """Extract headline/date (JSON-LD NewsArticle) + cleaned body <p>s.

    n-tv article pages are server-rendered: the body is plain <p>
    tags. The first <p> is navigation junk (starts with "Ressorts")
    and is dropped. JSON-LD articleBody is empty (verified 2026-11-10).
    """
    headline, published = "", ""
    for m in _LD_RE.finditer(html_text):
        try:
            ld = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(ld, dict) and ld.get("@type") == "NewsArticle":
            headline = ld.get("headline") or ""
            published = ld.get("datePublished") or ""
            break
    paras = []
    for raw in _P_RE.findall(html_text):
        txt = _html.unescape(_TAG_RE.sub("", raw)).replace("\u00a0", " ").strip()
        if not txt:
            continue
        if txt.startswith("Ressorts"):
            continue
        paras.append(txt)
    return {"headline": headline, "published": published,
            "body": "\n\n".join(paras)}
