.PHONY: help generate-server

serve:
	@poetry run python flock_resources_server/main.py run-server

test:
	@poetry run python flock_resources_server/main.py
	@poetry run pytest tests -vv
