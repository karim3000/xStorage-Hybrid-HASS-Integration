# xStorage-Hybrid-HASS-Integration
🚗🔋 xStorage Hybrid – Home Assistant Integration
A custom Home Assistant integration for monitoring and interacting with Nissan xStorage Hybrid energy systems.
This project brings real‑time visibility of your xStorage Hybrid battery, inverter, and energy flow directly into Home Assistant.

🌟 Features
- 📊 Live sensor data from your xStorage Hybrid system
- 🔌 Energy flow monitoring (grid, battery, solar, load)
- 🔋 Battery state tracking (SoC, voltage, temperature, charge/discharge status)
- ⚡ Inverter performance metrics
- 🏠 Home Assistant Energy Dashboard support
- 🔧 Local polling with no cloud dependency
- 🧩 Fully compatible with HACS as a custom repository

📦 Installation
Option 1 — HACS (Recommended)
- In Home Assistant, open HACS → Integrations
- Click the ⋮ menu → Custom repositories
- Add this repository:
https://github.com/karim3000/xStorage-Hybrid-HASS-Integration
- Select category: Integration
- Install the integration
- Restart Home Assistant
- Go to Settings → Devices & Services → Add Integration
- Search for xStorage Hybrid

Option 2 — Manual Installation
- Download the latest release
- Copy the folder:
custom_components/xstorage_hybrid
- into your Home Assistant configuration directory:
/config/custom_components/
- Restart Home Assistant
- Add the integration from Settings → Devices & Services


⚙️ Configuration
After installing, the integration will guide you through setup:
- Enter your xStorage Hybrid system’s IP address and Modbus TCP port 
- Sensors will automatically appear in the Home Assistant Dashboard

📜 License
This project is licensed under the MIT License.
