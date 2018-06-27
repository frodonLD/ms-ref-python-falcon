#!/bin/sh
#
# Environment variables used during package and archive stages
#

# UTC timestamp to seconds: 20171115211420
export BUILD_TIMESTAMP=$(TZ= date +%Y%m%d%H%M%S)

export GIT_REPO_URL=$(git config remote.origin.url)
export GIT_ORG_REPO_NAME=$(git config remote.origin.url | cut -f4-5 -d"/" | cut -f1 -d".")
export GIT_REPO_NAME=$(git config remote.origin.url | cut -d '/' -f5 | cut -d '.' -f1)
export GIT_BRANCH_NAME=$(git branch | grep \* | cut -d ' ' -f2-)
export GIT_COMMIT_HASH=$(git rev-parse HEAD)

export DOCKER_GROUP='stevetarver'
export DOCKER_PROJECT='ms-ref-python-falcon'

export DOCKER_IMAGE_BASENAME="${DOCKER_GROUP}/${DOCKER_PROJECT}"
export DOCKER_BUILD_IMAGE_NAME="${DOCKER_IMAGE_BASENAME}-${GIT_BRANCH_NAME}"
export DOCKER_BUILD_IMAGE_NAMETAG="${DOCKER_BUILD_IMAGE_NAME}:${BUILD_TIMESTAMP}"
export DOCKER_BUILD_IMAGE_NAMETAG_LATEST="${DOCKER_BUILD_IMAGE_NAME}:latest"

export DOCKER_DEPLOY_IMAGE_NAMETAG="${DOCKER_BUILD_IMAGE_NAME}:${BUILD_TIMESTAMP}"

export DOCKER_CI_IMAGE_NAMETAG="${DOCKER_GROUP}/python-ci:3.6.5-alpine3.6-r0"
