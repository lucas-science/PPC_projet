from threading import Thread
from time import sleep
from random import uniform, randint

from config.config import TRAFIC_GENERATION_PARAMS, VEHICLES_PARAMS, DIRECTION, VEHICLES


def getNewVehicle(type, direction):
    if type in VEHICLES_PARAMS:
        dest = direction
        while dest == direction:
            dest_index = randint(0,3)
            dest = DIRECTION[dest_index]
        
        return {
            "type": type,
            "destination":dest,
            "params": VEHICLES_PARAMS[type],
        }
    
    else:
        return -1

def timeGeneration(direction):
    for (dir,options) in TRAFIC_GENERATION_PARAMS["direction"].items():
        if dir == direction:
            if options["randomUniform"]:
                beginRange,endRange = options["randomUniformRange"]
                return uniform(beginRange, endRange)
            
            elif options["defined"]:
                return int(options["timeBetweenCar"])

def trafic(queue, direction):
    try:
        while True:
            timeToWait = timeGeneration(direction)
            sleep(timeToWait)
            randomVehcile = VEHICLES[randint(0,2)]
            newVehicle = getNewVehicle(randomVehcile, direction)
            queue.put(newVehicle)
            #print(f"Vehicule créée ! c'est un {newVehicle["type"]}")
    except KeyboardInterrupt:
        pass

def timeGenerationHighPriorityVehicle():
    if TRAFIC_GENERATION_PARAMS["highPriorityVehicles"]["defined"]:
        return TRAFIC_GENERATION_PARAMS["highPriorityVehicles"]["timeBetweenCar"]
    #else: -> si on utilise une génération aléatoire 
    
def high_priority_traffic(queues,events): 
    try:
        while True:
            if not events["presenceHighPriorityVehicle"].is_set():
                time_to_sleep = timeGenerationHighPriorityVehicle()
                sleep(time_to_sleep)
                random_index = randint(0,3)
                random_direction = DIRECTION[random_index]
                newVehicle = getNewVehicle("police", random_direction)
                print("POLICEEEEE")
                queues["traffic"][random_direction].put(newVehicle)
                events["presenceHighPriorityVehicle"].set()
                queues["locationHighPrirorityVehicle"].put(random_direction)
    except KeyboardInterrupt:
        pass
         

def TraficGeneration(queues,events):
    threads = []
    for (dir,q) in queues["traffic"].items():
        thread = Thread(target=trafic, args=[q,dir])
        threads.append(thread)
    threads.append(Thread(target=high_priority_traffic, args=[queues, events]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

