import os

from huddu import Store

store = Store(client_id="405d22fe-3a2f-404c-bcf2-5cd73b9fa057", client_secret=os.getenv("STORE_SECRET"))

config = store.get("config")

if not config:
    raise Exception("No config set in Store!")
