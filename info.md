## Home Assistant sensor component for Jumbo.com

Provides Home Assistant sensors for Jumbo.com (Dutch Supermarket).
See the [repository](https://github.com/peternijssen/home-assistant-jumbo) for automation examples.

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
