from threading import Thread
import socket
import json
from time import sleep
from config.config import DIRECTION

total = {
    "north":[],
    "south":[],
    "east":[],
    "west":[],
}

# Variable globale pour partager l'état des mises à jour
new_updates = False
previous_lights_etat = {
        "north":False,
        "south":False,
        "east":False,
        "west":False,
}

def getQueuesUpdates(queues, events):
    global total, new_updates, previous_lights_etat
    while True:
        has_messages = False
        for dir, q in queues.items():
            if not q.empty():
                has_messages = True
                total[dir].append(q.get())
        for dir,etat in previous_lights_etat.items():
            if events[dir].is_set() != etat:
                has_messages = True
                previous_lights_etat[dir] = events[dir].is_set()
        
        if has_messages:
            print(total)
            new_updates = True


def socketCommunication():
    global total, new_updates
    
    # Tentative de connexion au serveur
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 5000))  # Connexion au serveur distant
            print("Connecté au serveur")
            break
        except ConnectionRefusedError:
            print("Serveur non disponible, nouvelle tentative dans 5 secondes...")
            sleep(5)
    
    # Envoi des mises à jour
    while True:
        try:
            if new_updates:
                json_data = json.dumps({"traffic":total, "lights":previous_lights_etat}) + "\n"
                sock.sendall(json_data.encode('utf-8'))
                new_updates = False
            sleep(0.1)  # Petit délai pour ne pas surcharger le CPU
            
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
    threads.append(Thread(target=getQueuesUpdates, args=(queues,events)))
    threads.append(Thread(target=socketCommunication))

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()