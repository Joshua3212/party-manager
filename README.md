# party-manager

A dead simple ticketing system

### Required Envvars

- HUDDU_SECRET

### Party Manager Config

The config is supposed to be saved in Huddu Store with the id **config**
it should look something like this:

    {
        "teams": [
            {
                "name": "team1",
                "password": "password1"
            }
        ]
    }