from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .sync_modbus import read_register_sync, write_register_sync  # your sync functions


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    target_registers = getattr(coordinator, "registers", [])

    buttons = [
        ModbusToggleButton(hass, coordinator, entry.entry_id, reg)
        for reg in target_registers
    ]

    async_add_entities(buttons)
    

class ModbusToggleButton(CoordinatorEntity, ButtonEntity):
    """Button that flips a Modbus register between 0 and 1."""

    def __init__(self, hass: HomeAssistant, coordinator, entry_id: str, register: int):
        super().__init__(coordinator)
        self.hass = hass
        self._register = register
        self._attr_name = f"Toggle Register {register}"
        self._attr_unique_id = f"{entry_id}_toggle_{register}"

    async def async_press(self) -> None:
        """Handle button press: read → flip → write."""
        # 1) Read current value (sync → executor)
        current = await self.hass.async_add_executor_job(
            read_register_sync, self._register
        )

        new_value = 0 if current == 1 else 1

        # 2) Write new value (sync → executor)
        await self.hass.async_add_executor_job(
            write_register_sync, self._register, new_value
        )

        # 3) Refresh coordinator so sensors update
        await self.coordinator.async_request_refresh()