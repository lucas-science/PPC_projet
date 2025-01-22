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
    "north": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":10,
    },
    "south": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":7,
    },
    "east": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":5,
    },
    "west": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":16,
    },
}
VEHICLES = ["car", "truk", "scooter"]

VEHICLES_PARAMS = {
    "car":[],
    "truk":[],
    "scooter":[],
    "police":[],
}

GREEN_DURATION = 10