DIRECTION = [
    "north",
    "south",
    "east",
    "west"
]

TRAFIC_GENERATION_PARAMS = {
    "north": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":5,
    },
    "south": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":3,
    },
    "east": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":2,
    },
    "west": {
        "randomUniform":0,
        "randomUniformRange":[4,8],
        "defined":1,
        "timeBetweenCar":8,
    },
}
VEHICLES = ["car", "truk", "scooter"]

VEHICLES_PARAMS = {
    "car":[],
    "truk":[],
    "scooter":[],
    "highPriority":[],
}