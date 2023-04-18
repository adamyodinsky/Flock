from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from parsel import Selector
import re


class FlockSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = kwargs.get("name")
        self.start_urls: list[str] = kwargs.get("start_urls", [])
        self.allowed_domains:list(str) = kwargs.get("allowed_domains", [])
        self.deny_extensions: list(str) = kwargs.get("deny_extensions", [])
        self.custom_settings: list(str) = kwargs.get("custom_settings", {})
        self.rules = Rule(
            LinkExtractor(
                allow_domains=self.allowed_domains, deny_extensions=self.deny_extensions
            ),
            callback="parse_item",
            follow=True,
        )

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
