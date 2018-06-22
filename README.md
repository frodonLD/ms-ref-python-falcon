## Microservice reference: groovy / spring / gradle

This repo provides a reference cloud-native microservice implementing best practices described in [my blog](http://stevetarver.github.io/):

* Code
    * **TODO** Request validation
    * Minimal json:api standard (normal response and error bodies)
    * Healthz endpoints: liveness, readiness, and ping
* Build
    * **TODO** Unit tests and code coverage
    * Integration tests
    * Custom CI docker image
    * Helm chart
* Operations
    * Smoke test
    * Structured logging implementing the [logging standard](https://github.com/CenturyLinkCloud/pl-cloud-infrastructure/wiki/Standard:-Logging)
    * **TODO** Metrics using the Prometheus standard
    * **TODO** Distributed tracing using Jaeger client libraries

Implementation descriptions for each facility are in the `doc` directory.

## TODO

* add liveness and readiness probe to all tests with a repeat block

## Project structure

All kubernetes projects have, at project root:

* `/docker/{repo-name}`: Dockerfiles and related files
* `/helm/{repo-name}`: Helm templated kubernetes manifests
* `/jenkins/scripts`: Build scripts that implement pipeline stages
* `/jenkins/job-config`: Jenkins job config.xml files for each cluster
* `Jenkinsfile`: The standard Jenkins pipeline and configuration
* `/app`: All source code

## Project setup

See `doc/project_setup.md`

## Running locally

### Python app from IDE or command line

For local development and tinkering, you can run the service from the IDE or command line but you will need to build and run the MongoDb contacts datastore:

1. Clone the [sample-data repo](https://github.com/stevetarver/sample-data)
1. `cd docker`
1. `./build.sh build mongo`
1. `./build.sh run mongo`

Run the service in the IDE or from the command line:

```
./run.dev.sh
```

### docker-compose

To bring both this service and the MongoDB backend up on your local machine

```
ᐅ ./integration-test/local/compose_up.sh
===> Bringing up falcon and mongo with docker compose
Creating network "local_default" with the default driver
Creating ms-ref-python-falcon-service ... done
Creating ms-ref-python-falcon-service ...
===> It will take a bit for mongo to complete its initialization... but when complete
===> ms-ref-python-falcon is at http://localhost:8080
===> and MongoDB is at mongodb://localhost:27117
===> Opening a browser showing contacts
```

Notes:

* If no local image exists with tag `latest`, one will be built.
* If you want the docker image to refelect current code: `./integration-test/local/docker_clean.sh`

To bring this environment down:

```
ᐅ ./integration-test/local/compose_down.sh
Stopping ms-ref-python-falcon-service ... done
Stopping ms-ref-python-falcon-mongodb ... done
Removing ms-ref-python-falcon-service ... done
Removing ms-ref-python-falcon-mongodb ... done
Removing network local_default
```

This stops and removes containers created during `compose_up.sh`.

### minikube

To get started with minikube and helm, look through the instructions at `pl-cloud-starter/doc/install_k8s_and_helm_locally.md`.

To avoid docker image collisions with the Jenkins pipeline, we will use a dedicated portr repo: clc-control-minikube.

1. Start minikube: `minikube start`
1. Deploy to minikube: `./integration-test/local/minikube_install.sh`
4. Delete from minikube `./integration-test/local/minikube_delete.sh`
1. Stop minikube: `minikube stop`

Notes:

* You will be asked for portr creds during `minikube_install.sh`
* The script will open the minikube Kubernetes dashboard for you
* The script will open a browser to the `/contacts` collection
* The script will print out urls for the service and datastore

## Run unit tests

This project uses the `pytest` package. To run all tests in `test/`:

```
$ pytest test
```

## Run integration tests

There is a robust newman integration test runner: `integration-test/run.sh`. This is used for integration, canary, and prod deploy tests.

You can run this on local code:

```
ᐅ ./integration-test/local/compose_up.sh
===> Bringing up falcon and mongo with docker compose
Creating network "local_default" with the default driver
Creating ms-ref-python-falcon-mongodb ... done
Creating ms-ref-python-falcon-service ...
===> It will take a bit for mongo to complete its initialization... but when complete
===> ms-ref-python-falcon is at http://localhost:8000
===> and MongoDB is at mongodb://localhost:27117
===> Opening a browser showing contacts

ᐅ ./integration-test/run.sh -r -e local.compose
Running: newman run --color --reporters html -n 1 -e postman/env.local.native.json postman/test.smoke.json

ᐅ ./integration-test/local/compose_down.sh
Stopping ms-ref-python-falcon-mongodb ... done
Stopping ms-ref-python-falcon-service ... done
Removing ms-ref-python-falcon-mongodb ... done
Removing ms-ref-python-falcon-service ... done
Removing network local_default
```

## Local Jenkins build testing

The `tools` directory provides scripts that provide all env vars that Jenkins does and calls the `/jenkins/stages` versions simulating behaviour in the build pipeline.
