from flask import Flask, request
import json

from inventory.handler import InventoryHandler

app = Flask('shoppy')
app.config.from_pyfile('config.py')
inventory_json_path = app.config['INVENTORY_JSON_PATH']

with open(inventory_json_path) as inventory_file:
    inventory_data = json.load(inventory_file)
inventory_handler = InventoryHandler(inventory_data)

@app.route('/inventory', methods=['GET'])
def list_inventory():
    """Print the current inventory and list of prices per quantity"""
    return inventory_handler.get_current_inventory()

@app.route('/purchase', methods=['POST'])
def purchase():
    """Purchase (assuming enough money is sent and inventory present, 
        the items that have been purchased are removed from the inventory), 
        returning the leftover change"""
    return inventory_handler.purchase(request.json)

@app.route('/price_check', methods=['POST'])
def price_check():
    """Get the price for a set of groceries"""
    return inventory_handler.price_check(request.json)

@app.route('/reset', methods=['DELETE'])
def reset():
    """Reset, which restocks inventory and resets log
    Going with the reset verb as this is a destructive change"""
    return inventory_handler.reset()

@app.route('/logs', methods=['GET'])
def purchase_logs():
    """Get a log of all purchases"""
    return inventory_handler.get_purchase_logs()

@app.route('/status', methods=['GET'])
def status():
    return {'status': 'IMOK'}
