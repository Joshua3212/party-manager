import os

from huddu import Store

store = Store(
    store_token=os.getenv("huddu_store_token".upper()),
    space_id=os.getenv("huddu_space_id".upper()),
    region=os.getenv("huddu_region".upper()),
)

config = store.get("config")