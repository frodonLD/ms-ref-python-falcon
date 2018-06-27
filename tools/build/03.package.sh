#!/usr/bin/env bash
#
# Source our local environment variables and call matching script in jenkins/scripts
#
MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
(
    # ensure we are at project root
    cd ${MY_DIR}/../..
    . tools/build/config.sh

    ./jenkins/scripts/$(basename "$0")
)
