"""Support for Jumbo sensors."""

import logging
from datetime import timedelta

from jumbo_api.jumbo_api import JumboApi, UnauthorizedException
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=4)

_LOGGER = logging.getLogger(__name__)

BASKET_ICON = "mdi:basket"
BASKET_NAME = "jumbo_basket"

ORDER_ICON = "mdi:calendar-clock"
ORDER_NAME = "jumbo_orders"

VERSION = '0.1.0'

ATTRIBUTION = "Information provided by Jumbo.com"

ATTR_ATTRIBUTION = "attribution"
ATTR_ORDERS = "orders"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Jumbo sensor."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    try:
        api = JumboApi(username, password)
        _LOGGER.debug("Connection with Jumbo API succeeded")

    except UnauthorizedException:
        _LOGGER.exception("Can't connect to the Jumbo API")
        return

    data = JumboData(hass, config, api)

    async_add_entities([BasketSensor(data)], True)
    async_add_entities([OrderSensor(data)], True)


class JumboData:
    """Handle Jumbo data object"""
    def __init__(self, hass, config, api):
        """Initialize the data object."""
        self._api = api
        self.basket = None
        self.open_deliveries = {}
        self.closed_deliveries = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update data."""
        _LOGGER.debug("Updating Jumbo data")
        self.basket = self._api.get_basket()
        self.open_deliveries = self._api.get_open_deliveries()
        self.closed_deliveries = self._api.get_closed_deliveries()


class BasketSensor(Entity):
    """Basket Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()
        
        self._state = self._data.basket.amount

    @property
    def name(self):
        """Return the name of the sensor."""
        return BASKET_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return BASKET_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class OrderSensor(Entity):
    """Order Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_ORDERS: [],
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_ORDERS] = []
        self._state = None

        orders = self._data.open_deliveries
        for order in orders:
            self._attributes[ATTR_ORDERS].append(vars(order))

        if len(orders) > 0:
            first = next(iter(orders))
            self._state = first.delivery_date
        else:
            self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return ORDER_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ORDER_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
