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

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=60)

_LOGGER = logging.getLogger(__name__)

BASKET_ICON = "mdi:basket"
BASKET_NAME = "jumbo_basket"

ORDER_ICON = "mdi:truck-delivery"
ORDER_NAME = "jumbo_orders"

TIME_SLOT_ICON = "mdi:calendar-clock"
TIME_SLOT_NAME = "jumbo_time_slots"

VERSION = '0.4.0'

ATTRIBUTION = "Information provided by Jumbo.com"

ATTR_ATTRIBUTION = "attribution"
ATTR_ORDERS = "orders"
ATTR_TIME_SLOTS = "time_slots"
ATTR_PRICE = "price"

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
    async_add_entities([TimeSlotSensor(data)], True)


class JumboData:
    """Handle Jumbo data object"""

    def __init__(self, hass, config, api):
        """Initialize the data object."""
        self._api = api
        self.basket = None
        self.open_deliveries = {}
        self.closed_deliveries = {}
        self.open_time_slots = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update data."""
        _LOGGER.debug("Updating Jumbo data")
        self.basket = self._api.get_basket()
        self.open_deliveries = self._api.get_open_deliveries()
        self.closed_deliveries = self._api.get_closed_deliveries()
        self.open_time_slots = self._api.get_open_time_slots()


class BasketSensor(Entity):
    """Basket Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_PRICE: None,
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._state = self._data.basket.amount
        self._attributes[ATTR_PRICE] = vars(self._data.basket.price)

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
            ### TODO: Not happy with this solution
            p = vars(order.price)
            order.price = p
            self._attributes[ATTR_ORDERS].append(vars(order))

        if len(orders) > 0:
            first = next(iter(orders))
            self._state = first.delivery_date + " " + first.delivery_time
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


class TimeSlotSensor(Entity):
    """Time Slot Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_TIME_SLOTS: [],
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_TIME_SLOTS] = []
        self._state = None

        time_slots = self._data.open_time_slots
        for time_slot in time_slots:
            ### TODO: Not happy with this solution
            p = vars(time_slot.price)
            time_slot.price = p
            self._attributes[ATTR_TIME_SLOTS].append(vars(time_slot))

        if len(time_slots) > 0:
            first = next(iter(time_slots))
            self._state = first.start_date_time
        else:
            self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return TIME_SLOT_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return TIME_SLOT_ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
