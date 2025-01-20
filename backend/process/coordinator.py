from threading import Thread, Event, Lock
import socket
import json
from time import sleep
from queue import Queue
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

def manageTrafficForDirection(direction, events):
    index_dir = CIRCLE_DIRECTION.index(direction)
    while True:
        if events[direction].is_set() and data_sent.is_set():
            with traffic_lock:
                if not total_traffic[direction]:
                    sleep(0.1)
                    continue
                
                #print(f"Thread {direction}: Attente de l'envoi des données.",total_traffic[direction] )
                #print(f"Thread {direction}: Vérification des conditions pour modification de la circulation.")
                firstCar = total_traffic[direction][0]["destination"]
                en_face = CIRCLE_DIRECTION[(index_dir+2)%4]
                a_droite = CIRCLE_DIRECTION[(index_dir+3)%4]
                nbr_voiture_en_face = len(total_traffic[en_face])

                if firstCar == a_droite:
                    voiture = total_traffic[direction].pop(0)
                    print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                    sleep(TIME_TO_LIVE)
                    data_updated.set()
                elif firstCar == en_face:
                    voiture = total_traffic[direction].pop(0)
                    print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                    sleep(TIME_TO_LIVE)
                    data_updated.set()
                else:
                    gauche_event[direction].set()
                    if not nbr_voiture_en_face:
                        voiture = total_traffic[direction].pop(0)
                        gauche_event[direction].clear()
                        print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                        sleep(TIME_TO_LIVE)
                        data_updated.set()
                    if gauche_event[en_face].is_set():
                        if nbr_voiture_en_face < len(total_traffic[direction]):
                            voiture = total_traffic[direction].pop(0)
                            gauche_event[direction].clear()
                            print(f"{direction} : la {voiture["type"]} part vers {firstCar}")
                            sleep(TIME_TO_LIVE)
                            data_updated.set()

def getQueuesUpdates(queues, events):
    change = False
    while True:
        with traffic_lock:
            for dir, q in queues.items():
                if not q.empty():
                        total_traffic[dir].append(q.get())
                        change = True
            
                for dir, etat in previous_lights_etat.items():
                    if events[dir].is_set() != etat:
                        previous_lights_etat[dir] = events[dir].is_set()
                        change = True

        if change:
            data_updated.set()
            data_sent.clear()   
        change = False
        sleep(0.1)

def socketCommunication():
    # Connexion au serveur
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 5000))
            print("Connecté au serveur")
            break
        except ConnectionRefusedError:
            print("Serveur non disponible, nouvelle tentative dans 5 secondes...")
            sleep(5)

    while True:
        try:
            if data_updated.is_set():
                print("[DEBUG] Sending data to the server...")
                with traffic_lock:
                    json_data = json.dumps({
                        "traffic": total_traffic,
                        "lights": previous_lights_etat
                    }) + "\n"
                    sock.sendall(json_data.encode('utf-8'))
                    #print(f"[DEBUG] Data sent: {json_data}")
                    data_sent.set()
                    data_updated.clear()
            sleep(0.1)

        except socket.error as e:
            print(f"Erreur de connexion : {e}")
            sock.close()
            # Tentative de reconnexion
            while True:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(('localhost', 5000))
                    print("Reconnecté au serveur")
                    break
                except ConnectionRefusedError:
                    print("Serveur non disponible, nouvelle tentative dans 5 secondes...")
                    sleep(5)

def Coordinator(queues, events):
    threads = []
    
    threads.append(Thread(target=getQueuesUpdates, args=(queues, events)))
    threads.append(Thread(target=socketCommunication))
    
    for direction in CIRCLE_DIRECTION:
        threads.append(Thread(target=manageTrafficForDirection, args=(direction, events)))
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()