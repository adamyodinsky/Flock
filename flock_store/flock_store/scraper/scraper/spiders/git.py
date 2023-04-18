import re

from parsel import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GitSpider(CrawlSpider):
    name = "git"
    allowed_domains = ["python.langchain.com"]
    start_urls = ["http://python.langchain.com/"]
    deny_extensions = [
        "git",
        "gitignore",
        "gitattributes",
        "gitmodules",
        "zip",
        "tar.gz",
        "rar",
        "exe",
        "dll",
        "obj",
        "lib",
        "pdb",
        "class",
        "jar",
        "idea",
        "vscode",
        "bak",
        "lock",
        "ipynb",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                deny_extensions=deny_extensions,
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def set_crawler(self, crawler):
        self.name
        allowed_domains = ["python.langchain.com"]
        start_urls = ["http://python.langchain.com/"]

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
