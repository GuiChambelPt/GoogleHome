from gtts import gTTS
import time, datetime
import speech_recognition as sr
from pygame import mixer
audio = sr.Recognizer()

def executar_comando():
    try:
        with sr.Microphone() as source:
            print('Ouvindo..')
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'google' in comando:
                print(comando)
                vezesexecutado = 0
    except:
        mixer.init()
        mixer.music.load("./audios/erromicrofone.mp3")
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        quit()
    return comando

def comando_voz():
    comando = executar_comando()
    if 'horas' or 'hora' in comando:
        horahora = datetime.datetime.now().strftime('%H')
        horaminuto = datetime.datetime.now().strftime('%M')
        print(horahora)
        print(horaminuto)
        horas = ("Agora são {} horas e {} minutos.".format(horahora, horaminuto))
        tts = gTTS(text=horas, lang='pt-BR')
        tts.save("./audiotemp/horas.mp3")
        mixer.init()
        mixer.music.load("./audiotemp/horas.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
    if 'barra' or 'barras' in comando:

    
comando_voz()