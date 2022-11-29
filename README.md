Requirements:
<br>	# xterm
<br>	# aircrack-ng
<br>	# python
<br>	# apache
<br>	# hostapd
<br>	# python

<br>To setup the tool use sudo ./setup.sh, it will also install or update the required packages.
<br>(!Attention! !This will override your apache httpd.conf and httpd-vhosts.conf files! In case you dont have a apache Server running then you dont have nothing to worry about.)

Then cd into /source and type: <br>

sudo ./wci -i wlan1 [or write instead your network card]
<br>To use the tool.


This tool was developed in Arch linux, im currently working on making it available for debian based distros.
