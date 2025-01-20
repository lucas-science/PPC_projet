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
        try:
            print("[DEBUG] Sending traffic to the server...")
            json_data = json.dumps({
                "traffic": total_traffic,
                "lights": None
            }) + "\n"
            self.sock.sendall(json_data.encode('utf-8'))
        except socket.error as e:
            print(f"Erreur de connexion : {e}")

    def send_lights_to_server(self, lights):
        try:
            print("[DEBUG] Sending lights to the server...")
            json_data = json.dumps({
                "lights": lights,
                "traffic":None
            }) + "\n"
            self.sock.sendall(json_data.encode('utf-8'))
        except socket.error as e:
            print(f"Erreur de connexion : {e}")

    def run(self):
        self.connect_to_server()

