#!/bin/bash

sudo apt-get update

sudo apt-get -y install build-essential libglib2.0-dev \
	libssl-dev libcurl4-openssl-dev libgirepository1.0-dev \
	exfat-fuse exfat-utils ntfs-3g \
	autoconf libgtk2.0-dev libssl-dev \
	libcurl4-openssl-dev asciidoc git \
	samba samba-common-bin

printf "[Backup Drive 1]\ncomment = Backup Drive 1\npath = /mnt/usb1/\nbrowseable = yes\nread only = no\nguest ok = yes\ncreate mask = 0660\ndirectory mask = 2770\n" | sudo tee /etc/samba/smb.conf -a
sudo smbpasswd -a root

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

echo -n "Enter your Mega Upload account e-mail: "
read email
echo -n "Enter your Mega Upload account password: "
read pwd

printf "$email\n$pwd" | sudo tee .megaLogin -a


