import socket
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

class config_setup :
    APP_NAME = ""
    WINDOW_X = ""
    WINDOW_Y = ""
    COLOR = ""
    ACCENT = ""
    HOVER = ""
    FILE_TYPE = ""
    LOCATION = ""

    def __init__(self):
        try:
            print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Trying to read configuration file settings")
            f = open("../settings.config","r+")
            self.APP_NAME = f.readline().split("=")[1][:-1].strip()
            self.WINDOW_X = f.readline().split("=")[1].strip()
            self.WINDOW_Y = f.readline().split("=")[1].strip()
            self.COLOR = f.readline().split("=")[1][:-1].strip()
            self.ACCENT = f.readline().split("=")[1].strip()
            self.FILE_TYPE = f.readline().split("=")[1].strip()
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)
            self.LOCATION = "http://"+IPAddr+":8000/media/"
        except:
            print(f"{Fore.YELLOW}Warning :{Style.RESET_ALL} Error in configuration file forced settings to revert to default")
            self.APP_NAME = "Default"
            self.WINDOW_X = "800"
            self.WINDOW_Y = "400"
            self.COLOR = "system"
            self.ACCENT = "#eda850"
            self.FILE_TYPE = ".wav"
            self.LOCATION = "http://192.168.3.1:8000/media/"
            
        # Error checking the color input
        if (self.COLOR != 'dark' or self.COLOR != 'light' or self.COLOR != 'system'):
            self.COLOR = "system"

        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Using app name : {self.APP_NAME}")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Using window X : {self.WINDOW_X}")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Using window Y : {self.WINDOW_Y}")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Using app color : {self.COLOR}")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Using app accent color : {self.ACCENT}")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Using media file type : {self.FILE_TYPE}")
        print(f"[{Fore.GREEN}OK{Style.RESET_ALL}]: Serving media from : {self.LOCATION}")
    
    def getAppName(self):
        return self.APP_NAME
    
    def getWIN_X(self):
        return self.WINDOW_X

    def getWIN_Y(self):
        return self.WINDOW_Y

    def getColor(self):
        return self.COLOR

    def getAccent(self):
        return self.ACCENT

    def getFileType(self):
        return self.FILE_TYPE
    
    def getLocation(self):
        return self.LOCATION