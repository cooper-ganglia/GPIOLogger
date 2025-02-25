# Ross Carbonite Switcher LiveEDL Logging with Raspberry Pi

This guide provides a step-by-step process to set up a Raspberry Pi to log LiveEDL data from a Ross Carbonite switcher using GPIO and transfer the logs via FTP.

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

### 2. **Python Script to Monitor GPIO**
Save the following as `gpio_logger.py`.
```python
import RPi.GPIO as GPIO
import os
import time

LOG_FILE = "/home/pi/edl_log.txt"
START_COMMAND = "lftp -e 'open switcher_ip; user liveedl password; get edl_file; bye'"

GPIO.setmode(GPIO.BCM)
START_STOP_PIN = 17  # Corresponds to GPIO17 (Pin 11 on Raspberry Pi)
GPIO.setup(START_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed(channel):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    os.system(START_COMMAND)
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] LiveEDL Triggered\n")

GPIO.add_event_detect(START_STOP_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

### 3. **FTP Upload Script**
Save as `upload_edl.sh`.
```bash
#!/bin/bash
HOST='ftp_server_address'
USER='ftp_username'
PASS='ftp_password'
LOCAL_DIR='/home/pi/edl_files'
REMOTE_DIR='/path/on/ftp/server'

lftp -f "
open $HOST
user $USER $PASS
lcd $LOCAL_DIR
mirror --reverse --verbose . $REMOTE_DIR
bye
"
```
Make it executable:
```bash
chmod +x upload_edl.sh
```

### 4. **Automate with Cron Jobs**
Edit crontab:
```bash
crontab -e
```
Add these lines:
```bash
@reboot /usr/bin/python3 /home/pi/gpio_logger.py &
0 * * * * /home/pi/upload_edl.sh
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

