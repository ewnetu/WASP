#!/bin/sh

# Install some packages
sudo apt-get -y update
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip

# install python Flask web framework
sudo pip install Flask

# prepare install directory for application 
mkdir /var/www
cd /var/www

#echo "Cloning repo of the WASPY microservice"
git clone https://github.com/muyiibidun/WASP.git


#run you code HERE!
cd WASP/waspy
python start.py


