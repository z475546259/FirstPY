
# coding:utf-8
def tts(txt):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(txt)
    engine.runAndWait()
tts("欢迎回家，张治强")