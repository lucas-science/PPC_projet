from config.config import QUEUE_NAMES

def Coordinator(queues):
    total = {
        "northQueue":[],
        "southQueue":[],
        "eastQueue":[],
        "westQueue":[],
    }
    while True:
        for i, queue in enumerate(queues):
            new_car = queue.get()
            total[QUEUE_NAMES[i]].append(new_car)
            print(QUEUE_NAMES[i], ' : ', total[QUEUE_NAMES[i]])
            
        