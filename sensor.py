"""Sensor platform for Eaton xStorage Hybrid integration."""
import logging
import time
from typing import Any
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.framer import FramerType
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_HOST,
    CONF_PORT,
    DOMAIN,
    MANUFACTURER,
    MODEL,
    REGISTER_STATE_OF_CHARGE,
)

# Logger for this module
_LOGGER = logging.getLogger(__name__)



async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up xStorage Hybrid sensors from a config entry.
    
    This function is called by Home Assistant to set up the sensor platform.
    It creates sensor entities and adds them to Home Assistant.
    
    Args:
        hass: Home Assistant instance
        entry: The config entry for this integration
        async_add_entities: Callback to add entities to Home Assistant
    """
    # Get the configuration data stored in __init__.py
    config_data = hass.data[DOMAIN][entry.entry_id]
    host = config_data[CONF_HOST]
    port = config_data[CONF_PORT]
    
    _LOGGER.debug("Setting up xStorage Hybrid sensors for %s:%s", host, port)
    
    # Create the state of charge sensor
    # In a production version, you might create multiple sensors here
    sensors = [
        XStorageStateOfChargeSensor(host, port, entry.entry_id),
    ]
    
    # Add all sensors to Home Assistant
    async_add_entities(sensors, update_before_add=True)


class XStorageStateOfChargeSensor(SensorEntity):
    """Representation of the xStorage Hybrid State of Charge sensor.
    
    This sensor displays the battery's current state of charge as a percentage.
    """

    def __init__(self, host: str, port: int, entry_id: str) -> None:
        """Initialize the State of Charge sensor.
        
        Args:
            host: IP address of the Modbus device
            port: Port number for Modbus communication
            entry_id: Unique identifier for the config entry
        """
        # Store configuration
        self._host = host
        self._port = port
        self._entry_id = entry_id
        
        # Initialize sensor state
        self._attr_name = "State of Charge"
        self._attr_native_value = None
        self._attr_available = True
        
        # Set unique ID for this entity
        # This ensures the entity is uniquely identifiable
        self._attr_unique_id = f"{entry_id}_state_of_charge"
        
        # Configure sensor properties
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        
        # Set up device info to group all entities under one device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=f"{MODEL} ({host})",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="1.0.0",  # You could read this from the device if available
        )

        #Create modbus TCP connection
        try:
            self.client = ModbusTcpClient("192.168.40.70", port=8899, framer=FramerType.SOCKET)

            if not self.client.connect():
                print(f"Failed to connect to {CONF_HOST}:{CONF_PORT}")
                return

            print(f"Connected to {CONF_HOST}:{CONF_PORT}")

        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error updating State of Charge sensor: %s", err)
            self._attr_available = False

        _LOGGER.debug("Initialized State of Charge sensor for %s:%s", host, port)

        try:
            # 3) READ a register
            print(f"Reading register {REGISTER_STATE_OF_CHARGE}...")
            rr3 = self.client.read_input_registers(3066, count=1, device_id=1)
            if rr3.isError():
                print("Read failed:", rr3)
            else:
                print("Read value:", rr3.registers[0])
                read_data = rr3.registers[0]
                self._attr_native_value = read_data  # Static 85% state of charge
                self._attr_available = True

        except ModbusException as e:
            print("Modbus error:", e)

        finally:
            self.client.close()
            print("Connection closed.")


        _LOGGER.debug(
            "Updated State of Charge for %s:%s = %s%%",
            self._host,
            self._port,
            self._attr_native_value,
        )
        
