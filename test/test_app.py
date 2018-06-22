# -*- coding: utf-8 -*-
import os
import falcon
from falcon import testing
import pytest
from unittest.mock import mock_open, call

from pprint import pprint
from app.common.logging import initialize_logging, Logger
from app import app


@pytest.fixture
def client():
    os.environ["MONGO_URI"] = "mongodb://localhost:27017/"
    initialize_logging()
    return testing.TestClient(app.initialize())


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_get_contacts(client):
    doc = example_contact()

    # This simulates a GET /contacts - the mongo db must be running to succeed
    response = client.simulate_get('/contacts/5a41694752ec07986833d759')
    pprint(response)
    print(response.json)
    Logger('test').info("ms-ref-python-falcon starting", contact=response.json)

    assert response.json == doc
    assert response.status == falcon.HTTP_OK


def example_contact():
    return {
        "data": {
            "type": "contacts",
            "id": "5a41694752ec07986833d759",
            "attributes": {
                "_id": "5a41694752ec07986833d759",
                "firstName": "James",
                "lastName": "Butt",
                "companyName": "Benton, John B Jr",
                "address": "6649 N Blue Gum St",
                "city": "New Orleans",
                "county": "Orleans",
                "state": "LA",
                "zip": "70116",
                "phone1": "504-621-8927",
                "phone2": "504-845-1427",
                "email": "jbutt@gmail.com",
                "website": "http://www.bentonjohnbjr.com"
            }
        }
    }
