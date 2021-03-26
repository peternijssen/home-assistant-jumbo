## Debugging
If you experience unexpected output, please create an issue with additional logging. You can add the following lines to enable logging

```
logger:
  default: error
  logs:
      custom_components.jumbo: debug
      jumbo_api.jumbo_api: debug
```