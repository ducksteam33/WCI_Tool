#!/bin/bash

mkdir /opt/wci \
	  /opt/wci/main  \
	  /opt/wci/cache  \
	  /opt/wci/main/captures \ 
	  /srv/http/wciPage 2>/dev/null


rm /etc/httpd/conf/httpd.conf
rm /etc/httpd/conf/extra/httpd-vhosts.conf
cp ./source/confFiles/httpd.conf /etc/httpd/conf/
cp ./source/confFiles/httpd-vhosts.conf /etc/httpd/conf/extra
cp -r ./source  /opt/wci/main
cp -r ./source/confFiles/templates  /opt/wci/main/source


pacman -S xterm aircrack-ng hostapd apache --noconfirm #&>/dev/null



echo Done! Now you just can type 'wci -h' to get started!


