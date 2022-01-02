"""Support for Jumbo sensors."""

import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from jumbo_api.jumbo_api import JumboApi, UnauthorizedException

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

_LOGGER = logging.getLogger(__name__)

CONF_FULFILMENT_TYPE = "type"

BASKET_ICON = "mdi:basket"
BASKET_NAME = "jumbo_basket"

LIVE_ICON = "mdi:progress-clock"
LIVE_NAME = "jumbo_live"

DELIVERY_ICON = "mdi:truck-delivery"
DELIVERY_NAME = "jumbo_delivery"

PICK_UP_ICON = "mdi:store"
PICK_UP_NAME = "jumbo_pick_up"

DELIVERY_TIME_SLOT_ICON = "mdi:calendar-clock"
DELIVERY_TIME_SLOT_NAME = "jumbo_delivery_time_slots"

PICK_UP_TIME_SLOT_ICON = "mdi:calendar-clock"
PICK_UP_TIME_SLOT_NAME = "jumbo_pick_up_time_slots"

ATTRIBUTION = "Information provided by Jumbo.com"

ATTR_ATTRIBUTION = "attribution"
ATTR_DELIVERIES = "deliveries"
ATTR_PICK_UPS = "pick_ups"
ATTR_TIME_SLOTS = "time_slots"
ATTR_PRICE = "price"
ATTR_ETA_START = "eta_start"
ATTR_ETA_END = "eta_end"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_FULFILMENT_TYPE, default='both'): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Jumbo sensor."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    fulfilment_type = config.get(CONF_FULFILMENT_TYPE)

    api = JumboApi(username, password)
    data = JumboData(hass, config, api)

    async_add_entities([BasketSensor(data)], True)

    if fulfilment_type in ['delivery', 'both']:
        async_add_entities([LiveSensor(data)], True)
        async_add_entities([DeliverySensor(data)], True)
        async_add_entities([DeliveryTimeSlotSensor(data)], True)

    if fulfilment_type in ['pick_up', 'both']:
        async_add_entities([PickUpSensor(data)], True)
        async_add_entities([PickUpTimeSlotSensor(data)], True)


class JumboData:
    """Handle Jumbo data object"""

    def __init__(self, hass, config, api):
        """Initialize the data object."""
        self._api = api
        self.hass = hass
        self.basket = None
        self.open_deliveries = {}
        self.open_pick_ups = {}
        self.open_delivery_time_slots = {}
        self.open_pick_up_time_slots = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update data."""
        await self.hass.async_add_executor_job(self._get_data)

    def _get_data(self):
        try:
            self.basket = self._api.get_basket()
            self.open_deliveries = self._api.get_open_deliveries()
            self.open_pick_ups = self._api.get_open_pick_ups()
            self.open_delivery_time_slots = self._api.get_open_delivery_time_slots()
            self.open_pick_up_time_slots = self._api.get_open_pick_up_time_slots()
            _LOGGER.debug("Updated data from Jumbo")
        except UnauthorizedException:
            _LOGGER.error("Can't connect to the Jumbo API. Is your username/password valid?")


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

    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        if self._data.basket is None:
            return

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
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class LiveSensor(Entity):
    """Live Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_ETA_START: None,
            ATTR_ETA_END: None
        }

    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_ETA_START] = None
        self._attributes[ATTR_ETA_END] = None
        self._state = None

        deliveries = self._data.open_deliveries
        if len(deliveries) == 0:
            return

        delivery = next(iter(deliveries))
        self._state = delivery.eta_live
        self._attributes[ATTR_ETA_START] = delivery.eta_start
        self._attributes[ATTR_ETA_END] = delivery.eta_end

    @property
    def name(self):
        """Return the name of the sensor."""
        return LIVE_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return LIVE_ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class DeliverySensor(Entity):
    """Delivery Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_DELIVERIES: [],
        }

    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_DELIVERIES] = []
        self._state = None

        deliveries = self._data.open_deliveries
        for delivery in deliveries:
            # TODO: Not happy with this solution
            if not isinstance(delivery.price,dict):
                p = vars(delivery.price)
                delivery.price = p
            self._attributes[ATTR_DELIVERIES].append(vars(delivery))

        if len(deliveries) > 0:
            first = next(iter(deliveries))
            self._state = first.status.lower()
        else:
            self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return DELIVERY_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return DELIVERY_ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class PickUpSensor(Entity):
    """Pick Up Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_PICK_UPS: [],
        }

    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_PICK_UPS] = []
        self._state = None

        pick_ups = self._data.open_pick_ups
        for pick_up in pick_ups:
            # TODO: Not happy with this solution
            if not isinstance(pick_up.price,dict):
                p = vars(pick_up.price)
                pick_up.price = p
            self._attributes[ATTR_PICK_UPS].append(vars(pick_up))

        if len(pick_ups) > 0:
            first = next(iter(pick_ups))
            self._state = first.status.lower()
        else:
            self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return PICK_UP_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return PICK_UP_ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class DeliveryTimeSlotSensor(Entity):
    """Delivery Time Slot Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_TIME_SLOTS: [],
        }

    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_TIME_SLOTS] = []
        self._state = None

        time_slots = self._data.open_delivery_time_slots
        for time_slot in time_slots:
            # TODO: Not happy with this solution
            if not isinstance(time_slot.price,dict):
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
        return DELIVERY_TIME_SLOT_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return DELIVERY_TIME_SLOT_ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class PickUpTimeSlotSensor(Entity):
    """Pick Up Time Slot Sensor class."""

    def __init__(self, data):
        self.attr = {}
        self._state = None
        self._data = data
        self._attributes = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_TIME_SLOTS: [],
        }

    async def async_update(self):
        """Update the sensor."""
        await self._data.async_update()

        self._attributes[ATTR_TIME_SLOTS] = []
        self._state = None

        time_slots = self._data.open_pick_up_time_slots
        for time_slot in time_slots:
            # TODO: Not happy with this solution
            if not isinstance(time_slot.price,dict):
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
        return PICK_UP_TIME_SLOT_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return PICK_UP_TIME_SLOT_ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
