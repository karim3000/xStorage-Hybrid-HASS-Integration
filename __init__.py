"""The Eaton xStorage Hybrid integration."""
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_HOST, CONF_PORT, DOMAIN

# Logger for this component
_LOGGER = logging.getLogger(__name__)

# List of platforms to support
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eaton xStorage Hybrid from a config entry.
    
    This function is called when a config entry is being set up.
    It initializes the connection to the device and sets up platforms.
    
    Args:
        hass: Home Assistant instance
        entry: The config entry being set up
        
    Returns:
        bool: True if setup was successful, False otherwise
    """
    _LOGGER.debug("Setting up xStorage Hybrid integration")
    
    # Get configuration from entry
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    
    # Store configuration data in hass.data for access by platforms
    # This creates a nested dictionary structure: hass.data[DOMAIN][entry.entry_id]
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_HOST: host,
        CONF_PORT: port,
    }
    
    # Set up all platforms (in this case, just sensor)
    # This will call async_setup_entry in sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info("Successfully set up xStorage Hybrid at %s:%s", host, port)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.
    
    This function is called when a config entry is being removed.
    It cleans up all platforms and stored data.
    
    Args:
        hass: Home Assistant instance
        entry: The config entry being unloaded
        
    Returns:
        bool: True if unload was successful
    """
    _LOGGER.debug("Unloading xStorage Hybrid integration")
    
    # Unload all platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # Remove stored data if unload was successful
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Successfully unloaded xStorage Hybrid integration")
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry.
    
    This function handles reloading the integration when configuration changes.
    
    Args:
        hass: Home Assistant instance
        entry: The config entry being reloaded
    """
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
