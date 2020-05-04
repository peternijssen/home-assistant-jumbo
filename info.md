## BREAKING CHANGE!
If you installed this component prior to 0.5.0, please read the README.md file in the repository and https://community.home-assistant.io/t/jumbo-com-integration-dutch-supermarket/190438/27?u=ptnijssen

## Home Assisant sensor component for Jumbo.com

Provides Home Assistant sensors for Jumbo.com (Dutch Supermarket)

### Example config:

```yaml
  sensor:
    - platform: jumbo
      username: <username>            (required)
      password: <password>            (required)
      type: "both"                    (optional) (Choose from "delivery", "pick_up" or "both")
```

[For more information visit the repository](https://github.com/peternijssen/home-asssistant-jumbo)

### Lovelace Card
A dedicated lovelace card was created by @Voxxie, which can be found within HACS or [here](https://github.com/Voxxie/lovelace-jumbo-card).
