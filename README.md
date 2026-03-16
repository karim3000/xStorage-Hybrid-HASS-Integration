# xStorage-Hybrid-HASS-Integration
🚗🔋 xStorage Hybrid – Home Assistant Integration
A custom Home Assistant integration for monitoring and interacting with Nissan xStorage Hybrid energy systems.
This project brings real‑time visibility of your xStorage Hybrid battery, inverter, and energy flow directly into Home Assistant, enabling smarter automation and deeper insight into your home energy usage.

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

🗂️ Repository Structure
This project follows the required HACS structure:
xStorage-Hybrid-HASS-Integration/
│
├── custom_components/
│   └── xstorage_hybrid/
│       ├── __init__.py
│       ├── manifest.json
│       ├── sensor.py
│       ├── config_flow.py
│       └── ...
│
├── hacs.json
├── LICENSE
└── README.md



⚙️ Configuration
After installing, the integration will guide you through setup:
- Enter your xStorage Hybrid system’s IP address
- Choose polling interval (optional)
- Sensors will automatically appear in Home Assistant

🧪 Development Status
This integration is actively evolving.
Planned enhancements include:
- 🔧 Write‑capable controls (if supported by the device)
- 📈 Additional diagnostic sensors
- 🛠 Improved error handling and discovery
Contributions, bug reports, and feature requests are welcome.

🤝 Contributing
If you’d like to help:
- Open an issue
- Submit a pull request
- Share logs or device behavior to improve compatibility

📜 License
This project is licensed under the MIT License.

If you want, I can also generate:
- A logo for the integration
- A more technical deep‑dive section
- A troubleshooting section
- A HACS badge set for the top of the README
Just tell me the style you prefer.
