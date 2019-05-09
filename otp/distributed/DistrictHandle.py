
class DistrictHandle:
    def __init__(self, channel, population, name):
        self.channel = channel
        self.doId = self.channel
        self.population = population
        self.avatarCount = self.population
        self.name = name
        self.available = True