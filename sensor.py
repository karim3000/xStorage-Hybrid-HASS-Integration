# custom_components/xStorage-Hybrid-HASS-Integration/sensor.py
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, REGISTER_LIST


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    # Prefer the coordinator's list if it exists; fall back to REGISTER_LIST keys
    target_registers = getattr(coordinator, "registers", list(REGISTER_LIST.keys()))

    entities: list[SensorEntity] = []
    for reg in target_registers:
        spec = REGISTER_LIST.get(reg) or {"name": f"Register {reg}", "unit": None}
        entities.append(ModbusRegisterSensor(coordinator, entry.entry_id, reg, spec))

    async_add_entities(entities, update_before_add=True)


class ModbusRegisterSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id: str, register: int, spec: dict):
        super().__init__(coordinator)
        self._register = register
        self._attr_name = spec["name"]
        self._attr_unique_id = f"{entry_id}_reg_{register}"
        self._attr_native_unit_of_measurement = spec.get("unit")

    @property
    def native_value(self):
        # coordinator.data is a dict {register: value}
        data = self.coordinator.data or {}
        return data.get(self._register)

    @property
    def available(self) -> bool:
        # Reflects whether last coordinator update succeeded
        return self.coordinator.last_update_success