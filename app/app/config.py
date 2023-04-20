import json
import os

from huddu import Store

store = Store(
    client_id="7ba6acae-84f9-4dc1-bba1-a86f6e4f91d2",
    client_secret=os.getenv("STORE_SECRET"),
)

try:
    config = json.loads(store.get("config"))

except:
    config = store.get("config")
if not config:
    raise Exception("No config set in Store!")
