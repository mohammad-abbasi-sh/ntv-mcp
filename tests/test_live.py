"""Live tests — hit the real n-tv.de RSS feeds + one article. Cautious: few requests.

Run:  pytest tests/test_live.py -v
Skip: pytest -m "not live"  (or set NTV_SKIP_LIVE=1)
"""
import json
import os
import pathlib
import sys
import unittest

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from ntv_mcp import server as srv

pytestmark = pytest.mark.live
SKIP = os.environ.get("NTV_SKIP_LIVE") == "1"


@pytest.mark.skipif(SKIP, reason="NTV_SKIP_LIVE=1")
class TestLive(unittest.TestCase):
    def test_headlines_live(self):
        out = json.loads(srv.ntv_headlines("all", limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)
        print(f"\nLIVE headlines: {out['total_results']} — {out['items'][0]['title'][:60]}")

    def test_section_live(self):
        out = json.loads(srv.ntv_headlines("wirtschaft", limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)

    def test_markets_live(self):
        out = json.loads(srv.ntv_markets(limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)
        print(f"\nLIVE markets: {out['total_results']} — {out['items'][0]['title'][:60]}")

    def test_videos_live(self):
        out = json.loads(srv.ntv_videos(limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)

    def test_search_live(self):
        out = json.loads(srv.ntv_search_news("SPD", limit=3))
        self.assertNotIn("error", out)
        print(f"\nLIVE search 'SPD': {out['total_results']} hits")

    def test_get_article_live(self):
        out = json.loads(srv.ntv_get_article(
            "https://www.n-tv.de/politik/SPD-will-Bleiberecht-fuer-arbeitende-Gefluechtete-id31518724.html"))
        self.assertNotIn("error", out)
        self.assertTrue(out["headline"])
        self.assertGreater(len(out["body"]), 500)
        print(f"\nLIVE article: {out['headline'][:70]} — body {len(out['body'])} chars")

    def test_health_live(self):
        out = json.loads(srv.ntv_health())
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["http_status"], 200)
