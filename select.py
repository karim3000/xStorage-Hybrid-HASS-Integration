from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .sync_modbus import write_register_sync


# Example dropdown options:
# You can change these to whatever you want.
OPTIONS = {
    "Low": 10,
    "Medium": 50,
    "High": 100,
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    # Choose the register you want the dropdown to write to
    DROPDOWN_REGISTER = 3044

    entity = ModbusSelectEntity(
        hass,
        coordinator,
        entry.entry_id,
        DROPDOWN_REGISTER,
        OPTIONS,
    )

    async_add_entities([entity])


class ModbusSelectEntity(CoordinatorEntity, SelectEntity):
    """Dropdown menu that writes mapped values to a Modbus register."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator,
        entry_id: str,
        register: int,
        options: dict[str, int],
    ):
        super().__init__(coordinator)
        self.hass = hass
        self._register = register
        self._options_map = options

        self._attr_options = list(options.keys())
        self._attr_name = f"Mode Select {register}"
        self._attr_unique_id = f"{entry_id}_select_{register}"

    @property
    def current_option(self) -> str | None:
        """Return the dropdown option that matches the current register value."""
        data = self.coordinator.data or {}
        current_value = data.get(self._register)

        # Reverse lookup: find which label matches the current register value
        for label, value in self._options_map.items():
            if value == current_value:
                return label

        return None

    async def async_select_option(self, option: str) -> None:
        """Write the selected option's mapped value to the Modbus register."""
        if option not in self._options_map:
            return

        value = self._options_map[option]

        # Write synchronously in executor
        await self.hass.async_add_executor_job(
            write_register_sync, self._register, value
        )

        # Refresh coordinator so sensors update
        await self.coordinator.async_request_refresh()