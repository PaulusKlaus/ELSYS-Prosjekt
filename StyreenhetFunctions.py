import datetime






roomMarkBG_Color = "#fbfafa"
roomMarkOccupied_Color = "#63CBFF"

def sort_Hastegrad_ID_Time(requests_list):
    requests_list.sort(key=lambda x: (x["Hastegrad"]-4, x["Tid"]))
    for i, request in enumerate(requests_list):
        request["ID"] = i + 1

def print_requests(requests_list):
    for request in requests_list:
        print("Request ID:", request["ID"])
        print("Room:", request["Rom"])
        print("Bed:", request["Seng"])
        print("Request Type:", request["Hva"])
        print("Priority:", request["Hastegrad"])
        print("Occupied:", request["Occupied"])
        print("Time:", request["Tid"])
        print("")

def color(hastegrad):
    if hastegrad== 5:
        return "#22C22D"
    elif hastegrad == 4:
        return "#F3F041"
    elif hastegrad == 3:
        return "#FF800A"
    elif hastegrad == 2:
        return "#FF0000"
    elif hastegrad == 99:
        return "#fbfafa"
    elif hastegrad == 1:
        return "#800000"
    else:
        return "#002E5D"
def roomPosition(rom):
    if rom == 301:
        return (15,20)
    elif rom == 303:
        return (180,20)
    elif rom == 305:
        return (275,20)
    elif rom == 307:
        return (440,20)
    elif rom == 309:
        return (797,20)
    elif rom == 311:
        return (960,20)
    elif rom == 313:
        return (1057,20)
    elif rom == 315:
        return (1220,20)
    elif rom == 302:
        return (150,400)
    elif rom == 304:
        return (305,400)
    elif rom == 306:
        return (930,400)
    elif rom == 308:
        return (1085,400)
    else:
        print("Rom ikke funnet")
        return (0,0)

def occupiedColor(room):
    if room.get('Occupied'):
        return roomMarkOccupied_Color
    else:
        return roomMarkBG_Color
    
def timeDifference(startTime, endTime):
    time_diff = datetime.datetime.strptime(endTime, "%H:%M:%S") - datetime.datetime.strptime(startTime, "%H:%M:%S")
    time_diff_str = str(time_diff)
    return time_diff_str

def is_room_occupied(requests_list, room_number):
    for request in requests_list:
        if request["Rom"] == room_number and request.get("Occupied"):
            return True
    return False

def logStringText(user, request,logEvent,time):
    if logEvent == "Delete":
        return f"{time} - {user} slettet forespørsel manuelt av type {request['Hva']} for rom {request['Rom']} seng {request['Seng']} med hastegrad {request['Hastegrad']} etter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Increase Importance":
        return f"{time} - {user} økte hastegraden for forespørsel av type {request['Hva']} for rom {request['Rom']} seng {request['Seng']} til hastegrad {request['Hastegrad']}, eter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Decrease Importance":
        return f"{time} - {user} senket hastegraden for forespørsel av type {request['Hva']} for rom {request['Rom']} seng {request['Seng']} til hastegrad {request['Hastegrad']}, eter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Occupied":
        return f"{time} - {user} markerte rom {request['Rom']} seng {request['Seng']} med hastegrad {request['Hastegrad']} som sykepleier tilstede, etter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Unoccupied":
        return f"{time} - {user} markerte rom {request['Rom']} seng {request['Seng']} med hastegrad {request['Hastegrad']} som sykepleier ikke tilstede, etter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Added":
        return f"{time} - {user} la til forespørsel av type {request['Hva']} for rom {request['Rom']} seng {request['Seng']} med hastegrad {request['Hastegrad']}"
    elif logEvent == "Room Delete":
        return f"{time} - Rom {request['Rom']}, Seng {request['Seng']} angret forespørsel av type {request['Hva']} med hastegrad {request['Hastegrad']} etter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Remote Delete":
        return f"{time} - {user} slettet forespørsel med kort av type {request['Hva']} for rom {request['Rom']} seng {request['Seng']} med hastegrad {request['Hastegrad']} etter tid: {timeDifference(request['Tid'],time)}(T:M:S)"
    elif logEvent == "Faste Added":
        return f"{time} - {user} la til faste for rom {request['Rom']}"
    elif logEvent == "Faste Removed":
        return f"{time} - {user} fjernet faste for rom {request['Rom']}"
    else:
        return f"Error: logEvent:{logEvent} does not exist"
    
def logStringData(user, request,logEvent,time):
    if logEvent == "Room Delete":
        return f"{time},Rom {request['Rom']} Seng {request['Seng']},{request['Hva']},{request['Rom']},{request['Seng']},{timeDifference(request['Tid'],time)},{logEvent},{request['Hastegrad']}"
    elif logEvent == "Faste Added" or logEvent == "Faste Removed":
        return f"{time},{user},,{request['Rom']},,,{logEvent},"
    else:
        return f"{time},{user},{request['Hva']},{request['Rom']},{request['Seng']},{timeDifference(request['Tid'],time)},{logEvent},{request['Hastegrad']}"

def getCurrentTime():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time

def fileWrite(fileName, data):
    with open(fileName, 'a') as file:
        file.write(data + "\n")

