from config.config import DIRECTION

def Coordinator(queues):
    total = {
        "north":[],
        "south":[],
        "east":[],
        "west":[],
    }
    while True:
        has_messages = False
        for dir, q in queues.items():
            if not q.empty():
                has_messages = True
                total[dir].append(q.get())
        if has_messages:
            print(total)