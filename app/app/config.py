import os

from huddu import Store

store = Store(token=os.getenv("STORE_TOKEN"))

config = store.get("config")
