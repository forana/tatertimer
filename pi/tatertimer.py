import time
import math
import os
import sys
import threading
import subprocess

import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import requests

led_threshold = 7200 # seconds before LED lights up

last_time = time.time() # global tracking the last time tater went out
time_since_string = ""

wifi_connected = False

endpoint = "http://tater.alexforan.com/reset"
password = os.getenv("TATER_PASSWORD", "tater")

def log(message):
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.flush()

log("tater timer starting")

RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0

# Load font.
# font = ImageFont.load_default()
small_font = ImageFont.truetype(font = "font.ttf", size = 16)
large_font = ImageFont.truetype(font = "font.ttf", size = 48)

log("display initialized")

GPIO.setmode(GPIO.BCM)
# active-low button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# led w/ resistor
GPIO.setup(24, GPIO.OUT)

log("GPIO initialized")

def button_check():
    global last_time
    last_read = GPIO.LOW
    while True:
        # read the button with some craptastic debouncing
        current_read = GPIO.input(23)
        if current_read != last_read and current_read == GPIO.LOW:
            # then the button was pressed, and we reset the timer
            last_time = time.time()
            log("internal time reset")
            try:
                resp = requests.post(endpoint, data = {"password": password})
                if resp.status_code == 200:
                    log("reset sent to server successfully")
                else:
                    log("server error: " + resp.text)
            except e:
                log("something went real wrong: %s" % (e,))
        last_read = current_read
        time.sleep(0.01)

def time_control():
    global time_since_string
    while True:
        # do time math like an idiot
        time_since = time.time() - last_time
        h = math.floor(time_since/3600)
        m = math.floor(time_since/60)
        s = time_since%60
        time_since_string = "%02d:%02d:%02d" % (h, m, s)

        # if the time's past the threshold, light it up
        GPIO.output(24, GPIO.HIGH if led_threshold <= time_since else GPIO.LOW)
        
        time.sleep(1)

def wifi_check():
    global wifi_connected
    # check wifi state real hackily
    try:
        subprocess.check_output("iwconfig 2>&1 | grep ESSID", shell = True)
        wifi_connected = True
    except subprocess.CalledProcessError as e:
        wifi_connected = False

def screen_control():
    while True:
        # new blank frame
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        if time.time() - last_time >= led_threshold:
            draw.text((x, top + 0), "take the boy outside!", font=small_font, fill=255)

        draw.text((x, top + 16), time_since_string, font=large_font, fill=255)
        draw.text((x, top + 52), "wifi: " + ("yes :)" if wifi_connected else "no :( :( :("), font=small_font, fill=255)

        disp.image(image)
        disp.display()

        time.sleep(0.3)

threading.Thread(target = button_check).start()
threading.Thread(target = time_control).start()
threading.Thread(target = wifi_check).start()
threading.Thread(target = screen_control).start()

log("tater timer running")

# internals take care of these automatically, apparently?
#     disp.clear()
#     GPIO.cleanup()
