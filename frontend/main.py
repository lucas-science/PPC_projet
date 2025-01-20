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
        self.running = True
        self.queue = queue
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(1)
        print(f"Serveur démarré sur {self.host}:{self.port}")

        client_socket, address = server.accept()
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
        server.close()

    def format_data(self, traffic_data, traffic_lights):
        return {
            "vehicles": traffic_data,
            "lights": traffic_lights
        }

def run_server(queue):
    server = TrafficServer(queue=queue)
    server.start()

def run_interface(queue):
    # Importer le code de l'interface ici pour éviter les conflits d'importation
    from interface import main as run_interface_main  # Remplacer 'your_interface_file' par le nom de votre fichier
    
    def update_data():
        # Vérifier s'il y a de nouvelles données dans la queue
        if not queue.empty():
            return queue.get()
        return None

    # Lancer l'interface avec la fonction de mise à jour
    run_interface_main(update_data)

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