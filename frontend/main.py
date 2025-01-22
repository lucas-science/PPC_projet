import socket
import json
import multiprocessing as mp
from datetime import datetime


class TrafficServer:
    def __init__(self, host='localhost', port=5001, queue=None):
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

                self.queue.put(traffic_data)

                timestamp = datetime.now().strftime("%H:%M:%S")
                print(
                    f"\n[{timestamp}] Données reçues et transmises à l'interface")

            except json.JSONDecodeError as e:
                print(f"Erreur JSON: {e}")
            except socket.error as e:
                print(f"Erreur socket: {e}")
                break

        client_socket.close()


def run_server(queue):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5001))
    server.listen()
    print(f"Serveur démarré sur localhost:5001")

    while True:
        client_socket, address = server.accept()

        client_process = mp.Process(target=TrafficServer(
            queue=queue).start, args=(client_socket, address))
        client_process.start()


def run_interface(queue):
    # Remplacer 'your_interface_file' par le nom de votre fichier
    from interface import main as run_interface_main

    def update_data_from_queue():
        if not data_queue.empty():
            return data_queue.get()
        return None

    run_interface_main(update_data_from_queue)


if __name__ == "__main__":
    data_queue = mp.Queue()

    server_process = mp.Process(target=run_server, args=(data_queue,))
    interface_process = mp.Process(target=run_interface, args=(data_queue,))

    server_process.start()
    interface_process.start()

    try:
        server_process.join()
        interface_process.join()
    except KeyboardInterrupt:
        print("\nArrêt des processus...")
        server_process.terminate()
        interface_process.terminate()
        server_process.join()
        interface_process.join()
