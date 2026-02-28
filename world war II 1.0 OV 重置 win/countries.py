# 定义国家类
class Country:
    def __init__(self, name, is_player=False):
        self.name = name
        self.is_player = is_player
        self.resources = 100
        self.manpower = 100
        self.armies = []
        self.controlled_territories = []
    def recruit_army(self, size):
        cost = size * 10
        if self.resources >= cost and self.manpower >= size:
            self.resources -= cost
            self.manpower -= size
            self.armies.append(Army(size, self.name))
            return True
        return False
    def produce_resources(self):
        self.resources += len(self.controlled_territories) * 5
        self.manpower += len(self.controlled_territories) * 6