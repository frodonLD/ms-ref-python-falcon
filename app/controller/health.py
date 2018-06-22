# -*- coding: utf-8 -*-
"""
Service health indicators
"""
from datetime import datetime

import falcon

from ..common.json_api import make_response
from ..service.contacts_service import ContactsService
from ..repository.contacts_repository import ContactsRepoMongo
from ..common.build_info import BuildInfo

class Liveness(object):
    """
    Are we functional? Or should our scheduler kill us and make another.

    Note that this is a different question than "Are we ready to process messages?"
    and should only check for hung state within our service.

    Every service may have a slightly different method for determining if
    it is "hung". Choose one that is light-weight.

    Examples:
    - Pump a synthetic message through your service, checking for success
      excluding upstream partner liveness or readiness.
    - Check all threads in the process for a hung state.

    Note: there is tension between proving at least one thread is workable vs.
          all threads are workable. Some systems will detect hung threads and
          terminate them while others can gradually put every thread in the
          pool into a hung state until the thread pool is exhausted.

    This service will pump a get message through our service to prove all
    parts viable.

    Return 200 OK if we are functional, 503 otherwise with a json:api error
    describing the fault.
    """
    # TODO: implement json:api error response on failure
    def on_get(self, _: falcon.Request, resp: falcon.Response):
        start = datetime.now()
        ContactsService().find_one()
        duration = int((datetime.now() - start).total_seconds() * 1000000)

        resp.body = make_response('liveness',
                                  'id',
                                  dict(id=0,
                                       mongodb='ok',
                                       mongodbFindOneDurationMicros=duration))


class Readiness(object):
    """
    Are we ready to serve requests?

    Check that we have completed initialization and can connect to all upstream
    components using the upstream component's ping endpoint or similar light-weight
    read operation.

    Return 200 OK if we are functional, 503 otherwise with a json:api error
    describing the fault.
    """
    # TODO: implement json:api error response on failure
    def on_get(self, _: falcon.Request, resp: falcon.Response):
        start = datetime.now()
        ContactsRepoMongo().ping()
        duration = int((datetime.now() - start).total_seconds() * 1000000)

        resp.body = make_response('readiness',
                                  'id',
                                  dict(id=0,
                                       mongodb='ok',
                                       mongodbPingDurationMicros=duration))


class Ping(object):
    """
    Can someone connect to us?

    Light weight connectivity test for other service's readiness probes.

    Return 200 OK if we got this far, framework will fail or not respond
    otherwise
    """
    def on_get(self, _: falcon.Request, resp: falcon.Response):
        info = BuildInfo()
        result = dict(id=0,
                      repoName=info.repo_name,
                      commitHash=info.commit_hash,
                      serviceType=info.service_type,
                      serviceName=info.service_name,
                      serviceVersion=info.version,
                      buildDate=info.build_date,
                      buildEpochSec=info.build_epoch_sec
                     )
        resp.body = make_response('ping', 'id', result)
