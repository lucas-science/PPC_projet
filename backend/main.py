import multiprocessing as mp

from config.config import DIRECTION
from config.process import PROCESS_FCT


def createQueues() -> dict:
    return {
        "north":mp.Queue(),
        "south":mp.Queue(),
        "east":mp.Queue(),
        "west":mp.Queue(),
    }

def createEvents()-> dict:
    return {
        "north":mp.Event(),
        "south":mp.Event(),
        "east":mp.Event(),
        "west":mp.Event(),
        "presenceHighPriorityVehicle":mp.Event(),
    }


def initProcess(queues, events):
    process = []
    for fct in PROCESS_FCT:
        p = mp.Process(target=fct, args=[queues, events])
        process.append(p)
        p.start()
    return process

def waitEndProcess(process):
    for p in process:
        p.join()

if __name__ == "__main__":
    queues = createQueues()
    events = createEvents()

    process = initProcess(queues, events)
    waitEndProcess(process)