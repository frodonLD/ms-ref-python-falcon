# -*- coding: utf-8 -*-
"""
Application entry point.

Initializes the application and returns a falcon.API for Gunicorn to run.

Example::

    PYTHONPATH=$PYTHONPATH:. \
    MONGO_URI='mongodb://localhost:27017/' \
    gunicorn \
        --workers 5 \
        --logger-class app.common.logging.GunicornLogger \
        'app.app:run()'
"""
import falcon

from .controller.contacts_controller import Contacts, Contact
from .controller.health import Liveness, Readiness, Ping
from .common.falcon_mods import falcon_error_serializer
from .common.logging import initialize_logging, Logger
from .common.middleware import Telemetry, RequestId


def initialize() -> falcon.API:
    """
    Initialize the falcon api and our router
    :return: an initialized falcon.API
    """
    # No need to initialize logging here - Gunicorn will do it and then load us
    # into a configured system
    # initialize_logging()

    # Create our WSGI application
    # media_type set for json:api compliance
    api = falcon.API(media_type='application/json',
                     middleware=[RequestId(), Telemetry()])

    # Add a json:api compliant error serializer
    api.set_error_serializer(falcon_error_serializer)

    # Routes
    api.add_route('/reference/falcon/contacts', Contacts())
    api.add_route('/reference/falcon/contacts/{contact_id}', Contact())
    api.add_route('/healthz/liveness', Liveness())
    api.add_route('/healthz/ping', Ping())
    api.add_route('/healthz/readiness', Readiness())
    return api


def run() -> falcon.API:
    """
    :return: an initialized falcon.API
    """
    Logger('app').info("ms-ref-python-falcon starting")
    return initialize()
