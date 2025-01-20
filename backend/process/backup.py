def manageCirculation(events):
    global total_traffic
    while True:
        nordLight, southLight = events["north"].is_set(), events["south"].is_set()
        eastLight, westLight = ["east"].is_set(), events["west"].is_set()
        if nordLight and southLight:
            try:
                firstCarNorth, firstCarSouth = total_traffic["north"][0], total_traffic["south"][0]
            except IndexError:
                firstCarNorth = None if not total_traffic["north"] else total_traffic["north"][0]
                firstCarSouth = None if not total_traffic["south"] else total_traffic["south"][0]

            if (firstCarNorth["destination"] == "south" or firstCarNorth["destination"] == "west" )\
                and (firstCarSouth["destination"] == "north" or firstCarSouth["destination"] == "east"):
                northDelete.set()
                southDelete.set()
            elif firstCarNorth["destination"] == "east":
                if firstCarSouth == None:
                    northDelete.set()
                else:
                    southDelete.set()
            else:
                if firstCarNorth == None:
                    southDelete.set()
                else:
                    northDelete.set()

        elif eastLight and westLight:
            try:
                firstCarEast, firstCarWest = total_traffic["east"][0], total_traffic["west"][0]
            except IndexError:
                firstCarEast = None if not total_traffic["east"] else total_traffic["east"][0]
                firstCarWest = None if not total_traffic["west"] else total_traffic["west"][0]
            
            if (firstCarEast["destination"] == "west" or firstCarEast["destination"] == "north") and \
               (firstCarWest["destination"] == "east" or firstCarWest["destination"] == "south"):
                eastDelete.set()
                westDelete.set()
            elif firstCarEast["destination"] == "south":
                if firstCarWest == None:
                    eastDelete.set()
                else:
                    westDelete.set()
            else:
                if firstCarEast == None:
                    westDelete.set()
                else:
                    eastDelete.set()
