"""Common utils for yi-hack cam."""

from datetime import timedelta
import logging

import requests
from requests.auth import HTTPBasicAuth

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
)
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    END_OF_POWER_OFF,
    END_OF_POWER_ON,
    HTTP_TIMEOUT,
    PRIVACY,
)

_LOGGER = logging.getLogger(__name__)


def get_status(config):
    """Get system status from camera."""
    error = False
    try:
        response = call_api(config, "status.json", None)
    except:
        error = True
    if error:
        return None
    return response.json()

def get_system_conf(config):
    """Get system configuration from camera."""
    response = None
    response = call_api(config, "get_configs.sh", "conf=system")
    if response is None:
        return None
    return response.json()

def get_mqtt_conf(config):
    """Get mqtt configuration from camera."""
    response = None
    response = call_api(config, "get_configs.sh", "conf=mqtt")
    if response is None:
        return None
    return response.json()

def get_privacy(hass, device_name, config=None):
    """Get status of privacy from device."""
    # Privacy is true when the cam is off
    if power_off_in_progress(hass, device_name):
        return True
    # Privacy is false when the cam is on
    if power_on_in_progress(hass, device_name):
        return False

    if config is None:
        return hass.data[DOMAIN][device_name][PRIVACY]
    error = False
    response = call_api(config, "privacy.sh", "value=status")
    if response is not None and response:
        try:
            privacy_dict: dict = response.json()
            privacy: str = privacy_dict.get("status")
        except KeyError:
            _LOGGER.error("Response does not have key `status` on device %s", host)
            error = True
    else:
        _LOGGER.error("Failed to get status on device %s: error unknown", host)
        error = True

    if error:
        return None


    if privacy != "on":
        # Update local var
        hass.data[DOMAIN][device_name][PRIVACY] = False
        return False

    # Update local var
    hass.data[DOMAIN][device_name][PRIVACY] = True

    return True

def set_privacy(hass, device_name, newstatus, config=None):
    """Set status of privacy to device. Return true if web service completes successfully."""
    if config is None:
        hass.data[DOMAIN][device_name][PRIVACY] = newstatus
        return
    error = False
    if newstatus:
        newstatus_string = "on"
    else:
        newstatus_string = "off"
    response = call_api(config, "privacy.sh", "value=" + newstatus_string)
    if response is not None and response:
        try:
            if response.json()["status"] != "on" and response.json()["status"] != "off":
                _LOGGER.error("Returned status is neither on nor off on device %s", host)
                error = True
        except KeyError:
            _LOGGER.error("Response does not have key `status` on device %s", host)
            error = True
        except requests.exceptions.JSONDecodeError:
            _LOGGER.error("Invalid JSON returned: %s on device %s", response.text, host)
            error = True
    else:
        _LOGGER.error("Failed to switch on device %s: error unknown", host)
        error = True
    if error:
        return False
    hass.data[DOMAIN][device_name][PRIVACY] = newstatus
    return True

def set_power_off_in_progress(hass, device_name):
    device_conf = get_device_conf(hass, device_name)
    device_conf[END_OF_POWER_OFF] = dt_util.utcnow() + timedelta(seconds=5)

def power_off_in_progress(hass, device_name):
    device_conf = get_device_conf(hass, device_name)
    return (
        device_conf[END_OF_POWER_OFF] is not None
        and device_conf[END_OF_POWER_OFF] > dt_util.utcnow()
    )

def set_power_on_in_progress(hass, device_name):
    device_conf = get_device_conf(hass, device_name)
    device_conf[END_OF_POWER_ON] = dt_util.utcnow() + timedelta(seconds=5)

def power_on_in_progress(hass, device_name):
    device_conf = get_device_conf(hass, device_name)
    return (
        device_conf[END_OF_POWER_ON] is not None
        and device_conf[END_OF_POWER_ON] > dt_util.utcnow()
    )

def get_device_conf(hass, device_name, param=None):
    if param is None:
        return hass.data[DOMAIN][device_name]
    return hass.data[DOMAIN][device_name][param]

def call_api(config, api_name, query_string):
    """ Send HTTP GET request to API under /cgi-bin with a query string"""
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    user = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    error = False
    auth = None
    if user or password:
        auth = HTTPBasicAuth(user, password)
    response = None
    if query_string is None:
        query_string = ""
    else:
        query_string = "?" + query_string
    try:
        full_url = "http://" + host + ":" + str(port) + "/cgi-bin/" + api_name + query_string
        _LOGGER.debug("call_api: full_url: `%s`", full_url)
        response = requests.get(full_url, timeout=HTTP_TIMEOUT, auth=auth)
        if response.status_code >= 300:
            _LOGGER.error("unexpected HTTP status code by %s API on device %s (status: %d)", api_name, host, response.status_code)
            error = True
    except (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout) as e:
        _LOGGER.error("%s API timed out on %s (%d sec), %s", api_name, host, HTTP_TIMEOUT, e)
        error = True
    except:
        _LOGGER.error("%s API failed on device %s: error %s", api_name, host, e)
        error = True
    if error:
        return None
    return response
