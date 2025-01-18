from threading import Thread
from time import sleep
from random import uniform

from config.config import DIRECTION, TRAFIC_GENERATION_PARAMS, VEHICLES_PARAMS


def getNewVehicle(type):
    if type in VEHICLES_PARAMS:
        return {type, VEHICLES_PARAMS[type]}
    else:
        return -1

def timeEngine(direction):
    for (dir,options) in TRAFIC_GENERATION_PARAMS.items():
        if dir == direction:
            if options["randomUniform"]:
                beginRange,endRange = options["randomUniformRange"]
                return uniform(beginRange, endRange)
            
            elif direction["defined"]:
                return options["timeBetweenCar"]

def trafic(queue, direction):
    while True:
        timeToWait = timeEngine(direction)
        sleep(timeToWait)
        newVehicle = getNewVehicle()
        queue.put(newVehicle)

def high_priority_traffic(queues):
    pass


def TraficsGeneration(queues):
    threads = []
    for (i,q) in enumerate(queues):
        thread = Thread(target=trafic, args=[q, DIRECTION[i]])
        threads.append(thread)
        thread.start()

    threads.append(Thread(target=high_priority_traffic, args=[queues]))
    
    for thrad in threads:
        thread.join()

        