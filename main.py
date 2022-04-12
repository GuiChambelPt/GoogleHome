from gtts import gTTS
import time, datetime, os, requests, sqlite3, json
import speech_recognition as sr
from pygame import mixer

audio = sr.Recognizer()
banco = sqlite3.connect('./data/main.db')
baseurl = "http://127.0.0.1:1111/"
cursor = banco.cursor()
lang = 'pt-PT'
def execute_command():
    try:
        with sr.Microphone() as source:
            print('Listening..')
            voice = audio.listen(source)
            command = audio.recognize_google(voice, language=lang)
            command = command.lower()
            if 'google' in command:
                print(command)
    except:
        print("Error")
    return command

def command_voice():
    
    command = execute_command()
    if 'google' in command:
        if 'curiosidade' in command:
            resp = requests.get(url="http://127.0.0.1:1111/curiosidades/")
            data = resp.json()
            print(data)
            curiosidade = data["Curiosidades"]
            tts = gTTS(text=curiosidade, lang=lang)
            tts.save("./audiotemp/curiosidade.mp3")
            mixer.init()
            mixer.music.load("./audiotemp/curiosidade.mp3")
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(1)
            command_voice()
        if 'horas' in command:
            horahora = datetime.datetime.now().strftime('%H')
            horaminuto = datetime.datetime.now().strftime('%M')
            print(horahora)
            print(horaminuto)
            horas = ("Agora são {} horas e {} minutos.".format(horahora, horaminuto))
            tts = gTTS(text=horas, lang='pt-PT')
            tts.save("./audio/horas.mp3")
            mixer.init()
            mixer.music.load("./audio/horas.mp3")
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(1)
            command_voice()
        if 'tempo em' in command:
            baseweatherurl = "http://127.0.0.1:1111/weather/&c="
            command = command.replace("tempo em ", "")
            command = command.replace("google", "")
            city = command
            city = city.replace(" ",'')
            print(city)
            weatherurl = baseweatherurl + city
            weather1 = requests.get(url=weatherurl)
            weather = weather1.json()
            print(weather)
            finalweather = weather["WeatherDescription"]
            name = weather["name"]
            temp = weather["Temp"]
            temp_max = weather["Temp_max"]
            temp_min = weather["Temp_min"]
            text = ("O tempo em {} está com {} estão {}graus, com máxima de {}graus e mínima de {}graus, informação por OpenWeather.".format(name,finalweather, temp, temp_max, temp_min))
            tts = gTTS(text=text, lang="pt-PT")
            tts.save("./audio/weather.mp3")
            mixer.init()
            mixer.music.load("./audio/weather.mp3")
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(1)
            command_voice()
        if 'traduz' in command:
            text = command
            text = text.replace("para ", "")
            text = text.replace("google", "")
            text = text.replace("traduz", "")
            print(text)
            if "inglês" in text:
                text = text.replace("inglês", "")
                basetranslatorurl = "http://127.0.0.1:1111/translator/"
                srclanguage = "pt"
                destination = "en"
                finaltransalatorurl = basetranslatorurl + "&src=" + srclanguage + "&d=" + destination + "&p=" + text 
                phraserequest = requests.get(url=finaltransalatorurl)
                phraserequest = phraserequest.json()
                transalatedphrase = phraserequest["Translate_text"]
                tts = gTTS(text=transalatedphrase, lang=srclanguage)
                tts.save("./audio/translator.mp3")
                mixer.init()
                mixer.music.load("./audio/translator.mp3")
                mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(1)
        if 'procure por':
            tosearch = command
            tosearch = tosearch.replace("procure", "")
            tosearch = tosearch.replace("procura", "")
            tosearch = tosearch.replace("por ", "")
            tosearch = tosearch.replace("google", "")
            print(tosearch)
            lang="pt"
            requesturl= baseurl + "wikipedia/" + "&lang=" + lang + "&s=" + tosearch 
            request = requests.get(url=requesturl)
            request = request.json()
            summary = request["Summary"]
            tts = gTTS(text=summary, lang="pt-PT")
            tts.save("./audio/wikipedia.mp3")
            mixer.init()
            mixer.music.load("./audio/wikipedia.mp3")
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(1)
    else:
        command_voice()
    
        
def start():
    f = open ('data/data.json', "r+")
    data = json.loads(f.read())
    everstarted = data["everstarted"]
    
    if everstarted == "False":
        cursor.execute("CREATE TABLE Users(id integer,user text,email text)")
        stats = {"everstarted": "True","timesstarted": 0}
        jsonString = json.dumps(stats)
        f.write(jsonString)
        f.close()
        print("Criando DataBase, e o resto")
    else:
        timesstarted = data["timesstarted"]
        timesstarted = timesstarted + 1
        stats2 = {"everstarted": "True","timesstarted": timesstarted}
        jsonString = json.dumps(stats2)
        f.write(jsonString)
        f.close()
        command_voice()


        
if __name__ == "__main__":
    command_voice()