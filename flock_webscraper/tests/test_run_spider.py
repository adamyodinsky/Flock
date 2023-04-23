from flock_webscraper.run_scraper import run_flock_spider

def test_run_spider():
    # file_path = "config_example.json"
    # run_flock_spider(config_file=file_path)


    config = {
        "name": "test_spider",
        "allowed_domains": ["gutenberg.org"],
        "start_urls": ["https://www.gutenberg.org"],
        "custom_settings": {
          "DOWNLOAD_DELAY": 1
        },
        "deny_extensions": [".pdf", ".docx"]
    }

    run_flock_spider(config_obj=config)


if __name__ == "__main__":
  test_run_spider()
