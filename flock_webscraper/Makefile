.PHONY: help install test docker-test-build docker-test-run docker-build-prod clear

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  install           to install dependencies"
	@echo "  test              to run tests"
	@echo "  docker-test-build to build docker image for testing"
	@echo "  docker-test-run   to run docker image for testing"
	@echo "  docker-build-prod to build docker image for production"
	@echo "  clear             to clear spider output"

install:
	poetry install

test:
	@SCRAPER_NAME="test_spider" \
	SCRAPER_START_URLS="http://books.toscrape.com/catalogue/category/books/romance_8/index.html" \
	RULE_SCRAPER_ALLOWED_DOMAINS="books.toscrape.com" \
	RULE_SCRAPER_ALLOW="/catalogue/category/books/romance_8 /catalogue/category/books/philosophy_7" \
	RULE_SCRAPER_DENY_EXTENSIONS="" \
	SCRAPER_OUTPUT_DIR="${PWD}/.spider_output" \
	SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT=10 \
	poetry run scrapy runspider flock_webscraper/flock_spider.py

docker-test-build:
	@echo "Building docker image for testing"
	@docker build -t flock-webscraper .

docker-build-prod:
	docker build -t flock-webscraper:`poetry version | cut -d ' ' -f 2` .

docker-test-run:
	@docker run --rm \
	-e SCRAPER_NAME="test_spider" \
	-e SCRAPER_START_URLS="http://books.toscrape.com/catalogue/category/books/romance_8/index.html" \
	-e RULE_SCRAPER_ALLOWED_DOMAINS="books.toscrape.com" \
	-e RULE_SCRAPER_ALLOW="/catalogue/category/books/romance_8 /catalogue/category/books/philosophy_7" \
	-e RULE_SCRAPER_DENY_EXTENSIONS="" \
	-e SCRAPER_OUTPUT_DIR="/app/spider_output" \
	-e SCRAPER_FEED_EXPORT_BATCH_ITEM_COUNT=10 \
	--name flock_webscraper_test \
	-v ${PWD}/.spider_output:/app/spider_output \
	flock-webscraper

clear:
	rm -rf .spider_output
	