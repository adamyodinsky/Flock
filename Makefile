

build-poetry:
	@docker build -t flock-poetry -f Dockerfile.poetry .

build-agent:
	@docker build -t flock-agent -f Dockerfile.agent .