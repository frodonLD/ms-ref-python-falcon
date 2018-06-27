#!/usr/bin/env bash
#
# Create app/common/build_info.py using current build parameters
#
# From pl-cloud-starter/backend/ms-ref-python-falcon
#  ./build/generate_build_info.sh
#

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SERVICE_TYPE='poc'
SERVICE_NAME='ms-ref-python-falcon'

(
    # Run from project root
    cd ${MY_DIR}/..

    # TODO: should this build version use BUILD_TIMESTAMP provided by jenkins?
    # TODO: should we hardcode these values so we can use the default docker build stage

cat << EOF > app/common/build_info.py
# -*- coding: utf-8 -*-
"""
Build information for this service.

Auto-generated during the build process - do not modify
"""


class BuildInfo(object):
    """Current build info"""
    repo_name = '${GIT_REPO_NAME}'
    service_type = '${SERVICE_TYPE}'
    service_name = '${SERVICE_NAME}'
    version = '${DOCKER_VERSION}'
    commit_hash = '${GIT_COMMIT_HASH}'
    build_date = '$(date)'
    build_epoch_sec = $(date +%s)
EOF
)
