# Flock-Agent

Flock Agent

- [Interactive API docs](http://127.0.0.1:8000/redoc)
- [Alternative API docs](http://127.0.0.1:8000/docs)

## How it works

Containerized agent server.
AgentServer will be a FastAPI Server that imports the Builder class.
Together with a click, he will have the command run.
First, it will run the app server (and report to the mainframe in a later stage), then it will ingest the manifest into the Builder buildAgent method.

### Commands

#### run

- Loads configuration from a file (flag of input-path) or a string (flag of input-value)
- Spins the API server
- (Reports - Initializing)
- Validates the agent manifest
- Builds the agent
- (Reports Ready)
- Waiting for requests
