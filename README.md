# Flock

## Pre-requisites

- Minikube
- Docker
- Python
- Ngrok
- Okteto

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

### Expose the local machine with ngrok

```sh
export NGROK_USERNAME=user
export NGROK_PASSWORD=pass

make ngrok
```

- For accessing the ngrok endpoint via the browser, just enter the username and password.
- For accessing the ngrok endpoint via an http request, add an "Authorization" header, the value should be a base64 converted string of `<username>:<password>`.

#### Env Variables needed

- OPENAI_API_KEY
- SERPAPI_API_KEY
- WOLFRAM_ALPHA_APPID

## Troubleshooting

### Issue 01

Getting error when starting Minikube on a Mac machine

`failed to connect to /var/run/com.docker.vmnetd.sock: is vmnetd running?`

#### Solution

```sh
/Applications/Docker.app/Contents/MacOS/install remove-vmnetd
sudo /Applications/Docker.app/Contents/MacOS/install vmnetd
```

source: <https://github.com/docker/for-mac/issues/6677#issuecomment-1593787335>

### Exposing the service

https://www.softwaretestinghelp.com/ngrok-alternatives/
https://github.com/anderspitman/awesome-tunneling

- ngrok has an issue with cors i could not solve
- local tunnel - "lt --port 80" need to try it
- servo
