# Flock

## Pre-requisites

- Minikube
- Docker
- Python

## Setup

### Run all services

```sh
make minikube-start
make setup-all
```

### Run validate resources script

For uploading initial resources to the system.

Under `libs/flock_resources`, run the `resources_validation.py` script

```sh
make validate-resources
```

#### Env Variables needed

- OPENAI_API_KEY
- SERPAPI_API_KEY
- WOLFRAM_ALPHA_APPID

## Troubleshooting

### 01

Getting error when starting Minikube on Mac machine

`failed to connect to /var/run/com.docker.vmnetd.sock: is vmnetd running?`

#### Solution

```sh
/Applications/Docker.app/Contents/MacOS/install remove-vmnetd
sudo /Applications/Docker.app/Contents/MacOS/install vmnetd
```

source: <https://github.com/docker/for-mac/issues/6677#issuecomment-1593787335>

