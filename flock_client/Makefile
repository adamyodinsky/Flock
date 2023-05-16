
run:
	poetry run python flock_client/main.py run-server $(ARGS)


run-example-agent:
	poetry run python flock_client/main.py run-server $(ARGS) \
	--backend-host http://localhost:8000/agent \
	--backend-type agent \
	--port 7860


run-example-llm:
	poetry run python flock_client/main.py run-server $(ARGS) \
	--backend-host http://localhost:8080/v1/chat/completions \
	--backend-type llm \
	--port 7862
	

