
from inventory.handler import InventoryHandler


class TestCurrentInventory:
    def test_inventory(self, sample_handler):
        assert sample_handler.inventory == sample_handler.original_inventory
        resp = sample_handler.get_current_inventory()
        assert resp[0].json == [{'id':123, 'name':'potato', 'price': 100.00, 'quantity': 50},
                 {'id':456, 'name':'deluxe potato', 'price': 200.00, 'quantity': 1}]
        assert resp[1] == 200

class TestPurchases:
    def test_purchase_logged(self, sample_handler):
        assert len(sample_handler.purchase_logs) == 0
        sample_handler.purchase({'money':100, 'items':[123]})
        assert len(sample_handler.purchase_logs) == 1

    def test_purchase_change_returned(self, sample_handler):
        resp = sample_handler.purchase({'money':100, 'items':[123]})
        assert sample_handler.prices[123] + resp[0].json['change'] == 100

    def test_purchase_deducts_from_inv(self, sample_handler):
        assert sample_handler.inventory[123]['quantity'] == 50
        sample_handler.purchase({'money':100, 'items':[123]})
        assert sample_handler.inventory[123]['quantity'] == 49

    def test_failed_purchase_not_deducted(self, sample_handler):
        assert sample_handler.inventory[456]['quantity'] == 1
        sample_handler.purchase({'money':0, 'items':[456]})
        assert sample_handler.inventory[456]['quantity'] == 1
        sample_handler.purchase({'money':1000, 'items':[456, 456]})
        assert sample_handler.inventory[456]['quantity'] == 1

class TestValidInventory:
    def test_is_valid(self, sample_handler):
        assert sample_handler.valid_inventory([456])
        assert sample_handler.valid_inventory([123, 123, 123])
        assert not sample_handler.valid_inventory([456, 456])

class TestUpdateInventory:
    def test_is_updated(self, sample_handler):
        assert sample_handler.inventory[456]['quantity'] == 1
        sample_handler.update_inventory([456])
        assert sample_handler.inventory[456]['quantity'] == 0

class TestTotalPrice:
    def test_prices_totaled(self, sample_handler):
        assert sample_handler.total_price([456, 456, 456, 123]) == 700

class TestPriceCheck:
    def test_price_returned(self, sample_handler):
        resp = sample_handler.price_check({'items': [456, 456, 456, 123]})
        assert resp[0].json['price'] == 700

class TestReset:
    def test_is_reset(self, sample_handler):
        assert sample_handler.inventory[123]['quantity'] == 50
        sample_handler.purchase({'money':100, 'items':[123]})
        assert sample_handler.inventory[123]['quantity'] == 49
        assert len(sample_handler.purchase_logs) == 1
        sample_handler.reset()
        assert sample_handler.inventory[123]['quantity'] == 50
        assert len(sample_handler.purchase_logs) == 0

    def test_multiple_reset(self, sample_handler):
        # just to be confident in the deepcopy logic and not mutating the original
        for i in range(0, 5):
            assert sample_handler.inventory[123]['quantity'] == 50
            sample_handler.purchase({'money':100, 'items':[123]})
            assert sample_handler.inventory[123]['quantity'] == 49
            assert len(sample_handler.purchase_logs) == 1
            sample_handler.reset()
            assert sample_handler.inventory[123]['quantity'] == 50
            assert len(sample_handler.purchase_logs) == 0

class TestGetLogs:
    def test_purchase_logged(self, sample_handler):
        assert len(sample_handler.get_purchase_logs()[0].json) == 0
        purchase_order = {'money':100, 'items':[123]}
        sample_handler.purchase(purchase_order)
        assert sample_handler.get_purchase_logs()[0].json[0] == purchase_order
