# Description
[![Build Status](https://drone.io/github.com/denis4net/onliner-agent/status.png)](https://drone.io/github.com/denis4net/onliner-agent/latest)
Simple rent.onliner.by poller that notify you about new ready-for-sale apartments.

# System dependencies
```
apt-get install -y -qq python3 python3-pip
```

# Deploying
```
pip3 install -r requirements.txt
cp config.json.sample config.json
```


Edit configuration file (add a bot token: https://core.telegram.org/bots#3-how-do-i-create-a-bot) to `config.json` and launch:
```
python3 poller.py --config config.json
```
