
# Flock Deployer

## Pre-requisites for testing Test this project

- Setup the Flock project according to the readme in the root Flock directory, spinning up the minikube cluster etc...
- Run the "validate_resources" command on the flock_resources module.
- Run "write-json-schemas" and "load-global-config" commands (in this order).

## Okteto

```sh
MINIKUBE_IP=$(minikube ip)
PORT=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' | awk -F: '{print $3}' | tr -d /)
okteto context use https://$MINIKUBE_IP:$PORT
```
