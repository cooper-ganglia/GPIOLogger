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
