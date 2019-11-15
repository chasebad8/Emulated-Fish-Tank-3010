def emulate(tankID, name, location, petType):
    host = 'localHost'
    textport = 1025
            
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(textport)
    server_address = (host, port)

    data = {"tank_id": int(tankID), "name" : name, "location" : location, "petType": petType, "packetType": "tank"}

    sendIt = json.dumps(data)
    s.sendto(str(sendIt).encode('utf-8'), server_address)

    s.close()