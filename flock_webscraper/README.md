# Custom Web Scraper with Scrapy

This project is a customizable web scraper built using Scrapy, a powerful Python web scraping library. The scraper is designed to be easily configurable and can be run within a Docker container.

- [Custom Web Scraper with Scrapy](#custom-web-scraper-with-scrapy)
  - [Running the Scraper](#running-the-scraper)
    - [Using Docker](#using-docker)
  - [Without Docker](#without-docker)
  - [Customizing the Scraper](#customizing-the-scraper)

---

The scraper's behavior can be configured using a JSON file or a JSON string. The configuration options include:

- spider_name: The name of the spider (required).
- allowed_domains: A list of domains the spider is allowed to crawl (required).
- start_urls: A list of URLs to start the crawl (required).
- custom_settings: A dictionary of custom Scrapy settings (optional).
- deny_extensions: A list of file extensions to deny during the crawl (optional).

**Example configuration:**

```json
{
  "spider_name": "my_spider",
  "allowed_domains": ["example.com"],
  "start_urls": ["https://www.example.com"],
  "custom_settings": {
    "DOWNLOAD_DELAY": 1
  },
  "deny_extensions": [".pdf", ".docx"]
}
```

## Running the Scraper

### Using Docker

1. Build the Docker image:

```bash
docker build -t my_scraper .
```

2. Run the scraper with configuration from a file:

```bash
# Replace /path/to/local/config_file.json with the path to your custom config file on your local machine.
docker run -v /path/to/local/config_file.json:/app/custom_config.json -e SCRAPER_CONFIG=/app/custom_config.json my_scraper
```

Or, run the scraper with configuration from a JSON string:

```bash
# Store the JSON configuration string in a variable
CONFIG_JSON='{"spider_name": "my_spider", "allowed_domains": ["example.com"], "start_urls": ["https://www.example.com"]}'

# Pass the JSON string using the -e flag
docker run -e SCRAPER_CONFIG_JSON="$CONFIG_JSON" my_scraper
```

## Without Docker

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Run the scraper:

```bash
# Set the SCRAPER_CONFIG or SCRAPER_CONFIG_JSON environment variable with the path to your config file or JSON string.
export SCRAPER_CONFIG="/path/to/config_file.json"
# Or
export SCRAPER_CONFIG_JSON='{"spider_name": "my_spider", "allowed_domains": ["example.com"], "start_urls": ["https://www.example.com"]}'

# Run the scraper
python run_spider.py
```

## Customizing the Scraper

To customize the scraping logic, modify the parse method in the FlockSpider class located in the scraper/spiders/flock_spider.py file:

```python
def parse(self, response):
    # Your parsing logic here
    pass
```

Refer to the [Scrapy documentation](https://docs.scrapy.org/en/latest/) for more information on customizing spiders, handling different types of items, and storing the scraped data.
