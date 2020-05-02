
# Home Assisant sensor component for Jumbo.com

Provides Home Assistant sensors for Jumbo (Dutch Supermarket).
This library is not affiliated with Jumbo and retrieves data from the endpoints of the mobile application. Use at your own risk.

## Install
Use HACS to install these sensors or copy the files in the /custom_components/jumbo/ folder to [homeassistant]/config/custom_components/jumbo/

Example config:

```yaml
  sensor:
    - platform: jumbo
      username: <username>            (required)
      password: <password>            (required)
      type: "both"                    (optional) (Choose from "delivery", "pick_up" or "both")
```

## Sensors
Depending on the type you defined, you will get several sensors.

#### Basket
The sensor `jumbo_basket` indicates how many items you still have within your basket. Within the more dialog window you will also see the outstanding costs that you have.

#### Deliveries
The sensor `jumbo_delivery` indicates the state of your next upcoming delivery. The states are `open`, `processing` and `ready_to_deliver`.
Within the attributes (more info dialog), you can also see any future deliveries.

The sensor `jumbo_delivery_time_slots` indicates the next available delivery time slot. Within the attributes (more info dialog), you can also see any future delivery time slots.

#### Pick ups
The sensor `jumbo_pick_up` indicates the state of your next upcoming pick up. The states are `open`, `processing` and `ready_to_pick_up`.
Within the attributes (more info dialog), you can also see any future pick ups.

The sensor `jumbo_pick_up_time_slots` indicates the next available pick up time slot. Within the attributes (more info dialog), you can also see any future pick up time slots.

## Automation Examples (Untested!)
If you want to know when you delivery order is being processed:
```
- alias: jumbo_delivery_processing
  initial_state: "on"
  trigger:
    platform: state
    entity_id: sensor.jumbo_delivery
    to: 'processing'
  action:
    service: notify.telegram_peter
    data_template:
      title: "Jumbo"
      message: "De Jumbo verwerkt momenteel je bestelling. Je levering wordt tussen {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].time }}{% endraw %} verwacht"
```

If you want to know when you delivery order is ready for delivery:
```
- alias: jumbo_delivery_ready
  initial_state: 'on'
  trigger:
    platform: state
    entity_id: sensor.jumbo_delivery
    to: "ready_to_deliver"
  action:
    - service: notify.telegram_peter
      data:
        title: "Jumbo"
        message: "De Jumbo heeft je bestelling verwerkt. Hij is nu klaar voor vertrek!"
```

## Community
Share your thoughts  within [this topic](https://community.home-assistant.io/t/jumbo-com-integration-dutch-supermarket/190438).

## Lovelace Card
A dedicated lovelace card was created by @Voxxie, which can be found within HACS or [here](https://github.com/Voxxie/lovelace-jumbo-card).

## Debugging
If you experience unexpected output, please create an issue with additional logging. You can add the following lines to enable logging

```
logger:
  default: info
  logs:
      custom_components.jumbo: debug
```

## Contributors
* [Peter Nijssen](https://github.com/peternijssen)
