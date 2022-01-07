#!/bin/bash

# dependencies
# install python3
sudo dnf install -y python3 git 
# PIP needs to be updated
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python3 get-pip.py
# Install ansible 
python3 -m pip install --user ansible
