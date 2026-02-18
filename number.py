from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .sync_modbus import write_register_sync


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    SLIDER_REGISTER = 3078

    sliders = [
        ModbusSliderNumber(hass, coordinator, entry.entry_id, SLIDER_REGISTER)
    ]

    async_add_entities(sliders)


class ModbusSliderNumber(CoordinatorEntity, NumberEntity):
    """A slider that writes 0–100 to a Modbus register."""

    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = "slider"

    def __init__(self, hass: HomeAssistant, coordinator, entry_id: str, register: int):
        super().__init__(coordinator)
        self.hass = hass
        self._register = register
        self._attr_name = f"Brightness {register}"
        self._attr_unique_id = f"{entry_id}_slider_{register}"

    @property
    def native_value(self):
        """Return the current value from the coordinator."""
        data = self.coordinator.data or {}
        return data.get(self._register, 0)

    async def async_set_native_value(self, value: float) -> None:
        """Write the new slider value to the Modbus register."""
        await self.hass.async_add_executor_job(
            write_register_sync, self._register, int(value)
        )

        # Refresh sensors after writing
        await self.coordinator.async_request_refresh()