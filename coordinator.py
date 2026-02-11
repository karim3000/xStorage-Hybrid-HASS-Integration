from __future__ import annotations
from datetime import timedelta
from typing import Dict, List
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pymodbus.client import AsyncModbusTcpClient  # the build you're using

_LOGGER = logging.getLogger(__name__)

class ModbusCoordinator(DataUpdateCoordinator[Dict[int, int]]):
    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        unit_id: int,
        registers: List[int],
        interval_seconds: int = 60,
        timeout: float = 2.0,
        read_input: bool = True,   # True: read_input_registers (3xxxx), False: read_holding_registers (4xxxx)
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="modbus_coordinator",
            update_interval=timedelta(seconds=interval_seconds),
        )
        self._host = host
        self._port = port
        self._unit_id = unit_id
        self._registers = registers
        self._timeout = timeout
        self._read_input = read_input

        # per-register cache of last-known-good values
        self._last_values: Dict[int, int] = {}

    async def _async_update_data(self) -> Dict[int, int]:
        """Connect per cycle, read registers, keep last values on transient failures."""
        result: Dict[int, int] = {}

        client = AsyncModbusTcpClient(self._host, port=self._port, timeout=self._timeout)

        try:
            connected = await client.connect()
            if not connected and not getattr(client, "connected", False):
                raise RuntimeError("Unable to open Modbus TCP connection")

            # Pick the function based on your map
            async_read = (
                client.read_input_registers
                if self._read_input
                else client.read_holding_registers
            )

            for reg in self._registers:
                # IMPORTANT: keep using device_id as you requested
                rr = await async_read(address=reg, count=1, device_id=self._unit_id)

                if rr.isError():
                    # If we already have a value, keep showing it; log the issue
                    if reg in self._last_values:
                        _LOGGER.warning("Read error on reg %s: %s; keeping last value", reg, rr)
                        result[reg] = self._last_values[reg]
                    else:
                        # first time for this register and it fails ⇒ no fallback available
                        raise RuntimeError(f"Error reading register {reg}: {rr}")
                else:
                    val = rr.registers[0]
                    result[reg] = val
                    self._last_values[reg] = val

            return result

        except Exception as err:
            # If we have a previous full dataset, return it to keep entities available
            if self.data:
                _LOGGER.warning("Modbus poll failed (%s); returning last dataset", err)
                return self.data
            # First-ever failure: no previous data to show ⇒ mark as failed
            raise UpdateFailed(f"Modbus update failed: {err}") from err

        finally:
            try:
                client.close()   # your build’s close() is sync; don’t await
            except Exception:
                pass

    @property
    def registers(self) -> List[int]:
        return self._registers