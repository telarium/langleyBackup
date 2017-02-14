#!/bin/bash

sudo apt-get update

sudo apt-get -y install build-essential libglib2.0-dev \
	libssl-dev libcurl4-openssl-dev libgirepository1.0-dev \
	exfat-fuse exfat-utils ntfs-3g \
	autoconf libgtk2.0-dev libssl-dev \
	libcurl4-openssl-dev asciidoc git

cd ~
wget https://github.com/libfuse/libfuse/releases/download/fuse-3.0.0pre0/fuse-3.0.0pre0.tar.gz
tar -zxvf fuse-3.0.0pre0.tar.gz
cd ~/fuse-3.0.0pre0.tar.gz
./configure
make
sudo make install

cd ~
git clone https://github.com/megous/megatools.git
cd ~/megatools
automake --add-missing
autoreconf
./configure
make
sudo make install
