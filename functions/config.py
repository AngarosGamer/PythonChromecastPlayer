import socket

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
            f = open("settings.config","r+")
            self.APP_NAME = f.readline().split("=")[1][:-1].strip()
            self.WINDOW_X = f.readline().split("=")[1].strip()
            self.WINDOW_Y = f.readline().split("=")[1].strip()
            self.COLOR = f.readline().split("=")[1][:-1].strip()
            self.ACCENT = f.readline().split("=")[1][:-1].strip()
            self.FILE_TYPE = f.readline().split("=")[1].strip()
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)
            self.LOCATION = "http://"+IPAddr+":8000/media/"
        except:
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