import pyttsx3

class TextToSpeech:
    def __init__(self, text='', rate=200, volume=1):
        self.engine = pyttsx3.init()
        self.text = text
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def setText(self, text : str):
        self.text = text

    def setRate(self, rate: int):
        self.engine.setProperty('rate', rate)

    def setVolume(self, volume: float):
        self.engine.setProperty('volume', volume)

    def sayText(self):
        self.engine.say(self.text)
        self.engine.runAndWait()