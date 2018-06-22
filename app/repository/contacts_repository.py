# -*- coding: utf-8 -*-
"""
All operations on the MongoDB contacts collection
"""
import json
import os
from typing import List, Dict

import falcon
from bson import errors as bsonErrors
from bson.objectid import ObjectId
from pymongo import MongoClient, ReturnDocument
from pymongo import errors as pymongoErrors

from ..common.logging import LoggerMixin


class ContactsRepoMongo(LoggerMixin):
    """
    Handles all interactions with the MongoDB contacts collection

    NOTES:
    MongoDB bson ObjectIds are not json serializable, however, you can cast
    the ObjectId to a str, which is, and use that str to construct an ObjectId
    for searching.
    """

    def __init__(self):
        # 'mongodb://localhost:27017/'
        self._uri = os.getenv('MONGO_URI', '')
        if not self._uri:
            raise ValueError('MONGO_URI env var not set; required to connect to mongodb')
        self._mongo = MongoClient(self._uri,
                                  # Set the mongo connect timeout to 1s < gunicorn
                                  # worker timeout so we will fire a 503 when db is down
                                  serverSelectionTimeoutMS=29000)
        self._contacts = self._mongo.test.contacts

    def create_item(self, req: falcon.Request) -> Dict:
        try:
            result = self._contacts.insert_one(
                req.context['body_json']
            )
            return self._post_process_contact(self.get_item(None, str(result.inserted_id)))
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def delete_item(self, _: falcon.Request, object_id: str) -> None:
        try:
            self._contacts.delete_one(
                {'_id': self._make_objectid(object_id)}
            )
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def find_one(self) -> Dict:
        try:
            return self._post_process_contact(self._contacts.find_one())
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def get_list(self, _: falcon.Request) -> List[Dict]:
        try:
            self._info("Fetching all contacts from datastore")
            result = []
            for contact in self._contacts.find():
                result.append(contact)
            return self._post_process_contacts(result)
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def get_item(self, _: falcon.Request, object_id: str) -> Dict:
        try:
            contact = self._contacts.find_one(
                {'_id': self._make_objectid(object_id)}
            )
            if contact is None:
                self._handle_not_found(object_id)
            return self._post_process_contact(contact)
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def ping(self) -> None:
        """
        A very light weight database connectivity check used with liveness and
        readiness probes. Throws a service unavailable exception on failure
        :return:
        """
        try:
            self._mongo.admin.command('ping')
        except:  # pylint: disable=bare-except
            self._handle_service_unavailable()

    def replace_item(self, req: falcon.Request, object_id: str) -> Dict:
        try:
            result = self._contacts.find_one_and_replace(
                {'_id': self._make_objectid(object_id)},
                req.context['body_json'],
                return_document=ReturnDocument.AFTER)
            if result is None:
                self._handle_not_found(object_id)
            return self._post_process_contact(result)
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def update_item(self, req: falcon.Request, object_id: str) -> Dict:
        try:
            result = self._contacts.find_one_and_update(
                {'_id': self._make_objectid(object_id)},
                {'$set': req.context['body_json']},
                return_document=ReturnDocument.AFTER)
            if result is None:
                self._handle_not_found(object_id)
            return self._post_process_contact(result)
        except (pymongoErrors.AutoReconnect,
                pymongoErrors.ConnectionFailure,
                pymongoErrors.NetworkTimeout):
            self._handle_service_unavailable()

    def _make_objectid(self, object_id: str) -> ObjectId:
        try:
            return ObjectId(object_id)
        except bsonErrors.InvalidId as ex:
            raise falcon.HTTPBadRequest(
                title='Invalid contact id: {}'.format(object_id),
                description=str(ex))

    def _handle_not_found(self, object_id) -> None:
        raise falcon.HTTPNotFound(
            title='Not Found',
            description="Contact {} not found".format(object_id))

    def _handle_service_unavailable(self) -> None:
        raise falcon.HTTPServiceUnavailable(
            title='Datastore is unreachable',
            description="MongoDB at {} failed to respond to ping. "
                        "This is a transient, future attempts will work "
                        "when the datastore returns to service".format(self._uri),
            href='https://www.makara.com/api-docs/v2/#firewall',
            retry_after=30
        )

    def _post_process_contact(self, contact: dict) -> dict:
        """Convert _id to id for conformity with other reference services"""
        if '_id' in contact:
            contact['id'] = str(contact['_id'])
            del contact['_id']
        return contact

    def _post_process_contacts(self, contactList: list) -> list:
        """Convert _id to id for conformity with other reference services"""
        for item in contactList:
            self._post_process_contact(item)
        return contactList