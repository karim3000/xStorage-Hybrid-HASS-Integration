"""Constants for the Eaton xStorage Hybrid integration."""

# Domain name for the integration
DOMAIN = "xstorage_hybrid"

# Configuration keys
CONF_HOST = "host"
CONF_PORT = "port"

# Default values
DEFAULT_PORT = 502  # Standard Modbus TCP port
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Device information
MANUFACTURER = "Eaton"
MODEL = "xStorage Hybrid"

# Modbus register addresses (these should be adjusted based on actual device specification)
# Example registers - replace with actual xStorage Hybrid register addresses
REGISTER_STATE_OF_CHARGE = 1000  # Example register address for SoC
