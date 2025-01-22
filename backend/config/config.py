DIRECTION = [
    "north",
    "south",
    "east",
    "west"
]
CIRCLE_DIRECTION = [
    "north", "east", "south", "west"
]

TRAFIC_GENERATION_PARAMS = {
    "direction": {
        "north": {
            "randomUniform":0,
            "randomUniformRange":[4,8],
            "defined":1,
            "timeBetweenCar":15,
        },
        "south": {
            "randomUniform":0,
            "randomUniformRange":[4,8],
            "defined":1,
            "timeBetweenCar":12,
        },
        "east": {
            "randomUniform":0,
            "randomUniformRange":[4,8],
            "defined":1,
            "timeBetweenCar":18,
        },
        "west": {
            "randomUniform":0,
            "randomUniformRange":[4,8],
            "defined":1,
            "timeBetweenCar":19,
        },
    },
    "highPriorityVehicles": {
            "randomUniformVehicle":0,
            "randomUniformRange":[20,30],
            "defined":1,
            "timeBetweenCar":30,
    }
}
VEHICLES = ["car", "truk", "scooter", "police"]

VEHICLES_PARAMS = {
    "car":[],
    "truk":[],
    "scooter":[],
    "police":[],
}

GREEN_DURATION = 20

TIME_TO_LEAVE = 3