from gtts import gTTS
import os

f_t = open('resource/1791.txt', mode='r+', encoding='utf-8')

with open('1791.mp3', 'wb') as f:
    for l in f_t:
        l = l.strip()
        if l != "":
            print(l)
            audio = gTTS(text=l, lang="vi", slow=False)   
            audio.write_to_fp(f)
   
os.system("start 1791.mp3")
