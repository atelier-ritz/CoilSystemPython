#!/bin/bash
apt-get update
apt-get -y upgrade
apt-get install -y python3-pip
pip3 install opencv-python
pip3 install opencv-contrib-python
pip3 install numpy
pip3 install matplotlib
pip3 install pyqt5
apt-get install qttools5-dev-tools
apt-get install coriander

printf '\e[48;5;88m ACTION REQUIRED BELOW \n'
read -n 1 -p "Press enter to install s826 driver..." mainmenuinput
printf '\e[48;5;0m'
cd $(pwd)/s826
make modules
make install
modprobe s826
dmesg
printf '\e[48;5;88m ACTION REQUIRED BELOW \n'
read -n 1 -p "->check above for verification, then press Enter..." mainmenuinput
printf '\e[48;5;0m'
cd -

printf '\e[48;5;88m ACTION REQUIRED BELOW \n'
read -n 1 -p "Press enter to install pydc1394 (firewire camera)..." mainmenuinput
printf '\e[48;5;0m'
cd $(pwd)/pydc1394-master
python3 setup.py install
cd -
