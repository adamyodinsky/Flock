import json
import os

from scraper import FlockSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def load_config(json_string=None, file_path='config.json'):
    if json_string:
        return json.loads(json_string)
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

if __name__ == "__main__":
    config_json_string = os.environ.get("SCRAPER_CONFIG_JSON")
    config_file = os.environ.get("SCRAPER_CONFIG", "config.json")
    config = load_config(json_string=config_json_string, file_path=config_file)
    settings = get_project_settings()

    # Add custom settings
    for custom_key, custom_value in config.get("custom_settings", {}).items():
        settings.set(custom_key, custom_value)

    process = CrawlerProcess(settings)
    process.crawl(
        FlockSpider,
        spider_name=config["spider_name"],
        allowed_domains=config["allowed_domains"],
        start_urls=config["start_urls"],
        custom_settings=config["custom_settings"],
        deny_extensions=config["deny_extensions"]
    )
    process.start()
