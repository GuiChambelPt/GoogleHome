from gtts import gTTS
import time
import speech_recognition as sr
from pygame import mixer
tts = gTTS(text="Ola eu sou bue fixe tipo bue", lang='pt-BR')
tts.save("./audiotemp/1.mp3")
mixer.init()
mixer.music.load('./audiotemp/1.mp3')
mixer.music.play()
while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)

