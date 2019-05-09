from pandac.PandaModules import loadPrcFileData

class GameSettings:
    # TODO: find real api values
    GL = 0
    DX7 = 0
    DX8 = 0

    windowed = 1
    music = 1
    sfx = 1
    toon_chat_sounds = 1
    music_vol = 100
    sfx_vol = 100
    res = 1 # PS: 0 to 4 -- see ToonBase for reference
    embedded = 0
    
    acceptingNewFriends = 1
    acceptingNonFriendWhispers = 1

    def __init__(self):
        self.settingsFile = "etc/settings.user"
        
    def readSettings(self):
        pass # TODO -- ps: this is called multiple times so make sure to add a "isLoaded" variable
        
    def saveSettings(self):
        pass # TODO
        
    def doSavedSettingsExist(self):
        return True # TODO
        
    def setWindowedMode(self, boolean):
        self.windowed = boolean
        self.saveSettings()
        
    def getWindowedMode(self):
        return self.windowed
        
    def setMusic(self, boolean):
        self.music = boolean
        self.saveSettings()
        
    def getMusic(self):
        return self.music
        
    def setSfx(self, boolean):
        self.sfx = boolean
        self.saveSettings()
        
    def getSfx(self):
        return self.sfx
        
    def setToonChatSounds(self, boolean):
        self.toon_chat_sounds = boolean
        self.saveSettings()
        
    def getToonChatSounds(self):
        return self.toon_chat_sounds
        
    def setMusicVolume(self, value):
        self.music_vol = value
        self.saveSettings()
        
    def getMusicVolume(self):
        return self.music_vol
        
    def setSfxVolume(self, value):
        self.sfx_vol = value
        self.saveSettings()
        
    def getSfxVolume(self):
        return self.sfx_vol
        
    def setResolution(self, mode):
        self.res = mode
        self.saveSettings()
        
    def getResolution(self):
        return self.res
        
    def setEmbeddedMode(self, boolean):
        self.embedded = boolean
        self.saveSettings()
        
    def getEmbeddedMode(self):
        return self.embedded
        
    def setAcceptingNewFriends(self, boolean):
        self.acceptingNewFriends = boolean
        
    def getAcceptingNewFriends(self):
        return self.acceptingNewFriends
        
    def setAcceptingNonFriendWhispers(self, boolean):
        self.acceptingNonFriendWhispers = boolean
        
    def getAcceptingNonFriendWhispers(self):
        return self.acceptingNonFriendWhispers