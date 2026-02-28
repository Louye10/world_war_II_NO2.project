# 定义军队类
class Army:
    def __init__(self, size, country):
        self.size = size
        self.country = country
        self.location = None
        self.experience = 0
    def train(self):
        self.experience += 1
    def merge(self, other_army):
        if self.country == other_army.country:
            self.size += other_army.size
            self.experience = (self.experience + other_army.experience) / 2