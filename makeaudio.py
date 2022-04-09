from gtts import gTTS
tts = gTTS(text="Ocorreu um erro verifique o seu microfone", lang='pt-BR')
tts.save("./audios/erromicrofone.mp3")