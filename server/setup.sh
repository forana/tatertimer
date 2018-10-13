#/bin/bash -e

sudo apt-get install build-essential python-dev python-pip
sudo pip install -r requirements.txt

sudo cp tatertimer.service /etc/systemd/system/tatertimer.service
sudo systemctl daemon-reload
sudo systemctl start tatertimer
sudo systemctl enable tatertimer
