"""Flock Spider"""

import logging
import os
import re
import sys
from distutils.util import strtobool

from dotenv import find_dotenv, load_dotenv
from parsel import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

logger = logging.getLogger("scrapy")
logger.setLevel(
    os.environ.get("LOG_LEVEL", "INFO").upper()
)  # Set log level to INFO by default


class EnvVarNotSetError(Exception):
    """Raised when an environment variable is not set"""

    def __init__(self, var_name):
        self.var_name = var_name
        super().__init__(f"Environment variable '{self.var_name}' is not set")


def check_env_vars(required_vars, optional_vars=None):
    """Check that all required environment variables are set"""

    for var in required_vars:
        if var not in os.environ:
            raise EnvVarNotSetError(var)

    if optional_vars:
        for var in optional_vars:
            if var not in os.environ:
                logging.info(
                    "Warning: Optional environment variable '%s' is not set", var
                )


class FlockSpider(CrawlSpider):
    """Flock Spider"""

    # Check that all required environment variables are set
    load_dotenv(find_dotenv(os.getenv("FLOCK_ENV_FILE", ".env")))
    required_vars = []
    optional_vars = [
        "SCRAPER_NAME",
        "SCRAPER_START_URLS",
        "SCRAPER_OUTPUT_DIR",
        "RULE_SCRAPER_ALLOWED_DOMAINS",
        "RULE_SCRAPER_DENY_EXTENSIONS",
        "RULE_SCRAPER_ALLOW",
        "RULE_SCRAPER_DENY",
        "RULE_SCRAPER_RESTRICT_XPATHS",
        "RULE_SCRAPER_TAGS",
        "RULE_SCRAPER_ATTRS",
        "RULE_SCRAPER_RESTRICT_CSS",
        "RULE_SCRAPER_RESTRICT_TEXT",
        "RULE_SCRAPER_CANONICALIZE",
        "RULE_SCRAPER_UNIQUE",
        "RULE_SCRAPER_STRIP",
        "SCRAPER_DOWNLOAD_DELAY",
        "SCRAPER_FEED_EXPORT_ENCODING",
        "SCRAPER_FEED_FORMAT",
        "SCRAPER_REQUEST_FINGERPRINTER_IMPLEMENTATION",
        "SCRAPER_TWISTED_REACTOR",
        "SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT",
    ]
    try:
        check_env_vars(required_vars, optional_vars)
    except EnvVarNotSetError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    name = os.environ.get("SCRAPER_NAME", "flock_spider")
    start_urls = os.environ.get("SCRAPER_START_URLS", "").split()
    output_dir = os.environ.get("SCRAPER_OUTPUT_DIR", "output")
    print("hello")

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
        "FEED_URI": f"{output_dir}/%(name)s/%(batch_id)s.json",
        "DOWNLOAD_DELAY": os.environ.get("SCRAPER_DOWNLOAD_DELAY", 1),
        "FEED_EXPORT_ENCODING": os.environ.get("SCRAPER_FEED_EXPORT_ENCODING", "utf-8"),
        "FEED_FORMAT": os.environ.get("SCRAPER_FEED_FORMAT", "json"),
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": os.environ.get(
            "SCRAPER_REQUEST_FINGERPRINTER_IMPLEMENTATION", "2.7"
        ),
        "TWISTED_REACTOR": os.environ.get(
            "SCRAPER_TWISTED_REACTOR",
            "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        ),
        "FEED_EXPORT_BATCH_ITEM_COUNT": os.environ.get(
            "SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT", 10
        ),
    }

    rules = (
        Rule(
            LinkExtractor(
                allow=allow,
                deny=deny,
                allow_domains=allowed_domains,
                deny_extensions=deny_extensions,
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        """Parse item"""

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
