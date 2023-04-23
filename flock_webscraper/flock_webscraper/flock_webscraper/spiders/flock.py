import os
import re

from parsel import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FlockSpider(CrawlSpider):

    name = os.environ.get("SCRAPER_NAME", "flock_spider")
    start_urls = list(os.environ.get("SCRAPER_START_URLS", "")).split()
    allowed_domains = os.environ.get("SCRAPER_ALLOWED_DOMAINS", "").split()
    deny_extensions = os.environ.get("SCRAPER_DENY_EXTENSIONS", "").split()
    output_dir = os.environ.get("SCRAPER_OUTPUT_DIR", "output")
    custom_settings = {
        "DOWNLOAD_DELAY": os.environ.get("SCRAPER_DOWNLOAD_DELAY", 1),
        "FEED_EXPORT_ENCODING": os.environ.get("SCRAPER_FEED_EXPORT_ENCODING", "utf-8"),
        "FEED_FORMAT": os.environ.get("SCRAPER_FEED_FORMAT", "json"),
        "FEED_URI": f'{output_dir}/%(name)s/%(batch_id)s.json',
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": os.environ.get(
            "SCRAPER_REQUEST_FINGERPRINTER_IMPLEMENTATION", "2.7"),
        "TWISTED_REACTOR": os.environ.get(
            "SCRAPER_TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

        ),
        "FEED_EXPORT_BATCH_ITEM_COUNT": os.environ.get(
            "SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT", 100
        ),
    }

    rules = Rule(
            LinkExtractor(
                allow_domains=allowed_domains, deny_extensions=deny_extensions
            ),
            callback="parse_item",
            follow=True,
        )


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.name: str = kwargs.get("name")
    #     self.start_urls: list[str] = kwargs.get("start_urls", [])
    #     self.allowed_domains:list(str) = kwargs.get("allowed_domains", [])
    #     self.deny_extensions: list(str) = kwargs.get("deny_extensions", [])
    #     self.custom_settings: list(str) = kwargs.get("custom_settings", {})

    #     self.rules = Rule(
    #         LinkExtractor(
    #             allow_domains=self.allowed_domains, deny_extensions=self.deny_extensions
    #         ),
    #         callback="parse_item",
    #         follow=True,
    #     )
        


    def parse_item(self, response):
        # Use Parsel to parse HTML and remove tags
        selector = Selector(response.text)
        cleaned_text = selector.xpath("normalize-space(//body)").get()

        # Remove any remaining tags and whitespace
        cleaned_text = re.sub("<[^>]*>", " ", cleaned_text)
        cleaned_text = re.sub("\s+", " ", cleaned_text).strip()

        yield {
            "url": response.url,
            "text": cleaned_text,
        }
