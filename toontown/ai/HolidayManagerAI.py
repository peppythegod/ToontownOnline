
class HolidayManagerAI:
    currentHolidays = []
    
    def __init__(self, air):
        self.air = air
        
    def isHolidayRunning(self, holidayId):
        return holidayId in self.currentHolidays
        
    def isMoreXpHolidayRunning(self):
        return False