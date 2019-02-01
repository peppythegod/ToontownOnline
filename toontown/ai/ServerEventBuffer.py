
class ServerEventBuffer:

    def __init__(self, air, name, avId, period=None):
        self.air = air
        self.name = name
        self.avId = avId
        if period is None:
            period = 6 * 60.0

        self.period = period
        self.lastFlushTime = None

    def destroy(self):
        self.flush()

    def flush(self):
        self.lastFlushTime = None

    def writeEvent(self, msg):
        self.air.writeServerEvent(self.name, self.avId, msg)

    def considerFlush(self):
        if self.lastFlushTime is None:
            self.lastFlushTime = globalClock.getFrameTime()
        elif globalClock.getFrameTime() - self.lastFlushTime > self.period * 60.0:
            self.flush()


class ServerEventAccumulator(ServerEventBuffer):

    def __init__(self, air, name, avId, period=None):
        ServerEventBuffer.__init__(self, air, name, avId, period)
        self.count = 0

    def flush(self):
        ServerEventBuffer.flush(self)
        if not self.count:
            return None

        self.writeEvent('%s' % self.count)
        self.count = 0

    def addEvent(self):
        self.count += 1
        self.considerFlush()


class ServerEventMultiAccumulator(ServerEventBuffer):

    def __init__(self, air, name, avId, period=None):
        ServerEventBuffer.__init__(self, air, name, avId, period)
        self.events = {}

    def flush(self):
        ServerEventBuffer.flush(self)
        if not len(self.events):
            return None

        msg = ''
        eventNames = sorted(self.events.keys())
        for eventName in eventNames:
            msg += '%s:%s' % (eventName, self.events[eventName])
            if eventName != eventNames[-1]:
                msg += ','
                continue

        self.writeEvent(msg)
        self.events = {}

    def addEvent(self, eventName):
        self.events.setdefault(eventName, 0)
        self.events[eventName] += 1
        self.considerFlush()
