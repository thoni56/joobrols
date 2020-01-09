import unittest
from joobrols import Link, Links

class LinkTests(unittest.TestCase):
    def test_link_has_fields(self):
        link = Link("some path")
        self.assertEquals(link.path, "some path")
        self.assertFalse(link.scraped)
        self.assertFalse(link.broken)

class LinksTests(unittest.TestCase):
    def test_links_has_fields(self):
        links = Links("https://responsive.se")
        self.assertEquals(links.links, [])
        self.assertEquals(links.base_url, "https://responsive.se")

    def test_links_has_length(self):
        links = Links("")
        self.assertEquals(links.length(), 0)
        
    def test_links_can_append_link(self):
        links = Links("")
        self.assertEquals(links.length(), 0)
        links.append("some link")
        self.assertEquals(links.length(), 1)

    def test_links_will_not_append_link_twice(self):
        links = Links("")
        self.assertEquals(links.length(), 0)
        links.append("some link")
        self.assertEquals(links.length(), 1)
        links.append("some link")
        self.assertEquals(links.length(), 1)

    def test_can_get_path(self):
        links = Links("")
        links.append("some path")
        self.assertIsNone(links.get("some other path"))
        self.assertEquals(links.get("some path").path, "some path")

