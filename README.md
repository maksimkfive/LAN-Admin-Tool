# LAN-Admin-Tool
A CMD-based network administration tool.

---

## ⚠️ Status: Under Development ⚠️

This project is currently in its early stages and is only a concept. Significant work is needed to finalize its features and capabilities.

---

## Dependencies

- **SQLite3:** Used for database handling.
- **Scapy:** Required for network scanning and ARP spoofing functionalities.
- **Python's os and threading modules:** Used for various functionalities like multi-threaded port scanning and system-level commands.
- **Nmap:** Used for getting some details with `lookup` command.
  
To install dependencies, run: `pip install scapy sqlite3 nmap-python`


---

## Features

- **Network Scanning:** Identify hosts in your network.
- **Host Lookup:** Examine details about a detected host.

---

## Known Issues

- **ARP Spoofing:** Currently, the ARP spoofing functionality does not operate as intended.

---

## Usage

To run the LAN Admin Tool: `python network_admin_tool.py`

Use the `help` command within the program to see available commands and their descriptions.

---

## Contributions

Feel free to fork the project and submit pull requests. Any contributions to improve the tool or fix the known issues are welcome. 😊

---

Thank you for your interest in the LAN Admin Tool. Your feedback and contributions will help shape its future development.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
