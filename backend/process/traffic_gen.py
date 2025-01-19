from threading import Thread
from time import sleep
from random import uniform, randint

from config.config import TRAFIC_GENERATION_PARAMS, VEHICLES_PARAMS, DIRECTION


def getNewVehicle(type):
    if type in VEHICLES_PARAMS:
        return {
            "type": type,
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
        newVehicle = getNewVehicle("car")
        queue.put(newVehicle)

def high_priority_traffic(queues):
    pass


def TraficGeneration(queues):
    threads = []
    for (dir,q) in queues.items():
        thread = Thread(target=trafic, args=[q,dir])
        threads.append(thread)
        thread.start()

    threads.append(Thread(target=high_priority_traffic, args=[queues]))
    
    for thrad in threads:
        thread.join()

        