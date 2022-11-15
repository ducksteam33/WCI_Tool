# System Required Packages

# xterm
# mdk4
# hashcat
# aircrack-ng
# python
# apache
# hostapd


pacman -S hcxtools xterm mdk4 aircrack-ng hashcat hostapd apache --no-confirm &>/dev/null

mkdir /opt/wci \
			/opt/wci/cache \
			/opt/wci/main \
			/opt/wci/main/captures \
			/opt/wci/main/templates 2>/dev/null
sleep 0.4
