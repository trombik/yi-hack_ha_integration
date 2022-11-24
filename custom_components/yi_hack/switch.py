"""Support for yi-hack privacy switch."""

import asyncio
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import (CONF_HOST, CONF_MAC, CONF_NAME,
                                 CONF_PASSWORD, CONF_PORT, CONF_USERNAME)
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .common import (get_privacy, set_power_off_in_progress,
                     set_power_on_in_progress, set_privacy)
from .const import (DEFAULT_BRAND, DOMAIN, CONF_HACK_NAME,
                    DEFAULT_BRAND, MSTAR, ALLWINNER, ALLWINNERV2,
                    V5, SONOFF)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities):
    """Set up the Yi Camera media player from a config entry."""
    entities = []

    if (config.data[CONF_HACK_NAME] == DEFAULT_BRAND) or (config.data[CONF_HACK_NAME] == MSTAR):
        entities = [
            YiHackSwitch(config, "motion_detection"),
            YiHackSwitch(config, "baby_crying"),
        ]
    elif (config.data[CONF_HACK_NAME] == ALLWINNER) or (config.data[CONF_HACK_NAME] == V5):
        entities = [
            YiHackSwitch(config, "motion_detection"),
            YiHackSwitch(config, "baby_crying"),
            YiHackSwitch(config, "sound_detection"),
        ]
    elif (config.data[CONF_HACK_NAME] == ALLWINNERV2):
        entities = [
            YiHackSwitch(config, "motion_detection"),
            YiHackSwitch(config, "human_detection"),
            YiHackSwitch(config, "baby_crying"),
            YiHackSwitch(config, "sound_detection"),
        ]
    elif config.data[CONF_HACK_NAME] == SONOFF:
        entities = [
            YiHackSwitch(config, "motion_detection"),
        ]
    async_add_entities(entities)

class YiHackSwitch(SwitchEntity):
    """Representation of Yi Camera Switches."""

    def __init__(self, config, switch_type):
        """Initialize the switch."""
        self._device_name = config.data[CONF_NAME]
        self._mac = config.data[CONF_MAC]
        self._host = config.data[CONF_HOST]
        self._port = config.data[CONF_PORT]
        self._user = config.data[CONF_USERNAME]
        self._password = config.data[CONF_PASSWORD]
        self._state = False

        if switch_type == "motion_detection":
            self._unique_id = self._device_name + "_swmd"
        elif switch_type == "human_detection":
            self._unique_id = self._device_name + "_swhd"
        elif switch_type == "baby_crying":
            self._unique_id = self._device_name + "_swbc"
        elif switch_type == "sound_detection":
            self._unique_id = self._device_name + "_swsd"
        elif switch_type == "privacy":
            self._unique_id = self._device_name + "_swpr"
        else:
            raise HomeAssistantError(
                f"Unknown switch type: {switch_type}"
            )
        self._name = self._device_name + "_" + switch_type
        self._config = dict([
            (CONF_HOST, self._host),
            (CONF_PORT, self._port),
            (CONF_USERNAME, self._user),
            (CONF_PASSWORD, self._password),
        ])


    def update(self):
        """Return the state of the switch."""
        if self._unique_id.endswith("_swpr"):
            self._state = get_privacy(self.hass, self._device_name, self._config)
        elif self._unique_id.endswith("_swmd"):
            pass
        elif self._unique_id.endswith("_swhd"):
            pass
        elif self._unique_id.endswith("_swbc"):
            pass
        elif self._unique_id.endswith("_swsd"):
            pass
        else:
            _LOGGER.error("Unknown _unique_id: `%s`", self._unique_id)

    def turn_off(self):
        """Turn off the switch"""
        if self._unique_id.endswith("_swpr"):
            if get_privacy(self.hass, self._device_name):
                _LOGGER.debug("Turn off privacy, camera %s", self._name)
                # Turn off the privacy switch:
                # power on the cam and set privacy false
                set_power_on_in_progress(self.hass, self._device_name)
                set_privacy(self.hass, self._device_name, False, self._config)
                self._state = False
                self.schedule_update_ha_state(force_refresh=True)
        elif self._unique_id.endswith("_swmd"):
            pass
        elif self._unique_id.endswith("_swhd"):
            pass
        elif self._unique_id.endswith("_swbc"):
            pass
        elif self._unique_id.endswith("_swsd"):
            pass
        else:
            _LOGGER.error("Unknown _unique_id: `%s`", self._unique_id)

    def turn_on(self):
        """Turn on the switch."""
        if self._unique_id.endswith("_swpr"):
            if not get_privacy(self.hass, self._device_name):
                _LOGGER.debug("Turn on privacy, camera %s", self._name)
                # Turn on the privacy switch:
                # power off the cam and set privacy true
                set_power_off_in_progress(self.hass, self._device_name)
                set_privacy(self.hass, self._device_name, True, self._config)
                self._state = True
                self.schedule_update_ha_state(force_refresh=True)
        elif self._unique_id.endswith("_swmd"):
            pass
        elif self._unique_id.endswith("_swhd"):
            pass
        elif self._unique_id.endswith("_swbc"):
            pass
        elif self._unique_id.endswith("_swsd"):
            pass
        else:
            _LOGGER.error("Unknown _unique_id: `%s`", self._unique_id)

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def brand(self):
        """Camera brand."""
        return DEFAULT_BRAND

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the device."""
        return self._unique_id

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "name": self._device_name,
            "connections": {(CONNECTION_NETWORK_MAC, self._mac)},
            "identifiers": {(DOMAIN, self._mac)},
            "manufacturer": DEFAULT_BRAND,
            "model": DOMAIN,
        }
