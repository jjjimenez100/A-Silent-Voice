import Modules.TextToSpeech as tts
class WordBuilder:
    def __init__(self):
        self.currentWord = ""
        self.tts = tts.TextToSpeech(rate=130)
        self.currentLetter = ""
        self.consecutiveCount = 0

    def changeRate(self, rate):
        self.tts.setRate(rate)

    def changeVolume(self, volume):
        self.tts.setVolume(volume)

    def checkLetter(self, letter):
        if self.currentLetter == "":
            self.currentLetter = letter
        elif self.consecutiveCount>=40:
            self.currentWord += self.currentLetter
            self.currentLetter = ""
            self.consecutiveCount = 0
        elif letter == self.currentLetter:
            self.consecutiveCount += 1
        else:
            self.currentLetter = ""
            self.consecutiveCount = 0
        return self.currentWord

    def getWord(self):
        return self.currentWord

    def sayWord(self):
        self.tts.setText(self.currentWord)
        self.tts.sayText()

    def setWord(self, word):
        self.currentWord = word