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

## VSCODe Testing configuration

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "flock_agent/main.py",
      "console": "internalConsole",
      "justMyCode": true,
      "env": {
        "OPENAI_API_KEY": "token",
        "SERPAPI_API_KEY": "token",
        "INPUT_PATH": "tests/schemas/agent.json",
      },
      "args": ["run-agent"]
    },
    {
      "name": "Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
          "-s",
          "-vv",
          "-p",
          "no:cacheprovider",
          "${workspaceFolder}/tests"
      ],
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal",
    }
  ]
}
```

Test it with:

```bash
 curl -X POST -H "Content-Type: application/json" -d '{ "msg": "who is the president of USA?" }' localhost:8000/agent
```
