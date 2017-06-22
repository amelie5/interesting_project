#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# import sys
# import webbrowser
#
# sys.path.append("libs")
#
# url = 'http://www.baidu.com'
# webbrowser.open(url)
# print(webbrowser.get())






import speech_recognition as sr

# use the audio file as the audio source
r = sr.Recognizer()
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    print(audio)