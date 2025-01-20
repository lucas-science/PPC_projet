from time import sleep, time
from config.config import GREEN_DURATION

def lights(queues,events):
    last_switch_time = time()
    sens = "north_south"
    while True:
        while not events["presenceHighPriorityVehicle"].is_set():
            current_time = time()
            elapsed_time = current_time - last_switch_time
            
            if events["presenceHighPriorityVehicle"].is_set():
                break
                
            if elapsed_time >= GREEN_DURATION and not events["presenceHighPriorityVehicle"].is_set():
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
                    
                last_switch_time = current_time
            
            sleep(0.1) # éviter de surcharger le CPU
        