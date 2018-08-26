# Class to 'build' words that was inputted and returns the word created.
class WordBuilder:
    def __init__(self):
        self.currentWord = ""
        # self.tts = tts.TextToSpeech(rate=130)
        self.currentLetter = ""
        self.talking = False
        self.consecutiveCount = 0

    # Changes the rate in how fast to speak in the text to speech module
    # DEPRECATED
    def changeRate(self, rate):
        # self.tts.setRate(rate)
        pass

    # Changes the volume of the text to speech voice
    # DEPRECATED
    def changeVolume(self, volume):
        # self.tts.setVolume(volume)
        pass

    # Checks the letter to be placed into the word
    # If its the same letter 85 times, the current letter is placed into the word
    def checkLetter(self, letter):
        if self.currentLetter == "":
            self.currentLetter = letter
        elif self.consecutiveCount >= 60:
            self.currentWord += self.currentLetter
            self.currentLetter = ""
            self.consecutiveCount = 0
        elif letter == self.currentLetter:
            self.consecutiveCount += 1
        else:
            self.currentLetter = ""
            self.consecutiveCount = 0
        return self.currentWord

    # Gets the current word built
    def getWord(self):
        return self.currentWord

    # Gets the current word and passes it to the text to speech module to be said
    # DEPRECATED
    def sayWord(self):
        # if not self.talking:
        #     self.talking = True
        #     print("speaking")
        #     self.tts.setText(self.currentWord)
        #     self.tts.sayText()
        #     self.talking = False
        #     print("done speaking")
        #     return True
        # return False
        pass

    # Changes the word to the inputted word
    # DEPRECATED
    def setWord(self, word):
        self.currentWord = word
        pass
