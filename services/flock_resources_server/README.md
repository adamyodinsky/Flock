# Flock FastAPI server

## Installation & Usage

To run the server, please execute the following from the root directory:

```bash
poetry install
uvicorn main:app --host 0.0.0.0 --port 8080
```

and open your browser at `http://localhost:8080/docs/` to see the docs.

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
docker-compose up --build
```

## Tests

To run the tests:

```bash
pip3 install pytest
PYTHONPATH=src pytest tests
```

- <https://github.com/mjhea0/awesome-fastapi>
- <https://github.com/zhanymkanov/fastapi-best-practices>
  
## Docs

<http://127.0.0.1:8000/redoc>
<http://127.0.0.1:8000/docs>
