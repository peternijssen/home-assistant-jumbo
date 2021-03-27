# Lovelace
This markdown card automatically displays information based on the state of your order and your basket.
```
- type: markdown
  content: >
      {% if state_attr('sensor.jumbo_delivery', 'deliveries') %}
        {% if states('sensor.jumbo_delivery') == 'open' %}
        De volgende Jumbo levering is op **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].date }}** tussen **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].time }}**.
        Je kunt je bestelling nog aanpassen tot **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].cut_off_date }}**
        {% elif states('sensor.jumbo_delivery') == 'processing'  %}
        Je bestelling wordt verwacht tussen **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].start_time }}** en **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].end_time }}** op **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].date }}**
        {% elif states('sensor.jumbo_delivery') == 'ready_to_deliver' %}
        Je bestelling wordt geleverd tussen **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_start }}** en **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_end }}**. Waarschijnlijk rond **{{ state_attr('sensor.jumbo_delivery', 'deliveries')[0].eta_live }}**.
        {% endif %}            
      {% endif %}
      {% if states('sensor.jumbo_basket') != 0 %}
        Je hebt nog **{{ states('sensor.jumbo_basket') }}** producten in je winkelmandje met een totale waarde van **{{ state_attr('sensor.jumbo_basket', 'price').format }}**
      {% endif %}
```

This markdown card only shows you information when the driver is en route.

```
- type: markdown
  content: >
      {% if states('sensor.jumbo_live') != 'Unknown' %}
        Goed nieuws! De Jumbo is onderweg en verwacht er om **{{ states('sensor.jumbo_live') }}** te zijn. 
      {% endif %}
```

## Card
A dedicated lovelace card was created by [@Voxxie](https://github.com/Voxxie), which can be found within HACS or [here](https://github.com/Voxxie/lovelace-jumbo-card).