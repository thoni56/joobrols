import unittest
from joobrols import Link, Links

class LinkTests(unittest.TestCase):
    def test_link_has_fields(self):
        link = Link("some url")
        self.assertEquals(link.url, "some url")
        self.assertFalse(link.scraped)

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