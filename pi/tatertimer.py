import time
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT)
toggle = True
print("press the button to toggle the light")
last_read = GPIO.LOW

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load font.
# font = ImageFont.load_default()
font = ImageFont.truetype(font = "font.ttf", size = 16)

try:
    while True:
        current_read = GPIO.input(23)
        if current_read != last_read and current_read == GPIO.LOW:
            toggle = not toggle
        last_read = current_read
        GPIO.output(24, GPIO.HIGH if toggle else GPIO.LOW)

        draw.rectangle((0,0,width,height), outline=0, fill=0)
    
        draw.text((x, top), "tater timer :)", font=font, fill=255)
    
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True)
        draw.text((x, top + 16), "IP: " + str(IP),  font=font, fill=255)
    
        draw.text((x, top + 32), "time: " + time.strftime("%I:%M:%S %p"), font=font, fill=255)
        
        draw.text((x, top + 48), "button: " + ("up" if current_read else "down"), font=font, fill=255)

        disp.image(image)
        disp.display()
        time.sleep(.01)
finally:
    disp.clear()
    GPIO.cleanup()

