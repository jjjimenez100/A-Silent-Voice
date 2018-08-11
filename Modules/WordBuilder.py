# import Modules.TextToSpeech as tts
class WordBuilder:
    def __init__(self):
        self.currentWord = ""
        # self.tts = tts.TextToSpeech(rate=130)
        self.currentLetter = ""
        self.talking = False
        self.consecutiveCount = 0

    def changeRate(self, rate):
        self.tts.setRate(rate)

    def changeVolume(self, volume):
        self.tts.setVolume(volume)

    def checkLetter(self, letter):
        if self.currentLetter == "":
            self.currentLetter = letter
        elif self.consecutiveCount>=100:
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
        if not self.talking:
            self.talking = True
            print("speaking")
            self.tts.setText(self.currentWord)
            self.tts.sayText()
            self.talking = False
            print("done speaking")
            return True
        return False

    def setWord(self, word):
        self.currentWord = word
