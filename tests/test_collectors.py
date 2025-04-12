import unittest
from collectors.api_collector import APICollector
from collectors.scrapper_collector import ScrapperCollector


class TestCollectors(unittest.TestCase):
    def test_api_collector(self):
        collector = APICollector()
        self.assertTrue(hasattr(collector, "collect_data"))

    def test_scrapper_collector(self):
        collector = ScrapperCollector()
        self.assertTrue(hasattr(collector, "collect_data"))


if __name__ == "__main__":
    unittest.main()
