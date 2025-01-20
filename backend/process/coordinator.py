from threading import Thread, Event, Lock
import socket
import json
from time import sleep
from process.lib.socket import SocketCommunication

from config.config import DIRECTION, CIRCLE_DIRECTION

# Verrou pour protéger l'accès aux données partagées
traffic_lock = Lock()

# État global du trafic
total_traffic = {
    "north": [],
    "south": [],
    "east": [],
    "west": [],
}

# Events pour les tournants à gauche
gauche_event = {
    "north": Event(),
    "south": Event(),
    "east": Event(),
    "west": Event(),
}

# État des feux
previous_lights_etat = {
    "north": False,
    "south": False,
    "east": False,
    "west": False,
}

data_updated = Event()
data_sent = Event()

TIME_TO_LIVE = 2


def manageTrafficForDirection(direction, events, sock):
    index_dir = CIRCLE_DIRECTION.index(direction)
    while True:
        if events[direction].is_set():
            if not total_traffic[direction]:
                sleep(0.1)
                continue

            # print(f"Thread {direction}: Attente de l'envoi des données.",total_traffic[direction] )
            # print(f"Thread {direction}: Vérification des conditions pour modification de la circulation.")
            firstCar = total_traffic[direction][0]["destination"]
            en_face = CIRCLE_DIRECTION[(index_dir+2) % 4]
            a_droite = CIRCLE_DIRECTION[(index_dir+3) % 4]
            nbr_voiture_en_face = len(total_traffic[en_face])

            if firstCar == a_droite:
                voiture = total_traffic[direction].pop(0)
                print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                sleep(TIME_TO_LIVE)
                sock.send_traffic_to_server(total_traffic.copy())
            elif firstCar == en_face:
                voiture = total_traffic[direction].pop(0)
                print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                sleep(TIME_TO_LIVE)
                sock.send_traffic_to_server(total_traffic.copy())
            else:
                gauche_event[direction].set()
                if not nbr_voiture_en_face:
                    voiture = total_traffic[direction].pop(0)
                    gauche_event[direction].clear()
                    print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                    sleep(TIME_TO_LIVE)
                    sock.send_traffic_to_server(total_traffic.copy())
                if gauche_event[en_face].is_set():
                    if nbr_voiture_en_face < len(total_traffic[direction]):
                        voiture = total_traffic[direction].pop(0)
                        gauche_event[direction].clear()
                        print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                        sleep(TIME_TO_LIVE)
                        sock.send_traffic_to_server(total_traffic.copy())


def getQueuesUpdates(queues, events, sock):
    change = False
    while True:
        for dir, q in queues.items():
            if not q.empty():
                    total_traffic[dir].append(q.get())
                    change = True

        if change:
            sock.send_traffic_to_server(total_traffic)
        change = False
        sleep(0.1)

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