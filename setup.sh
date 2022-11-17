# System Required Packages

# xterm
# mdk4
# hashcat
# aircrack-ng
# python
# apache
# hostapd


pacman -S xterm aircrack-ng hostapd apache --no-confirm &>/dev/null

mkdir /opt/wci \
			/opt/wci/main  \
			/opt/wci/cache  \
			/opt/wci/main/captures  \ 
			/srv/http/wciPage 2>/dev/null
sleep 0.5


rm /etc/httpd/conf/httpd.conf
rm /etc/httpd/conf/extra/httpd-vhosts.conf

sleep 0.5
cp ./WCI/source/confFiles/httpd.conf /etc/httpd/conf/
cp ./WCI/source/confFiles/httpd-vhosts.conf /etc/httpd/conf/extra
cp -r ./WCI/source/confFiles/templates /opt/wci/main/
cp -r ./WCI/source /opt/wci/main
sleep 0.5

rename '/opt/wci/main/source' files source
