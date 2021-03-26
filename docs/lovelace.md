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