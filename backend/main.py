import multiprocessing as mp

from config.config import DIRECTION
from config.process import PROCESS_FCT


def createQueues() -> dict:
    queues = dict()
    for name in DIRECTION:
        queues[name] = mp.Queue()
    return queues    

def initProcess(queues):
    process = []
    for fct in PROCESS_FCT:
        p = mp.Process(target=fct, args=[queues])
        process.append(p)
        p.start()
    
    for p in process:
        p.join()


if __name__ == "__main__":
    queues = createQueues()
    initProcess(queues)
    