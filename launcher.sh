#!/bin/bash
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

echo "Es ist:"
date
cd /
source /home/pi/dsabot/dsa/bin/activate
echo "activated alias"
cd /home/pi/dsabot/
echo "changed to python dir"
python --version # example way to see that your virtual env loaded as expected
nohup python3 main.py
echo "run program"
cd /
echo "change back to root"
