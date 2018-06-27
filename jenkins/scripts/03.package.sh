#!/usr/bin/env bash
#
# Package the app - build the docker image
#
MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
(
    # ensure we are at project root
    cd ${MY_DIR}/../..
    . jenkins/common.sh

    echo "$ECHO_PREFIX Generating build information for ${DOCKER_PROJECT}"
    ./jenkins/generate_build_info.sh

    if [[ $? -ne 0 ]]; then
        fatal "./jenkins/generate_build_info.sh failed"
    fi

    echo "$ECHO_PREFIX Building ${DOCKER_PROJECT} image"
    docker build \
        -f "docker/Dockerfile"                         \
        --build-arg GIT_REPO_NAME=${GIT_REPO_NAME}     \
        --build-arg GIT_BRANCH_NAME=${GIT_BRANCH_NAME} \
        --build-arg BUILD_TIMESTAMP=${BUILD_TIMESTAMP} \
        --build-arg GIT_COMMIT_HASH=${GIT_COMMIT_HASH} \
        -t ${DOCKER_BUILD_IMAGE_NAMETAG}               \
        -t ${DOCKER_BUILD_IMAGE_NAMETAG_LATEST}        \
        .
)