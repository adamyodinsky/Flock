# First stage: Install dependencies using Poetry
FROM python:3.9-slim-buster as builder

# Set the working directory
WORKDIR /app

# Set the Poetry version as a build argument
ARG POETRY_VERSION=1.1.9

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install the dependencies and create a virtual environment
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-dev

# Second stage: Prepare the final image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the project files into the container
COPY . .

# Run the Scrapy spider
CMD ["python", "run_spider.py"]
