#!/usr/bin/env bash
#
# lint the project, omitting reports, just fail on any error.
#
# From pl-cloud-starter/backend/ms-ref-python-falcon::
#
#   ./build/lint.sh
#
lint() {
    local PROJECT="$1"
    local OUTPUT

    OUTPUT=$(pylint -f parseable --errors-only --jobs 4 ${PROJECT})

    if [ $? -ne 0 ]; then
        echo
        echo -e "${OUTPUT}"
        echo
        fatal "pylint ${PROJECT} failed"
    else
        echo "pylint ${PROJECT} passed"
    fi
}

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
(
    # ensure we are at project root
    cd ${MY_DIR}/..
    . jenkins/common.sh

    lint app
    lint test
)

