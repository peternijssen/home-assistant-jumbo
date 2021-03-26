# Home Assistant component for Jumbo.com

[![](https://img.shields.io/github/release/peternijssen/home-assistant-jumbo.svg?style=flat-square)](https://github.com/peternijssen/home-assistant-jumbo/releases/latest)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) 

Provides Home Assistant sensors for [Jumbo](https://www.jumbo.com) (Dutch Supermarket) based on the [python-jumbo-api](https://github.com/peternijssen/python-jumbo-api) repository.

This library is not affiliated with [Jumbo](https://www.jumbo.com) and retrieves data from the endpoints of the mobile application. Use at your own risk.

## Install
Use [HACS](https://hacs.xyz/) to install these sensors or copy the files in the /custom_components/jumbo/ folder to [homeassistant]/config/custom_components/jumbo/

Example config:

```yaml
  sensor:
    - platform: jumbo
      username: <username>            (required)
      password: <password>            (required)
      type: "both"                    (optional) (Choose from "delivery", "pick_up" or "both")
```

## Documentation
* [Sensors](docs/sensors.md)
* [States](docs/states.md)
* [Automation Examples](docs/automations.md)
* [Lovelace Examples](docs/lovelace.md)
* [Debugging](docs/debug.md)

## Questions / Feedback
Share your thoughts within [this topic](https://community.home-assistant.io/t/jumbo-com-integration-dutch-supermarket/190438).

## Contributors
* [Peter Nijssen](https://github.com/peternijssen)
