"""Config flow for Eaton xStorage Hybrid integration."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    _LOGGER.info("Validating connection to %s:%s", data[CONF_HOST], data[CONF_PORT])
    return {"title": f"xStorage Hybrid ({data[CONF_HOST]})"}


class XStorageHybridConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eaton xStorage Hybrid.
    
    This class defines the configuration flow that appears in the UI
    when a user adds the integration.
    """

    VERSION = 1  # Schema version for the config entry

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step when user initiates the configuration.
        
        This is the first step in the config flow, where we ask for
        the IP address and port of the Modbus device.
        
        Args:
            user_input: Dictionary containing user input, or None on first call
            
        Returns:
            FlowResult: Either shows the form or creates the entry
        """
        # Dictionary to store any errors that occur
        errors: dict[str, str] = {}

        # If user has submitted the form
        if user_input is not None:
            try:
                # Validate the input
                info = await validate_input(self.hass, user_input)
                
                # Create a unique ID based on the host
                # This prevents duplicate entries for the same device
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                
                # Create the config entry with the validated data
                return self.async_create_entry(title=info["title"], data=user_input)
                
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during validation: %s", err)
                errors["base"] = "cannot_connect"

        # Define the data schema for the configuration form
        # This creates the input fields in the UI
        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,  # IP address (required)
                vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,  # Port with default value
            }
        )

        # Show the configuration form to the user
        return self.async_show_form(
            step_id="user",  # Identifier for this step
            data_schema=data_schema,  # The form schema
            errors=errors,  # Any errors to display
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect to the device."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth (if authentication is added later)."""
