#/bin/bash -e

sudo apt-get install build-essential python-dev python-pip python-imaging python-smbus
sudo pip install RPi.GPIO

git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
cd ..

sudo cp tatertimer.service /etc/systemd/system/tatertimer.service
sudo systemctl daemon-reload
sudo systemctl start tatertimer
sudo systemctl enable tatertimer
