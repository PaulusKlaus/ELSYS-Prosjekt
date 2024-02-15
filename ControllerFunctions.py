roomMarkBG_Color = "#fbfafa"
roomMarkOccupied_Color = "#A2E8A8"

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
        print("Time:", request["Tid"])
        print("")

def color(hastegrad):
    if hastegrad== 4:
        return "#006D07"
    elif hastegrad == 3:
        return "#F3F041"
    elif hastegrad == 2:
        return "#FF800A"
    elif hastegrad == 1:
        return "#FF0000"
    elif hastegrad == 99:
        return "#fbfafa"
    else:
        return "#002E5D"
def roomPosition(rom):
    if rom == 301:
        return (20,20)
    elif rom == 303:
        return (150,20)
    elif rom == 305:
        return (240,20)
    elif rom == 307:
        return (370,20)
    elif rom == 309:
        return (680,20)
    elif rom == 311:
        return (810,20)
    elif rom == 313:
        return (900,20)
    elif rom == 315:
        return (1020,20)
    elif rom == 302:
        return (130,350)
    elif rom == 304:
        return (260,350)
    elif rom == 306:
        return (790,350)
    elif rom == 308:
        return (920,350)
    else:
        print("Rom ikke funnet")
        return (0,0)

def occupiedColor(room):
    if room.get('Occupied'):
        return roomMarkOccupied_Color
    else:
        return roomMarkBG_Color
