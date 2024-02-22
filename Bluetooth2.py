import ControllerFunctions as cf
server = cf.createServer("38:d5:7a:7d:5d:2e", 4)
print(cf.getMessage(server))