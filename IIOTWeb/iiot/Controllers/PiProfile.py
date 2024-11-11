import os,socket,platform,pywifi


def gethostname():
    hostname=socket.gethostname()
    return hostname
def getIPaddr():
    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(hostname)
    return IPAddr
    # platform.uname()[1]