# Ross Carbonite Switcher LiveEDL Logging with Raspberry Pi

## Project Description
This project integrates a Raspberry Pi with a Ross Carbonite switcher to automate LiveEDL logging using GPIO triggers and FTP file transfers. It allows for seamless recording of switcher activity with a simple button press and automatic log uploads.

## Requirements
### Hardware
- Raspberry Pi (any model with GPIO support)
- Ross Carbonite switcher with GPI/O DB37 connector
- Bi-directional logic level converter (5V to 3.3V)
- DB37 male connector breakout or pigtail wires
- Jumper wires
- Momentary push button (for external control)
- USB storage device (optional for log backup)

### Software
- Raspbian OS (or any Linux-based OS for Raspberry Pi)
- Python 3
- `RPi.GPIO` Python library
- `lftp` (for FTP file transfer)
- `cron` (for automation)

## Wiring Setup

### **GPIO Pinout Connection**

| Carbonite GPI/O (DB37) | Function               | Raspberry Pi (40-pin GPIO) |
|------------------------|------------------------|----------------------------|
| Pin 1 (GPI/O 1)       | Start/Stop LiveEDL     | GPIO17 (Pin 11)            |
| Pin 25                | Ground                 | Ground (Pin 6)             |
| Pin 26 (5V)           | Power for Converter    | 5V (Pin 2)                 |
| Pin 31                | Ground                 | Ground (Pin 9)             |
| Pin X (Other Inputs)  | Additional GPI Inputs  | GPIOXX (as needed)         |

- Connect the **Carbonite GPIO outputs** to the **logic level converter's high-voltage (HV) side**.
- Connect the **low-voltage (LV) side** of the converter to the Raspberry Pi's GPIO inputs.
- The **momentary button** is wired to GPI/O 1 (DB37 Pin 1) and Ground (DB37 Pin 25) to start/stop LiveEDL.

## Software Setup

### 1. **Install Required Packages**
```bash
sudo apt update
sudo apt install python3-pip lftp
pip3 install RPi.GPIO
```

### 2. **Required Files**

- `gpio_logger.py`: A Python script to monitor the GPIO button press and trigger LiveEDL recording.
- `upload_edl.sh`: A Bash script to upload recorded EDL files to an FTP server.
- `crontab` entry to automate the execution of the scripts.

Ensure the scripts are stored in `/home/pi/` and are executable:
```bash
chmod +x /home/pi/gpio_logger.py /home/pi/upload_edl.sh
```

### 3. **Automate with Cron Jobs**
Edit crontab:
```bash
crontab -e
```
Add these lines:
```bash
@reboot /usr/bin/python3 /home/pi/gpio_logger.py &
0 * * * * /home/pi/upload_edl.sh
```

## File Structure
```
📂 Ross-Carbonite-Logger
├── 📜 README.md
├── 📜 gpio_logger.py
├── 📜 upload_edl.sh
└── 📂 logs
    └── edl_log.txt
```

## Usage
- Press the physical button to start/stop LiveEDL recording.
- EDL logs are saved and automatically uploaded to FTP every hour.
- Logs can be retrieved manually from `/home/pi/edl_log.txt`.

## Troubleshooting
- Check GPIO wiring if the button does not trigger events.
- Use `sudo journalctl -u cron` to debug cron jobs.
- Manually test FTP with `lftp -u ftp_username,ftp_password ftp_server_address`.

This setup ensures seamless LiveEDL logging and automation for the Ross Carbonite switcher.

