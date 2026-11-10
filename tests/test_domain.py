"""Offline tests — parse real captured n-tv RSS feeds + a structural article
fixture, no network."""
import json
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from ntv_mcp import domain as dom
from ntv_mcp import server as srv

FIX = pathlib.Path(__file__).resolve().parent / "fixtures"


def _read(name):
    return (FIX / name).read_text(encoding="utf-8")


class TestSections(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(dom.validate_section("all"), "all")
        self.assertEqual(dom.validate_section("Politik"), "politik")
        self.assertEqual(dom.validate_section("  der_tag "), "der_tag")

    def test_invalid(self):
        for bad in ["", "news", "eilmeldungen", "boerse"]:
            with self.assertRaises(ValueError, msg=bad):
                dom.validate_section(bad)

    def test_feed_urls(self):
        self.assertEqual(dom.feed_url("all"), "https://www.n-tv.de/rss")
        self.assertEqual(dom.feed_url("sport"), "https://www.n-tv.de/sport/rss")

    def test_limit(self):
        self.assertEqual(dom.validate_limit(10), 10)
        with self.assertRaises(ValueError):
            dom.validate_limit(0)
        with self.assertRaises(ValueError):
            dom.validate_limit(51)


class TestFixtures(unittest.TestCase):
    def test_feed_main(self):
        items = dom.parse_feed(_read("feed-main.xml"))
        self.assertEqual(len(items), 50)
        self.assertTrue(all(i["title"] and i["url"] and i["published"] for i in items))
        self.assertTrue(all(i["category"] for i in items))

    def test_feed_politik(self):
        items = dom.parse_feed(_read("feed-politik.xml"))
        self.assertEqual(len(items), 30)
        self.assertTrue(all(i["category"] == "Politik" for i in items))

    def test_feed_boerse(self):
        items = dom.parse_feed(_read("feed-boerse.xml"))
        self.assertEqual(len(items), 30)

    def test_feed_videos(self):
        items = dom.parse_feed(_read("feed-videos.xml"))
        self.assertEqual(len(items), 30)
        self.assertTrue(all("/mediathek/videos/" in i["url"] for i in items))

    def test_article_fixture(self):
        out = dom.parse_article(_read("article-de.html"))
        self.assertEqual(out["headline"], "Test-Schlagzeile über Deutschland")
        self.assertEqual(out["published"], "2026-11-10T19:02:24+01:00")
        self.assertTrue(out["body"].startswith(
            "Der erste Absatz des Artikeltexts beginnt hier"))
        self.assertNotIn("Ressorts", out["body"])
        self.assertIn("zweite Absatz", out["body"])

    def test_bad_feed(self):
        with self.assertRaises(ValueError):
            dom.parse_feed("<rss><unclosed")


class TestServerOffline(unittest.TestCase):
    def test_headlines_mock(self):
        with mock.patch("ntv_mcp.http.fetch_text",
                        return_value=_read("feed-main.xml")):
            out = json.loads(srv.ntv_headlines("all", limit=3))
        self.assertEqual(out["section"], "all")
        self.assertEqual(out["total_results"], 50)
        self.assertEqual(out["count"], 3)
        self.assertIn("fetched_at", out)
        self.assertEqual(out["source"], "n-tv.de")

    def test_search_mock(self):
        with mock.patch("ntv_mcp.http.fetch_text",
                        return_value=_read("feed-main.xml")):
            out = json.loads(srv.ntv_search_news("Kreml", limit=5))
        self.assertGreaterEqual(out["total_results"], 1)
        self.assertTrue(all("kreml" in (i["title"] + i["description"]).casefold()
                            for i in out["items"]))

    def test_bad_section(self):
        out = json.loads(srv.ntv_headlines("news", limit=3))
        self.assertIn("error", out)

    def test_get_article_mock(self):
        with mock.patch("ntv_mcp.http.fetch_text",
                        return_value=_read("article-de.html")):
            out = json.loads(srv.ntv_get_article(
                "https://www.n-tv.de/politik/test-article-id31500000.html"))
        self.assertEqual(out["headline"], "Test-Schlagzeile über Deutschland")
        self.assertIn("zweite Absatz", out["body"])

    def test_get_article_bad_url(self):
        out = json.loads(srv.ntv_get_article("https://example.com/x"))
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
