#!/bin/bash

# dependencies
# install python3
sudo dnf install -y python3 git 
# install dev tools
sudo dnf groupinstall "Development Tools" -y
sudo dnf install openssl-devel libffi-devel bzip2-devel -y
sudo dnf install wget -y
wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
tar zxvf Python-3.9.9.tgz
cd Python-3.9*/
./configure --enable-optimizations
sudo make altinstall
# PIP needs to be updated
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python3.9 get-pip.py
# Install ansible 
#python3.9 -m pip install --user ansible
# Install python3.9 as alternative
sudo alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1000001 --slave /usr/bin/pip3 pip3 /usr/local/bin/pip3.9 --slave /usr/bin/pydoc3 pydoc3 /usr/local/bin/pydoc3.9
# also update pip globally
sudo python3 get-pip.py
# install ansible globally
sudo pip3 install ansible
cd ~/
rm -rf Python-3.9.9.tgz Python-3.9.9/
