from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, REGISTER_LIST
from .coordinator import ModbusCoordinator

PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data["host"]
    port = entry.data.get("port", 502)
    unit_id = entry.data.get("unit_id", 1)

    # Registers you want to poll (keep this list here or load from options)
    registers = list(REGISTER_LIST.keys())

    coordinator = ModbusCoordinator(
        hass=hass,
        host=host,
        port=port,
        unit_id=unit_id,
        registers=registers,
        interval_seconds=30,  # was 15
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok