
## Home Assisant sensor component for Jumbo.com

Provides Home Assistant sensors for Jumbo.com (Dutch Supermarket)

### Install
Use HACS to isntall these sensors or copy the files in the /custom_components/jumbo/ folder to [homeassistant]/config/custom_components/jumbo/

Example config:

```yaml
  sensor:
    - platform: jumbo
      username: <username>            (required)
      password: <password>            (required)
```

### Usage
Two sensors will be created:

#### Basket
The sensor `jumbo_basket` indicates how many items you still have within your basket at this point.

#### Orders
The sensor `jumbo_orders` indicates when your next order is expected. Within the attributes, you can also see any future orders.

### Debugging
If you experience unexpected output, please create an issue with additional logging. You can add the following lines to enable logging

```
logger:
  default: info
  logs:
      custom_components.jumbo: debug
```