# Home Assistant component for Jumbo.com


[![](https://img.shields.io/github/release/peternijssen/home-assistant-jumbo.svg?style=flat-square)](https://github.com/peternijssen/home-assistant-jumbo/releases/latest)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) 

Provides Home Assistant sensors for Jumbo (Dutch Supermarket) based on the [python-jumbo-api](https://github.com/peternijssen/python-jumbo-api) repository.

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

## Automation Examples
If you want a 24h warning up front before your delivery is being processed (A [Date & Time Sensor](https://www.home-assistant.io/integrations/time_date/) is required):
```
- alias: jumbo_24h_warning
  initial_state: "on"
  trigger:
    platform: template
    value_template: "{% if state_attr('sensor.jumbo_delivery', 'deliveries') %}{{ (state_attr('sensor.jumbo_delivery', 'deliveries')[0].cut_off_date.timestamp() - 86400) == strptime(states('sensor.date_time'), '%Y-%m-%d, %H:%M').timestamp() }}{% endif %}"
  action:
    service: notify.telegram_peter
    data:
      title: "Jumbo"
      message: "Je hebt nog 24 uur voordat je bestelling wordt verwerkt. Is de bestelling compleet?"
```

If you want a 1h warning up front before your delivery is being processed while you still have items in your basket (A [Date & Time Sensor](https://www.home-assistant.io/integrations/time_date/) is required):
```
- alias: jumbo_1h_warning
  initial_state: "on"
  trigger:
    platform: template
    value_template: "{% if state_attr('sensor.jumbo_delivery', 'deliveries') %}{{ (state_attr('sensor.jumbo_delivery', 'deliveries')[0].cut_off_date.timestamp() - 3600) == strptime(states('sensor.date_time'), '%Y-%m-%d, %H:%M').timestamp() }}{% endif %}"
  condition:
    condition: numeric_state
    entity_id: 'sensor.jumbo_basket'
    above: 0
  action:
    service: notify.telegram_peter
    data:
      title: "Jumbo"
      message: "Je hebt nog 1 uur om je bestelling bij de Jumbo aan te passen. Er staan nog {{ states('sensor.jumbo_basket') }} producten in je mandje."
```

If you want to know when you delivery order is being processed:
```
- alias: jumbo_delivery_processing
  initial_state: "on"
  trigger:
    platform: state
    entity_id: sensor.jumbo_delivery
    from: 'open'
    to: 'processing'
  action:
    service: notify.telegram_peter
    data_template:
      title: "Jumbo"
      message: "De Jumbo verwerkt momenteel je bestelling. Je levering wordt tussen {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_start }}{% endraw %} en {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_end }}{% endraw %} verwacht"
```

If you want to know when you delivery order is ready for delivery:
```
- alias: jumbo_delivery_ready
  initial_state: 'on'
  trigger:
    platform: state
    entity_id: sensor.jumbo_delivery
    from: 'processing'
    to: 'ready_to_deliver'
  action:
    - service: notify.telegram_peter
      data:
        title: "Jumbo"
        message: "De Jumbo heeft je bestelling verwerkt. Hij is nu klaar voor vertrek en wordt verwacht om {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_live }}{% endraw %}"
```

## Lovelace
A dedicated lovelace card was created by [@Voxxie](https://github.com/Voxxie), which can be found within HACS or [here](https://github.com/Voxxie/lovelace-jumbo-card).

You can also work with the data directly like so:
```
- type: markdown
  content: >
      {% if state_attr('sensor.jumbo_delivery', 'deliveries') %}
        De volgende Jumbo levering is op **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].date }}** tussen **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].time }}**. De huidige status is: **{{ states('sensor.jumbo_delivery') }}**. De totale kosten bedragen **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].price.format }}**. 
        {% if states('sensor.jumbo_delivery') == 'open' %}
        Je kunt je bestelling nog aanpassen tot **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].cut_off_date }}**
        {% elif states('sensor.jumbo_delivery') == 'processing'  %}
        Je bestelling wordt verwacht tussen {{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_start }} en {{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_end }}
        {% elif states('sensor.jumbo_delivery') == 'ready_to_deliver' %}
        Je bestelling wordt geleverd om {{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_live }}
        {% endif %}            
      {% endif %}
      {% if states('sensor.jumbo_basket') != 0 %}
        Je hebt nog **{{ states('sensor.jumbo_basket') }}** producten in je winkelmandje met een totale waarde van **{{ state_attr('sensor.jumbo_basket', 'price').format }}**
      {% endif %}
```

## States
Here is the list through which states a delivery / pick up goes:

| State | Description | When |
|-------|-------------|------|
| open  | You can still change your order | As soon as you open up an order |
| processing | You cannot change your order, but it's not ready yet for delivery / pick up | As soon as the cut off date has been reached |
| ready_to_deliver | Jumbo is about to deliver your order. | As soon as the time slot time is reached |
| ready_to_pick_up | You can almost pick up your order. | As soon as the time slot time is reached. Note: UNTESTED |
| picked_up | The order is closed | As soon as you picked up the order or when the order was delivered |
| cancelled | The order is cancelled | As soon as you cancelled the order |

## Questions / Feedback
Share your thoughts within [this topic](https://community.home-assistant.io/t/jumbo-com-integration-dutch-supermarket/190438).

## Debugging
If you experience unexpected output, please create an issue with additional logging. You can add the following lines to enable logging

```
logger:
  default: error
  logs:
      custom_components.jumbo: debug
      jumbo_api.jumbo_api: debug
```

## Contributors
* [Peter Nijssen](https://github.com/peternijssen)
