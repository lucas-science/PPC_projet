import socket
import json
import multiprocessing as mp
import pygame
import sys
from datetime import datetime

# Code du serveur socket
class TrafficServer:
    def __init__(self, host='localhost', port=5000, queue=None):
        self.host = host
        self.port = port
        self.queue = queue
        self.running = True

    def start(self, client_socket, address):
        print(f"Connexion établie avec {address}")

        while self.running:
            try:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break

                traffic_data = json.loads(data)

                # Préparer les données pour l'interface
                formatted_data = self.format_data(traffic_data["traffic"], traffic_data["lights"])

                # Envoyer les données à l'interface via la queue
                self.queue.put(formatted_data)

                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{timestamp}] Données reçues et transmises à l'interface")

            except json.JSONDecodeError as e:
                print(f"Erreur JSON: {e}")
            except socket.error as e:
                print(f"Erreur socket: {e}")
                break

        client_socket.close()

    def format_data(self, traffic_data, traffic_lights):
        return {
            "vehicles": traffic_data,
            "lights": traffic_lights
        }

def run_server(queue):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5000))
    server.listen()
    print(f"Serveur démarré sur localhost:5000")

    while True:
        client_socket, address = server.accept()

        # Pour chaque connexion, créer un nouveau processus pour gérer la communication
        client_process = mp.Process(target=TrafficServer(queue=queue).start, args=(client_socket, address))
        client_process.start()

def run_interface(queue):
    # Importer le code de l'interface ici pour éviter les conflits d'importation
    from interface import main as run_interface_main  # Remplacer 'your_interface_file' par le nom de votre fichier
    
    def update_data_from_queue():
        if not data_queue.empty():
            return data_queue.get()  # Récupérer les nouvelles données de la queue
        return None  # Si aucune nouvelle donnée


    # Lancer l'interface avec la fonction de mise à jour
    run_interface_main(update_data_from_queue)

if __name__ == "__main__":
    # Créer une queue pour la communication entre les processus
    data_queue = mp.Queue()

    # Créer et démarrer les processus
    server_process = mp.Process(target=run_server, args=(data_queue,))
    interface_process = mp.Process(target=run_interface, args=(data_queue,))

    server_process.start()
    interface_process.start()

    # Attendre la fin des processus
    try:
        server_process.join()
        interface_process.join()
    except KeyboardInterrupt:
        print("\nArrêt des processus...")
        server_process.terminate()
        interface_process.terminate()
        server_process.join()
        interface_process.join()
