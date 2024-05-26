class Vehicle:
    name:str
    capacity:int
    type:str
    count:int

    def __init__(self, name:str, capacity:int, type:str, count:int):
        self.name = name
        self.capacity = capacity
        self.type = type
        self.count = count