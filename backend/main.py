import multiprocessing as mp
from time import sleep
import json
import socket
import signal
import os


from config.config import DIRECTION
from config.process import PROCESS_FCT

process = list()

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

def signalHandler(frame, sign):
    for p in process:
        p.terminate()
    print("Tous les processus et threads sont terminés. Programme arrêté.")
    for p in process:
        p.join()  



if __name__ == "__main__":
    queues = createQueues()
    events = createEvents()

    process = initProcess(queues, events)

    signal.signal(signal.SIGINT, signalHandler)

    waitEndProcess(process)
