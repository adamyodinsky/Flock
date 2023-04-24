# Use a base image with Python 3.9
FROM python:3.9

# Set the working directory
WORKDIR /app

COPY . /app

RUN apt update && apt install curl -y && apt install net-tools -y
# Install the dependencies and the main project
# RUN pip install --index-url=http://localhost:8080/simple/ flock-secrets-store && \
#     pip install --index-url=http://localhost:8080/simple/ flock-resource-store && \
#     pip install --index-url=http://localhost:8080/simple/ flock-schemas && \
#     pip install --index-url=http://localhost:8080/simple/ flock-models && \
# RUN    pip install dependencies/flock_agent-*.whl

# Run the application
# ENTRYPOINT ["python", "flock_agent/main.py", "run-agent"]

# pip install --index-url=http://localhost:8080/simple/ flock-secrets-store
# pip install --index-url=http://localhost:8080/simple/ flock-resource-store
# pip install --index-url=http://localhost:8080/simple/ flock-schemas
# pip install --index-url=http://localhost:8080/simple/ flock-models
# pip install --index-url=http://localhost:8080/simple/ flock-agent

# pip download --index-url=http://localhost:8080/simple/ flock-secrets-store -d dependencies
# pip download --index-url=http://localhost:8080/simple/ flock-resource-store -d dependencies
# pip download --index-url=http://localhost:8080/simple/ flock-schemas -d dependencies
# pip download --index-url=http://localhost:8080/simple/ flock-models -d dependencies
# pip download --index-url=http://localhost:8080/simple/ flock-agent -d dependencies


