# Shoppy McShopface
This is a very simple inventory-tracking application with no persistent storage.

# Running it 

## Locally

1.) Install the dependencies with `pip install -r requirements.txt`
2.) Run the flask app with `FLASK_APP=shoppy.py flask run`
3.) Make sure you're running- `curl localhost:5000/status`

## In Docker

`docker build . -t shoppy` then `docker run shoppy -p 5000:5000`

# Running Tests

`python -m pytest tests`

Use -k to match test class or method names and run specific tests.

# Expected Inventory JSON

The initial JSON of inventory is expected to contain an array of dictionaries representing unique items in inventory. Each item should have an id, name, price, and quantity in stock.

For example:

`[{'id':0, 'name':'potato', 'price': .40, 'quantity':1000}, {'id':1, 'name':'carrot', 'price': 1.20, 'quantity': 5}]`

By default, the app will use the included sample .json file- to override this set the environment variable INVENTORY_JSON_PATH to a path to your custom file in this format.

# Endpoints

## /inventory

### GET
Returns an array of items in the same structure as the original input JSON (each item has an id, price, name, and quantity)

## /purchase

### POST
Expects two keys: money, which is a numeric ammount of money to be sent, and items, which is an array of item ids to be purchased. 

Example payload: `{"money": 1000, "items": [0, 1, 1, 1]}`

Returns an object containing a single key, "change" on success. Otherwise, returns an error if insufficient money was sent, ids do not exist, etc.

## /price_check

### POST
Expects one key, "items", which is an array of item ids to be purchased.

Example payload: `{ "items": [0, 1, 1, 1]}`

## /reset

### DELETE
Resets the state of the inventory system to the data from the original JSON. Returns the new inventory.

## /logs

### GET
Returns an array of the purchases POSTed to /purchase

# Known Issues and TODOs
* Don't just store everything in memory while this is running
* Would like to handle merging items in inventory with the same id
* Should use a real server and not the flask dev server 
* Read config from environment-specific files and/or the environment
* Should be able to dump inventory to JSON
* The purchase logs could be more descriptive and easier to validate (for example, include the remaining inventory after each purchase in the logs)
* Probably should add some custom exceptions for insufficient money, etc.
* Need to add validation of user JSON payloads (for example make sure "items" key exists)
* Allow bulk purchase of many items with count instead of array of ids
* More specific insufficient inventory message
* Handle bad inputs- negative money, strings instead of numerics, etc.
