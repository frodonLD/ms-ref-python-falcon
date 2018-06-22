#!/usr/bin/env bash
#
# This run command is intended for local development in prod mode
#
# Configuration
#   --graceful-timeout 10 - match docker stop timeout

PYTHONPATH=$PYTHONPATH:. \
MONGO_URI='mongodb://localhost:27017/' \
gunicorn \
    --workers 5 \
    --graceful-timeout 10 \
    --logger-class app.common.logging.GunicornLogger \
    'app.app:run()'

