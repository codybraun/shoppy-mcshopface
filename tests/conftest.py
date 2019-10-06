from pytest import fixture
from inventory.handler import InventoryHandler
from flask import current_app

import shoppy

@fixture
def sample_handler():
    inventory = [{'id':123, 'name':'potato', 'price': 100.00, 'quantity': 50},
                 {'id':456, 'name':'deluxe potato', 'price': 200.00, 'quantity': 1}]
    return InventoryHandler(inventory)

@fixture(autouse=True)
def test_app():
    with shoppy.app.test_client() as test_client:
        with shoppy.app.app_context() as context:
            yield test_client
