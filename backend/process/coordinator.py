from threading import Thread, Event, Lock
import socket
import json
from time import sleep
from process.lib.socket import SocketCommunication

from config.config import DIRECTION, CIRCLE_DIRECTION, TIME_TO_LEAVE 

# Locks for shared data
traffic_lock = Lock()
gauche_event_lock = Lock()  # New lock for gauche_event access

# Global traffic state
total_traffic = {
    "north": [],
    "south": [],
    "east": [],
    "west": [],
}

# Left turn events
gauche_event = {
    "north": Event(),
    "south": Event(),
    "east": Event(),
    "west": Event(),
}

# Light states
previous_lights_etat = {
    "north": False,
    "south": False,
    "east": False,
    "west": False,
}

data_updated = Event()
data_sent = Event()

def deleteCarFromTraffic(traffic, direction, sock, events):
    with traffic_lock:
        voiture = traffic[direction].pop(0)
    print(f"{direction} : la {voiture['type']} part vers {voiture['destination']}")
    sleep(TIME_TO_LEAVE)
    voiture["source"] = direction
    sock.send_traffic_to_server(traffic.copy(), voiture)
    if voiture["type"] == "police":
        events["presenceHighPriorityVehicle"].clear()

def manageTrafficForDirection(direction, events, sock):
    index_dir = CIRCLE_DIRECTION.index(direction)
    en_face = CIRCLE_DIRECTION[(index_dir+2) % 4]
    a_droite = CIRCLE_DIRECTION[(index_dir+3) % 4]
    
    try:
        while True:
            with traffic_lock:
                if not total_traffic[direction]:
                    continue
                
            if events[direction].is_set() and events[en_face].is_set():
                with traffic_lock:
                    firstCarDestination = total_traffic[direction][0]["destination"]
                    nbr_voiture_en_face = len(total_traffic[en_face])

                if firstCarDestination == a_droite:
                    deleteCarFromTraffic(total_traffic, direction, sock, events)
                elif firstCarDestination == en_face:
                    deleteCarFromTraffic(total_traffic, direction, sock, events)
                else:
                    with gauche_event_lock:
                        gauche_event[direction].set()
                        if not nbr_voiture_en_face:
                            deleteCarFromTraffic(total_traffic, direction, sock, events)
                        if gauche_event[en_face].is_set():
                            if nbr_voiture_en_face < len(total_traffic[direction]):
                                deleteCarFromTraffic(total_traffic, direction, sock, events)
            
            elif events[direction].is_set():
                print("circulation en mode police")
                deleteCarFromTraffic(total_traffic, direction, sock, events)
            
            sleep(0.1)

    except KeyboardInterrupt:
        pass

def getQueuesUpdates(queues, events, sock):
    change = False
    try:
        while True:
            for dir, q in queues["traffic"].items():
                if not q.empty():
                    with traffic_lock:
                        total_traffic[dir].append(q.get())
                        change = True

            if change:
                sock.send_traffic_to_server(total_traffic)
            change = False
            sleep(0.1)
    except KeyboardInterrupt:
        print("Get queue thread ended")

def Coordinator(queues, events):
    sock = SocketCommunication()
    sock.run()

    threads = []
    threads.append(Thread(target=getQueuesUpdates, args=(queues, events, sock)))
    
    for direction in CIRCLE_DIRECTION:
        threads.append(Thread(target=manageTrafficForDirection, args=(direction, events, sock)))
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    sock.close_connection()