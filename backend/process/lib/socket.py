import json, socket
from time import sleep

class SocketCommunication:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.sock = None

    def connect_to_server(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                print("Connecté au serveur")
                break
            except ConnectionRefusedError:
                print("Serveur non disponible, nouvelle tentative dans 5 secondes...")
                sleep(5)

    def send_traffic_to_server(self, total_traffic):
        if self.sock is not None:  # Vérifie si la socket est toujours ouverte
            try:
                print("[DEBUG] Sending traffic to the server...")
                json_data = json.dumps({
                    "traffic": total_traffic,
                    "lights": None
                }) + "\n"
                self.sock.sendall(json_data.encode('utf-8'))
            except socket.error as e:
                print(f"Erreur de connexion : {e}")
        else:
            print("La socket est fermée, impossible d'envoyer les données.")
            # Optionnellement, tu peux essayer de te reconnecter ici si nécessaire.
            # self.connect_to_server()  # Si tu veux que la socket tente une reconnexion

    def send_lights_to_server(self, lights):
        if self.sock is not None:  # Vérifie si la socket est toujours ouverte
            try:
                print("[DEBUG] Sending lights to the server...")
                json_data = json.dumps({
                    "lights": lights,
                    "traffic": None
                }) + "\n"
                self.sock.sendall(json_data.encode('utf-8'))
            except socket.error as e:
                print(f"Erreur de connexion : {e}")
        else:
            print("La socket est fermée, impossible d'envoyer les données.")
            # Optionnellement, tu peux essayer de te reconnecter ici si nécessaire.
            # self.connect_to_server()  # Si tu veux que la socket tente une reconnexion

    def close_connection(self):
        """Ferme la connexion socket proprement."""
        if self.sock:
            try:
                print("Fermeture de la connexion...")
                self.sock.shutdown(socket.SHUT_RDWR)  # Fermeture de la connexion de manière ordonnée
                self.sock.close()  # Fermeture finale de la socket
                print("Connexion fermée avec succès.")
            except socket.error as e:
                print(f"Erreur lors de la fermeture de la connexion : {e}")
            finally:
                self.sock = None  # S'assurer que la référence à la socket est supprimée

    def run(self):
        self.connect_to_server()