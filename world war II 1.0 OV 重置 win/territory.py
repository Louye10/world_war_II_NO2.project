# 定义领土类
class Territory:
    def __init__(self, name, resources, strategic_value):
        self.name = name
        self.resources = resources
        self.strategic_value = strategic_value
        self.controlling_country = None
        self.armies = []
    def add_army(self, army):
        army.location = self
        self.armies.append(army)
    def remove_army(self, army):
        if army in self.armies:
            self.armies.remove(army)
            army.location = None