"""MCP server: unofficial read-only access to n-tv news via its
official RSS feeds + article pages. No key, no login. NOTE: there is
no dedicated breaking-news feed (/eilmeldungen/rss 404s), so no
breaking-news tool is offered; the Börse feed carries market NEWS,
not live quotes."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from . import domain as _dom
from . import http as _http

INSTRUCTIONS = """\
Unofficial read-only MCP server for n-tv news via n-tv's official \
RSS feeds (no key, no login): latest headlines by section, market \
news, latest videos, keyword search over the latest headlines and \
full article text. NOTE: there is no dedicated breaking-news feed, \
so no breaking-news tool is offered; the Börse feed carries market \
NEWS, not live quotes. Built by Mohammad Abbasi \
(mohammad-abbasi-sh) — https://almanibama.ir · https://mabbasi.ir \
— Germany MCP factory.\
"""

_SOURCE = "n-tv.de"
_DISCLAIMER = "Unofficial read-only data from n-tv.de RSS feeds and article pages; verify on the site before acting on it."


def _envelope() -> dict:
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": _SOURCE,
        "disclaimer": _DISCLAIMER,
    }


def _ok(payload: dict) -> str:
    return json.dumps({**_envelope(), **payload}, ensure_ascii=False)


def _err(e: Exception) -> str:
    return _ok({"error": str(e)})


mcp = FastMCP("ntv-mcp", instructions=INSTRUCTIONS)


def _feed(url: str, limit: int, extra: dict | None = None) -> str:
    lim = _dom.validate_limit(limit)
    items = _dom.parse_feed(_http.fetch_text(url))
    payload = {"total_results": len(items),
               "count": min(lim, len(items)), "items": items[:lim]}
    if extra:
        payload.update(extra)
    return _ok(payload)


@mcp.tool()
def ntv_headlines(section: str = "all", limit: int = 10) -> str:
    """Latest n-tv headlines. section: "all" or one of politik,
    wirtschaft, sport, technik, panorama, wissen, der_tag.
    limit: 1..50 (default 10)."""
    try:
        sec = _dom.validate_section(section)
        return _feed(_dom.feed_url(sec), limit, {"section": sec})
    except (_http.NtvMcpError, ValueError) as e:
        return _err(e)


@mcp.tool()
def ntv_markets(limit: int = 10) -> str:
    """Latest n-tv market NEWS from the Börse feed (news stories about
    markets — not live quotes). limit: 1..50 (default 10)."""
    try:
        return _feed(_dom.BOERSE_URL, limit)
    except (_http.NtvMcpError, ValueError) as e:
        return _err(e)


@mcp.tool()
def ntv_videos(limit: int = 10) -> str:
    """Latest n-tv videos. limit: 1..50 (default 10)."""
    try:
        return _feed(_dom.VIDEOS_URL, limit)
    except (_http.NtvMcpError, ValueError) as e:
        return _err(e)


@mcp.tool()
def ntv_search_news(query: str, limit: int = 10) -> str:
    """Keyword search over the LATEST n-tv headlines (the main feed
    holds roughly the last 50 — this is not a full-archive search).
    query: keyword or phrase. limit: 1..50 (default 10)."""
    try:
        lim = _dom.validate_limit(limit)
        q = (query or "").strip()
        if not q:
            raise ValueError("query must not be empty")
        items = _dom.parse_feed(_http.fetch_text(_dom.feed_url("all")))
        ql = q.casefold()
        hits = [i for i in items
                if ql in i["title"].casefold()
                or ql in i["description"].casefold()]
    except (_http.NtvMcpError, ValueError) as e:
        return _err(e)
    return _ok({"query": q, "searched": "latest headlines in the n-tv main feed",
                "total_results": len(hits),
                "count": min(lim, len(hits)), "items": hits[:lim]})


@mcp.tool()
def ntv_get_article(url: str) -> str:
    """Full text of one n-tv article. url: an n-tv.de article link, e.g.
    https://www.n-tv.de/politik/...-id31518724.html (video pages may
    return little or no body text)."""
    try:
        u = (url or "").strip()
        if not u.startswith("https://www.n-tv.de/"):
            raise ValueError("url must be an n-tv.de article link "
                             "(https://www.n-tv.de/...)")
        out = _dom.parse_article(_http.fetch_text(u))
        if not out["headline"] and not out["body"]:
            raise ValueError("no article content found at that URL "
                             "(it may be a video or topic page)")
    except (_http.NtvMcpError, ValueError) as e:
        return _err(e)
    return _ok({"url": u, "headline": out["headline"],
                "published": out["published"],
                "body": out["body"][:6000]})


@mcp.tool()
def ntv_health() -> str:
    """Check whether n-tv.de is reachable right now.

    Returns status ok (HTTP 200), blocked (HTTP 403/429 — bot wall or
    rate limit) or error, plus the HTTP status and the probed URL.
    One polite request; it does not fetch any listings."""
    return _ok(_http.health_check())


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    sys.exit(main())
