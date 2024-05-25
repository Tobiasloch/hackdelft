class Vehicle:
    name:str
    capacity:int
    speed:int
    type:str
    count:int

    def __init__(self, name:str, capacity:int, speed:int, type:str, count:int):
        self.name = name
        self.capacity = capacity
        self.speed = speed
        self.type = type
        self.count = count