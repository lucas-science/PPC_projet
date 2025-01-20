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
    for (dir,options) in TRAFIC_GENERATION_PARAMS.items():
        if dir == direction:
            if options["randomUniform"]:
                beginRange,endRange = options["randomUniformRange"]
                return uniform(beginRange, endRange)
            
            elif options["defined"]:
                return int(options["timeBetweenCar"])

def trafic(queue, direction):
    while True:
        timeToWait = timeGeneration(direction)
        sleep(timeToWait)
        randomVehcile = VEHICLES[randint(0,2)]
        newVehicle = getNewVehicle(randomVehcile, direction)
        queue.put(newVehicle)
        #print(f"Vehicule créée ! c'est un {newVehicle["type"]}")

def high_priority_traffic(queues,events): 
    while True:
        sleep(randint(5,15))
        random_index = randint(0,3)
        random_direction = DIRECTION[random_index]
        newVehicle = getNewVehicle("highPriority")
        queues[random_direction].put(newVehicle)
        

def TraficGeneration(queues,events):
    threads = []
    for (dir,q) in queues.items():
        thread = Thread(target=trafic, args=[q,dir])
        threads.append(thread)
        thread.start()

    #threads.append(Thread(target=high_priority_traffic, args=[queues, events]))
    
    for thread in threads:
        thread.join()
