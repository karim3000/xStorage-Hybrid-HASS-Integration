from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pymodbus.client import AsyncModbusTcpClient  # pymodbus 3.x

_LOGGER = logging.getLogger(__name__)

class ModbusCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass, host: str, port: int, unit_id: int, registers: list[int], interval_seconds: int = 25):
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

    async def _async_update_data(self) -> dict:
        """Open connection, read requested registers, close connection."""
        data: dict[int, int] = {}

        client = AsyncModbusTcpClient(self._host, port=self._port, timeout=2)

        try:
            # 1) Connect and VERIFY
            connected = await client.connect()
            # Some versions return a bool; others set .connected or .protocol/transport.
            if not connected and not getattr(client, "connected", False):
                raise UpdateFailed("Unable to open Modbus TCP connection")


            
            # 2) Read registers (use input vs holding as per your map)
            for reg in self._registers:
                # If these are INPUT registers (3xxxx), use read_input_registers;
                # for HOLDING registers (4xxxx), use read_holding_registers.
                rr = await client.read_input_registers(address=reg, count=1, device_id=1)
                if rr.isError():
                    raise UpdateFailed(f"Error reading register {reg}: {rr}")
                data[reg] = rr.registers[0]

            return data

        except Exception as err:
            # Coordinator will log and handle retry/backoff for you
            raise UpdateFailed(f"Modbus update failed: {err}") from err
        
        finally:
            client.close()


    @property
    def registers(self) -> list[int]:
        return self._registers
