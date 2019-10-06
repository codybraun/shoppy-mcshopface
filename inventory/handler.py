from copy import deepcopy
from flask import jsonify
from flask_api import status
from collections import Counter

class InventoryHandler():

    def __init__(self, inventory_data):
        self.original_inventory = {item['id'] : item for item in inventory_data}
        self.inventory = deepcopy(self.original_inventory)
        self.prices = {item['id']: item['price'] for item in inventory_data}
        self.purchase_logs = []

    def get_current_inventory(self):
        return jsonify(list(self.inventory.values())), status.HTTP_200_OK

    def purchase(self, purchase_order):
        items, money = purchase_order['items'], purchase_order['money']
        order_total = self.total_price(items)
        if order_total > money:
            # Insufficient payment sent
            return jsonify({'money': money, 'total': order_total}), status.HTTP_402_PAYMENT_REQUIRED
        elif not self.valid_inventory(items):
            return jsonify({'message': 'Insufficient inventory'}), status.HTTP_409_CONFLICT
        self.update_inventory(items)
        self.purchase_logs.append(purchase_order)
        return jsonify({'change': money - order_total}), status.HTTP_200_OK

    def update_inventory(self, items):
        for item in items:
            self.inventory[item]['quantity'] = self.inventory[item]['quantity'] - 1

    def valid_inventory(self, items):
        counts = Counter(items)
        for item in counts.keys():
            if self.inventory[item]['quantity'] < counts[item]:
                return False
        return True

    def total_price(self, items):
        return sum([self.prices[item] for item in items])

    def price_check(self, purchase_order):
        return jsonify({'price': self.total_price(purchase_order['items'])}), status.HTTP_200_OK

    def reset(self):
        self.inventory = deepcopy(self.original_inventory)
        self.purchase_logs = []
        return jsonify(self.inventory), status.HTTP_200_OK

    def get_purchase_logs(self):
        return jsonify(self.purchase_logs), status.HTTP_200_OK
