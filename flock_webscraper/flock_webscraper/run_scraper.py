import json
import os

from flock_webscraper.flock_webscraper.spiders.flock import FlockSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule



def load_config(config_obj: dict = None, file_path='config.json'):
    if config_obj:
        return config_obj
    with open(file_path, 'r') as config_file:
        return json.load(config_file)


def run_flock_spider(config_file: str = 'config.json', config_obj = None):
    config_obj = os.environ.get("SCRAPER_CONFIG_JSON", config_obj)
    config_file = os.environ.get("SCRAPER_CONFIG", config_file)
    config = load_config(config_obj=config_obj, file_path=config_file)
    settings = get_project_settings()

    # Add custom settings
    for custom_key, custom_value in config.get("custom_settings", {}).items():
        settings.set(custom_key, custom_value)

    rule = (
        Rule(
            LinkExtractor(
                allow_domains=config["allowed_domains"],
                deny_extensions=config["deny_extensions"]
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    process = CrawlerProcess(settings)
    process.crawl(
        FlockSpider,
        name=config["name"],
        start_urls=config["start_urls"],
        custom_settings=config["custom_settings"],
        allow_domains=config["allowed_domains"],
        deny_extensions=config["deny_extensions"],
        rule=rule,
    )
    process.start()


if __name__ == "__main__":
    run_flock_spider()
