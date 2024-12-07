# Purpose
On request from Chainlink:

Crawls a local copy of [registry.json](https://github.com/balancer/code-review/blob/main/erc4626/registry.json) and generates a CSV of chainlink feeds referenced by rate providers.  


# Instructions
Requires a DRPC API key stored in DRPC
`export DRPC_KEY=!!SECRET!!`
Then grab the most recent registry.json from the link above and save it into the root of this repo.

Setup a venv and install requirements
```
python3.12 -mvenv venv ## Python 3.11 and 3.10 should work too
pip3 install -r requirements.txt
source venv/bin/activate
```


Run the script
```
python get_feeds.py
```
It will print a lot of stuff, and assuming no errors, check the updated [feeds.csv](./feeds.csv)

