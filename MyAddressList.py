__addressList={}

def addAdress2List(address,Topic):
    global __addressList
    __addressList[Topic]=address
    return __addressList

def remove(Topic):
    return __addressList.pop(Topic)

def get(Topic):
   return __addressList.get(Topic)

def getAllAddress():
    return __addressList.values()

def getAll(Topic):
    return __addressList