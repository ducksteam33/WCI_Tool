import os
import shutil
import subprocess as sp
import banners as bn
import evil_twin as et
import deauthattack as dt



class tool:
    def __init__(self,interface):
        self.chipset = interface
        self.selectedModule = ""
        self.commandOutput = ""

        self.currentMacAdress = ""
        self.permanentMacAdress = ""
        
        self.ismonitorMode = "No"
        self.monitorModeColor = "31"
        self.macCardColor = "31"
        self.wlanMode = ""

        while True:
            try:
                # Detect if the Networking Card is in Monitor mode
                temp = sp.run(["iwconfig",self.chipset],stdout=sp.PIPE)
                temp = temp.stdout.decode().split("\n")
                if("Managed" in temp[1]):
                    self.ismonitorMode = "No"
                    self.monitorModeColor = "31"
                if("Monitor" in temp[1]):
                    self.ismonitorMode = "Yes"
                    self.monitorModeColor = "32"

                #Detect the Macadress from the current Networking Card
                temp = sp.run(["macchanger","-s", f"{self.chipset}"],stdout=sp.PIPE)
                self.currentMacAdress = str(temp.stdout.decode().split("\n"))
                self.permanentMacAdress = self.currentMacAdress.split()[6]
                self.currentMacAdress = self.currentMacAdress.split()[2]


                #Comandline interface
                os.system("clear")
                banner = bn.Banner1()
                print(f"""

                                    {banner}

                                \33[37m 
                    Using Wifi Cracking Interface: V0.1.0
            by ducksteam33 | https://github.com/ducksteam33/WCI_Tool/


                    \33[37m Current Wifi Card: {self.chipset}
                    \33[37m Current MAC: \33[{self.macCardColor}m {self.currentMacAdress}
                    \33[37m Permanent MAC: {self.permanentMacAdress}
                    \33[37m Is in monitor mode: \33[{self.monitorModeColor}m  {self.ismonitorMode}
                    \33[37m

             Type numbers in to select the different options:

    [01]: change card Mac Adress                 [07]: start Evil Twin Attack
    [02]: change card to Monitor Mode            [08]: start Deauth Attack
    [03]: change card to Managed Mode            
    [04]: kill Networking Proceses
    [05]: restart Networking
    [06]: start Airodump-ng


              


            \n""")
                #Command Output
                print(self.commandOutput)

                #Command Input
                self.commandOutput = ""
                command = input(f"{self.selectedModule}/>>")


                #Command Options

                match command:
                    #Change Macadress
                    case "1":
                        self.commandOutput = self.ChangeMac(self.chipset)
                        self.macCardColor = "32"
                    #Change to Monitor Mode
                    case "2":
                        self.commandOutput = self.ChangeMonitorModeOn(self.chipset)
                        self.ismonitorMode = "Yes"
                        self.monitorModeColor = "32"
                        self.wlanMode = "mon"
                    #Change to Managed Mode
                    case "3":
                        self.commandOutput = self.ChangeMonitorModeOff(self.chipset)
                        self.ismonitorMode = "No"
                        self.monitorModeColor = "31"
                        self.wlanMode = ""
                    #Kill all possible Conflicting Networking processes with other commands
                    case "4":
                        self.commandOutput = self.killConflictingProcesses()
                    #Restart Networking Processes
                    case "5":
                        self.commandOutput = self.restartNetworking()
                    #Start Airodum-NG
                    case "6":
                        if self.ismonitorMode == "No":
                            self.ChangeMonitorModeOn(self.chipset)
                            self.ismonitorMode = "Yes"
                            self.monitorModeColor = "32"
                            self.wlanMode = "mon"
                            os.system(f"airodump-ng {self.chipset}")
                        else:
                            os.system(f"airodump-ng {self.chipset}")
                    #Start EvilTwin
                    case "7":
                        if self.ismonitorMode == "No":
                                self.ChangeMonitorModeOn(self.chipset)
                                self.ismonitorMode = "Yes"
                                self.monitorModeColor = "32"
                                self.wlanMode = "mon"
                                et.StartEvilTwin()
                        else:
                                et.StartEvilTwin()
                        self.ChangeMonitorModeOff(self.chipset)
                    #Start DeauthAttack
                    case "8":
                        if self.ismonitorMode == "No":
                                self.ChangeMonitorModeOn(self.chipset)
                                self.ismonitorMode = "Yes"
                                self.monitorModeColor = "32"
                                self.wlanMode = "mon"
                                dt.StartDeauthAttack()
                        else:
                            dt.StartDeauthAttack()
                        self.ChangeMonitorModeOff(self.chipset)
                    # Clear Output
                    case "clear":
                            os.system("clear")
                    # Quit Tool
                    case "exit":
                        quit()
                    # Non Existing Command
                    case other:
                        self.commandOutput = "Please enter a valid Command"
            except KeyboardInterrupt:
                os.system("clear")
                if self.ismonitorMode == "Yes":
                    self.ChangeMonitorModeOff(self.chipset)
                    self.removeFullFolder("/opt/wci/main/captures/handshake/")
                    os.system(f"mkdir /opt/wci/main/captures/handshake/ ")
                quit()


    #Function - Change Macadress
    def ChangeMac(self,interface):
        sp.run(["ifconfig",f"{interface}","down"])
        s = sp.run(["macchanger","-r", f"{interface}"], shell=False, stdout=sp.PIPE, stderr=sp.STDOUT)
        sp.run(["ifconfig",f"{interface}","up"])
        macOutput = s.stdout.decode().split("\n")
        output = str(macOutput[0])+"\n"+str(macOutput[1])+"\n"+str(macOutput[2])+"\n"
        return output

    #Function - Turn Monitor Mode On
    def ChangeMonitorModeOn(self,interface):
        if self.ismonitorMode == "No":
            sp.run(["ifconfig",f"{interface}","down"])
            os.system('iwconfig ' + interface + ' mode monitor')
            os.system(f"ip link set {interface} name {interface}mon")
            sp.run(["ifconfig",f"{interface}mon","up"])
            self.chipset = interface+"mon"

            output = "Card changed to Monitor mode sucessfully "
            return output
        else:
            output = "Card is allready in Monitor mode"
            return output

    #Function - Turn Monitor Mode Off
    def ChangeMonitorModeOff(self,interface):
        if self.ismonitorMode == "Yes":
            sp.run(["ifconfig",f"{interface}","down"])
            os.system('iwconfig ' + interface + ' mode managed')
            size = len(interface)
            self.chipset = interface[:size-3]
            os.system(f"ip link set {self.chipset}mon name {self.chipset}")
            sp.run(["ifconfig",f"{self.chipset}","up"])
            output = "Card changed to Managed mode sucessfully "
            return output
        else:
            output = "Card is allready in Managed mode" 
            return output
    #Function - Restart Networking Processes
    def restartNetworking(self):
        os.system("systemctl restart NetworkManager")
        os.system("systemctl start wpa_supplicant")
        os.system("systemctl start dhcpd")
        output = "Restarted wpa_supplicant and NetworkManager."
        return output

    #Function - Kill Networking Processes
    def killConflictingProcesses(self):
        s = sp.run(["airmon-ng","check","kill"],stderr=sp.STDOUT)
        os.system("killall hostapd dnsmasq dhcpd")
        output = "Killed posible conflicting Processes"
        return output
        
    #Function - Remove Folder
    def removeFullFolder(self,targetFolder):
        shutil.rmtree(targetFolder,ignore_errors=True,onerror=None)                    