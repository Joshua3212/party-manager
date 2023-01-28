# party-manager

A dead simple ticketing system

### Required Envvars

- HUDDU_STORE_TOKEN
- HUDDU_SPACE_ID
- HUDDU_REGION

### Party Manager Config

The config is supposed to be saved in Huddu Store with the id **config**
it should look something like this:

    {
        "users": [
            {
                "username": "user1",
                "password": "password1
            }
        ]
    }