#!/usr/bin/env bash
#
# Docker run command for this service
#
# Configuration
#   --graceful-timeout 10 - match docker stop timeout
#
PYTHONPATH=$PYTHONPATH:. \
gunicorn \
    -b 0.0.0.0:8000 \
    --workers 25 \
    --graceful-timeout 10 \
    --logger-class app.common.logging.GunicornLogger \
    'app.app:run()'
