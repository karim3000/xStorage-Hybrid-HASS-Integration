# button.py
from __future__ import annotations

import asyncio
import logging
from typing import Iterable, Tuple

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .sync_modbus import write_register_sync  # <-- using your sync wrapper

_LOGGER = logging.getLogger(__name__)

ModbusWriteSteps = Iterable[Tuple[int, int]]

DELAY_BETWEEN_WRITES = 2  # seconds


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    buttons = [
        ModbusActionButton(
            hass=hass,
            coordinator=coordinator,
            entry_id=entry.entry_id,
            name="Force charge",
            unique_suffix="force_charge",
            steps=[(3044, 1), (3079, 100), (3086, 1)],
            delay=DELAY_BETWEEN_WRITES,
        ),
        ModbusActionButton(
            hass=hass,
            coordinator=coordinator,
            entry_id=entry.entry_id,
            name="Force discharge",
            unique_suffix="force_discharge",
            steps=[(3044, 1), (3078, 50), (3086, 2)],
            delay=DELAY_BETWEEN_WRITES,
        ),
        ModbusActionButton(
            hass=hass,
            coordinator=coordinator,
            entry_id=entry.entry_id,
            name="Reset mode",
            unique_suffix="reset_mode",
            steps=[(3044, 0), (3086, 0)],
            delay=DELAY_BETWEEN_WRITES,
        ),
    ]

    async_add_entities(buttons)


class ModbusActionButton(CoordinatorEntity, ButtonEntity):
    """Button that performs a sequenced set of Modbus register writes."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator,
        entry_id: str,
        name: str,
        unique_suffix: str,
        steps: ModbusWriteSteps,
        delay: float = 0.0,
    ) -> None:
        super().__init__(coordinator)
        self.hass = hass
        self._steps = list(steps)
        self._delay = float(delay)
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{unique_suffix}"

    async def async_press(self) -> None:
        """Execute the sequence of Modbus writes."""
        try:
            for i, (register, value) in enumerate(self._steps):

                # Perform sync write inside executor (correct for new pymodbus)
                await self.hass.async_add_executor_job(
                    write_register_sync, register, value
                )

                # Delay between steps (except last)
                if self._delay and i < len(self._steps) - 1:
                    await asyncio.sleep(self._delay)

            # Refresh coordinator after all writes
            await self.coordinator.async_request_refresh()

        except Exception as exc:
            _LOGGER.exception(
                "Modbus action '%s' failed: %s", self._attr_name, exc
            )
            raise
