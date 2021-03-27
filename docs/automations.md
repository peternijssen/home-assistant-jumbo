# Automation Examples

## 24 hour warning before your order closes
If you want a 24 hour warning up front before your delivery is being processed (A [Date & Time Sensor](https://www.home-assistant.io/integrations/time_date/) is required):
```
- alias: jumbo_24h_warning
  initial_state: "on"
  trigger:
    platform: template
    value_template: "{% if state_attr('sensor.jumbo_delivery', 'deliveries') %}{{ (state_attr('sensor.jumbo_delivery', 'deliveries')[0].cut_off_date.timestamp() - 86400) == strptime(states('sensor.date_time'), '%Y-%m-%d, %H:%M').timestamp() }}{% endif %}"
  action:
    service: notify.all_devices
    data:
      title: "Jumbo"
      message: "Je hebt nog 24 uur voordat je bestelling wordt verwerkt. Is je bestelling compleet?"
```

## 1 hour warning before your order closes
If you want a 1 hour warning up front before your delivery is being processed while you still have items in your basket (A [Date & Time Sensor](https://www.home-assistant.io/integrations/time_date/) is required):
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
    service: notify.all_devices
    data:
      title: "Jumbo"
      message: "Je hebt nog 1 uur om je bestelling bij de Jumbo aan te passen. Er staan nog {{ states('sensor.jumbo_basket') }} producten in je mandje."
```
#### Notification that your order is being processed
If you want to get a notification when you delivery order is being processed:
```
- alias: jumbo_delivery_processing
  initial_state: "on"
  trigger:
    platform: state
    entity_id: sensor.jumbo_delivery
    from: 'open'
    to: 'processing'
  action:
    service: notify.all_devices
    data:
      title: "Jumbo"
      message: "De Jumbo verwerkt momenteel je bestelling. Je levering wordt op {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].date }}{% endraw %} tussen {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].start_time }}{% endraw %} en {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].end_time }}{% endraw %} verwacht."
```

## Notification that your order is on it's way
If you want to get a notification when you delivery order is ready for delivery:
```
- alias: jumbo_delivery_ready
  initial_state: 'on'
  trigger:
    platform: state
    entity_id: sensor.jumbo_delivery
    from: 'processing'
    to: 'ready_to_deliver'
  action:
    service: notify.all_devices
    data:
      title: "Jumbo"
      message: "De Jumbo heeft je bestelling verwerkt. Hij is nu klaar voor vertrek en wordt verwacht tussen {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_start }}{% endraw %} en {% raw %}{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_end }}{% endraw %}."
```

## Notification when the live arrival time is known
If you want to get a notification what the expected arrival time is:
```
- alias: jumbo_delivery_live
  initial_state: 'on'
  trigger:
    platform: state
    entity_id: sensor.jumbo_live
    from: 'unknown'
  action:
    service: notify.all_devices
    data:
      title: "Jumbo"
      message: "Je bestelling is er bijna! De verwachting is dat hij er om {{ states('sensor.jumbo_live') }} zal zijn."
```