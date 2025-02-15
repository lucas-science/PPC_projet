from time import sleep, time
from config.config import GREEN_DURATION, DIRECTION
from process.lib.socket import SocketCommunication

sock = SocketCommunication()


def lights(queues, events):
    HighPrirorityVehicleDirection = None
    sock.run()
    last_switch_time = time()
    sens = "north_south"
    while True:
        while not events["presenceHighPriorityVehicle"].is_set():
            HighPrirorityVehicleDirection = None
            current_time = time()
            elapsed_time = current_time - last_switch_time

            if events["presenceHighPriorityVehicle"].is_set():
                break

            if elapsed_time >= GREEN_DURATION and not events["presenceHighPriorityVehicle"].is_set():
                print("[LIGHTS] On change de couleur")
                if sens == "north_south":
                    events["north"].clear()
                    events["south"].clear()
                    events["east"].set()
                    events["west"].set()
                    sens = "east_west"

                else:
                    events["east"].clear()
                    events["west"].clear()
                    events["north"].set()
                    events["south"].set()
                    sens = "north_south"

                sock.send_lights_to_server({
                    "north": events["north"].is_set(),
                    "south": events["south"].is_set(),
                    "east": events["east"].is_set(),
                    "west": events["west"].is_set()
                })

                last_switch_time = current_time
            sleep(0.1)
        # si y a un vehicule de high priroity alors on init les feu si ce n'est pas déja fait
        if HighPrirorityVehicleDirection == None:
            HighPrirorityVehicleDirection = queues["locationHighPrirorityVehicle"].get()
            print("emergency in : ", HighPrirorityVehicleDirection)
            for dir in DIRECTION:
                if dir != HighPrirorityVehicleDirection:
                    events[dir].clear()
            if not events[HighPrirorityVehicleDirection].is_set():
                events[HighPrirorityVehicleDirection].set()

            sock.send_lights_to_server({
                "north": events["north"].is_set(),
                "south": events["south"].is_set(),
                "east": events["east"].is_set(),
                "west": events["west"].is_set()
            })
        sleep(0.1)
