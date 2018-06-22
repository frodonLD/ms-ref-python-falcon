# -*- coding: utf-8 -*-
"""
Contacts Controller

Falcon wants a single class as a responder for each URI. Most frequently,
this will divide a single resource into operations on the collection and
collection items. We use:
    * Contacts: for operations on the entire contacts collection
    * Contact: for operations on a single contact item

ReST Controller classes:
Classes in the controller directory are responsible for
    * request parameter validation
    * response encoding
    * exception handling

Examples:
    A well formed contact response looks like::

        {
        "type": "contacts",
        "id": "5970fc55f33a80de48ba7a54",
        "attributes": {
            "_id": "5970fc55f33a80de48ba7a54",
            "firstName": "Leroy",
            "lastName": "Jenkins",
            "companyName": "Docker Publishing Company",
            "address": "1 Solutions Parkway",
            "city": "Town & Country",
            "county": "Chesterfield",
            "state": "MO",
            "zip": "63011",
            "phone1": "855-226-0709",
            "phone2": "888-638-6771",
            "email": "leroy.jenkins@ctl.io",
            "website": "http://www.ctl.io"
            }
        },

Logging:
    * Each class is subclassed from the LoggerMixin which exposes protected
      members for logging. The logging mixins add information about the class
      to the log entry.
"""
from typing import Union, List, Dict

import falcon

from ..common.logging import LoggerMixin
from ..service.contacts_service import ContactsService


class _ContactsController(LoggerMixin):

    def __init__(self):
        self._service = ContactsService()

    @staticmethod
    def _validate_contact(_: falcon.Request, __: falcon.Response, ___, ____):
        """
        Validate create contact params.

        Example:
            This will normally be attached to the on_post, on_put methods via a before hook::

                @falcon.before(_ContactsApi._validate_contact)

        Args:
            req (falcon.Request): the client request
            resp (falcon.Response): the client response (so far)
            resource:
            params:

        Returns:
            Nothing on success.

            Raises a falcon.HTTPBadRequest on validation error with explanation
            in response body.
        """
        # perform validation and if failure ->
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)


class Contacts(_ContactsController):
    """Handler for collection operations"""

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Get list of contacts"""
        # resp.body = json.dumps(self._service.get_list(req))
        resp.media = self._service.get_list(req)

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Create a contact"""
        resp.media = self._service.create_item(req)
        resp.status = falcon.HTTP_201


class Contact(_ContactsController):
    """Handler for element operations"""

    def on_delete(self, req: falcon.Request, resp: falcon.Response, contact_id: str) -> None:
        """Delete specified contact"""
        self._service.delete_item(req, contact_id)
        resp.status = falcon.HTTP_204

    def on_get(self, req: falcon.Request, resp: falcon.Response, contact_id: str) -> None:
        """Get specified contact"""
        resp.media = self._service.get_item(req, contact_id)

    def on_patch(self, req: falcon.Request, resp: falcon.Response, contact_id: str) -> None:
        """Update specified contact - unspecified attributes are not modified"""
        resp.media = self._service.update_item(req, contact_id)

    def on_put(self, req: falcon.Request, resp: falcon.Response, contact_id: str) -> None:
        """Replace specified contact"""
        resp.media = self._service.replace_item(req, contact_id)
