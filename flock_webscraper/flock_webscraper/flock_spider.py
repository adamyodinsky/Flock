"""Flock Spider"""

import os
import re

from parsel import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from distutils.util import strtobool


class FlockSpider(CrawlSpider):
    name = os.environ.get("SCRAPER_NAME", "flock_spider")
    start_urls = os.environ.get("SCRAPER_START_URLS", "").split()
    output_dir = os.environ.get("SCRAPER_OUTPUT_DIR", "output")
    
    # Arguments for LinkExtractor Rule
    allowed_domains = os.environ.get("RULE_SCRAPER_ALLOWED_DOMAINS", "").split()
    deny_extensions = os.environ.get("RULE_SCRAPER_DENY_EXTENSIONS", "").split()
    allow = os.environ.get("RULE_SCRAPER_ALLOW", "").split()
    deny = os.environ.get("RULE_SCRAPER_DENY", "").split()
    restrict_xpaths = os.environ.get("RULE_SCRAPER_RESTRICT_XPATHS", "").split()
    tags = os.environ.get("RULE_SCRAPER_TAGS", "").split()
    attrs = os.environ.get("RULE_SCRAPER_ATTRS", "").split()
    restrict_css = os.environ.get("RULE_SCRAPER_RESTRICT_CSS", "").split()
    restrict_text = os.environ.get("RULE_SCRAPER_RESTRICT_TEXT", "").split()
    canonicalize = strtobool(os.environ.get("RULE_SCRAPER_CANONICALIZE", "False"))
    unique = strtobool(os.environ.get("RULE_SCRAPER_UNIQUE", "True"))
    strip = strtobool(os.environ.get("RULE_SCRAPER_STRIP", "True"))
    

    # Overrides default settings, usually in the settings.py file
    custom_settings = {
        "FEED_URI": f'{output_dir}/%(name)s/%(batch_id)s.json',
        "DOWNLOAD_DELAY": os.environ.get("SCRAPER_DOWNLOAD_DELAY", 1),
        "FEED_EXPORT_ENCODING": os.environ.get("SCRAPER_FEED_EXPORT_ENCODING", "utf-8"),
        "FEED_FORMAT": os.environ.get("SCRAPER_FEED_FORMAT", "json"),
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": os.environ.get(
            "SCRAPER_REQUEST_FINGERPRINTER_IMPLEMENTATION", "2.7"),
        "TWISTED_REACTOR": os.environ.get(
            "SCRAPER_TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

        ),
        "FEED_EXPORT_BATCH_ITEM_COUNT": os.environ.get(
            "SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT", 10
        ),
    }

    rules = (
        Rule(LinkExtractor(allow=allow, deny=deny, allow_domains=allowed_domains,  deny_extensions=deny_extensions), callback='parse_item', follow=True),
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
