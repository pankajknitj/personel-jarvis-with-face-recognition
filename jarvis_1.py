#need to give your own song list with path in list named track

import speech_recognition as sr
import face_recognition as fc
import numpy as np
import pandas as pd
import cv2 as cv
import time as t
import vlc
import random as r
import pyttsx3 as sx
import wikipedia
from datetime import date
from googlesearch import search
import webbrowser as wb
import requests, json
import geocoder
from pynput.mouse import Button,Controller

v=cv.VideoCapture(0)
try:
    db=pd.read_csv('jarvise_image.csv')
    label=list(db['labels'])
    d=np.array(db)
    db_image=list(d[:,1:129])
    db_inf=pd.read_csv('person_imformation.csv')
    log=open('log.txt','r+')
    log_data=log.read()
    print("i'm ready")
except:
    print('file not available')
    label=[]
    db_image=[]
    db_inf=[]
    



def log_(data,jarvis=True):
    if jarvis==False:
        log.write(user+' :'+data+'\n')
    else:
        log.write('Jarvis :'+data+'\n')


        
def take_image():
    r,live=v.read()
    if r==True:
        face=fc.face_locations(live)
        if len(face)>0:
            [x1,y1,x2,y2]=face[0]
            cv.rectangle(live,(y2,x1),(y1,x2),(0,0,255),3)
            cv.imshow('image',live)
            cv.waitKey(4)
            e=fc.face_encodings(live,face)[0]
            return e
        else:
            return take_image()
    
def find_label():
    try:
        l=label[-1]+1
    except:
        l=0
    return l

def save_(dataframe1,dataframe2):
    if len(label)>0:
        dataframe2.to_csv('person_imformation.csv',mode='a',header=False)
        dataframe1.to_csv('jarvise_image.csv',mode='a',header=False)
    else:
        dataframe2.to_csv('person_imformation.csv')
        dataframe1.to_csv('jarvise_image.csv')
    
    
def say(word):
    engine=sx.init()
    engine.setProperty('rate', 100)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)
    engine.say(word)
    engine.runAndWait()
    
def face_recognizer():
        e=take_image()
        res=fc.compare_faces(db_image,e)
        if True in res:
            index=label[res.index(True)]
            return index
        else:
            print("i'm not recognizing you,come in front of camera to take few pictures")
            l=find_label()
            E=[]
            n=[]
            q=[]
            a=[]
            count=1
            while count<=5:
                e=take_image()
                E.append(e)
                count+=1
            dataframe1=pd.DataFrame(E)
            dataframe1['labels']=[l,l,l,l,l]
            name,quali,age=input("enter name qualification and age seprated by ','").split(',')
            n.append(name)
            q.append(quali)
            a.append(age)
            dataframe2=pd.DataFrame({'name':n,'qualification':q,'age':a})
            save_(dataframe1,dataframe2)
            return l
            

def speech_recognizer():
    global word
    word=input('enter...')
    return word
'''def speech_recognizer():
    s=sr.Recognizer()
    with sr.Microphone() as source:
        print('speak...')
        s.adjust_for_ambient_noise(source)
        audio=s.listen(source)
    try:
        d=s.recognize_google(audio)
        d=d.lower()
        return d
    except Exception as e:
        print("coudn't recognize")
        return speech_recognizer()'''


def vlc_player(word,player=''):
    ps=list                       #previous state
    track=['D:\Downloads\Video\(643) Tu Cheez Badi 4k Video song - YouTube.MKV',
           'D:\Downloads\Video\(643) Official Video- Humnava Mere Song - Jubin Nautiyal - Manoj Muntashir - Rocky - Shiv - Bhushan Kumar - YouTube.MKV',
           'D:\Downloads\Video\(643) Full Video- Tera Yaar Hoon Main - Sonu Ke Titu Ki Sweety - Arijit Singh Rochak Kohli - Song 2018 - YouTube.MKV',
           'D:\Downloads\Video\(643) Yo Yo Honey Singh- DIL CHORI (Video) Simar Kaur, Ishers - Hans Raj Hans - Sonu Ke Titu Ki Sweety - YouTube.MKV,',
           'D:\Downloads\Video\(643) Saiyaara - Full Song - Ek Tha Tiger - Salman Khan - Katrina Kaif - Mohit Chauhan - Taraannum Mallik - YouTube.MKV',
           'D:\Downloads\Video\(643) Bom Diggy Diggy (VIDEO) - Zack Knight - Jasmin Walia - Sonu Ke Titu Ki Sweety - YouTube.MKV']


    v=cv.VideoCapture(0)
    fd=cv.CascadeClassifier(r'C:\Users\pankaj kumar\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
    
    #while True:
    status,image=v.read()
    if status==True:
        if 'open vlc' in word or 'play song' in word:
            song=track[r.randint(0,5)]
            player=vlc.MediaPlayer(song)
            gray_image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
            face=fd.detectMultiScale(gray_image)
            for [x,y,w,h]in face:
                cv.rectangle(image,(x,y),(x+w,y+h),(255,255,255),1)

            k=cv.waitKey(3)
            cs=type(face)
            if ps!=cs:
                ps=cs
                if type(face)==tuple:
                    player.pause()
                else:
                    player.play()
            return player        
        elif 'stop' in word or 'close' in word:
            player.stop()
            cv.destroyAllWindows()
            #break
        elif 'next' in word or 'next song' in word:
            player.stop()
            player=vlc.MediaPlayer(track[r.randint(0,len(track)-1)])           #5 also be included not excluded here in randint()
            player.play()
            return player
        elif 'pause' in word:
            player.pause()
        elif 'play' in word:
            player.play()
        cv.imshow('my image',image) 


def browser(word):
    mouse=Controller()
    if 'next recomended song' in word:
            mouse.position=(1000,200)
            mouse.press(Button.left)
            mouse.release(Button.left)
            print('Jarvis :next song played')
            say('next song played')
            log_('next song played')
    else:
        try:
            print('Jarvis :searchng in progress...please wait!')
            say('searchng in progress...please wait!')
            log_('searchng in progress...please wait!')
            #word=speech_recogniser()
            for link in search(word,tld='co.in',num=1,stop=1,pause=2):
                print("Jarvis :obtaied link :"+link)
                log_(link)
                wb.open(link)
            if 'youtube' in word:    
                t.sleep(1)    
                mouse=Controller()
                #mouse.position=(400,300)
                #mouse.press(Button.left)
                #mouse.release(Button.left)
            
            
                print('jarvis :done')
            print("Jarvis :"+'searching done!')
            say('searching done!')
            log_('searching done!')
        except:
            p='sorry!\n word not recognized try again.'
            print(p)
            log_(p)
            return browser()

def Wikipedia():
    try:
        print('Jarvis :what you want to search?')
        say('what you want to search?')
        log_('what you want to search?')
        word=speech_recognizer()
        print(user+' :'+word)
        wi=wikipedia.summary(word, sentences=1)
        print("Jarvis :" ,wi)
        say(wi)
        log_(word,False)
        log_(wi)
    except:
        print('hey!\n'+'Matching not found try with different words')
        log_('hey!\n'+'Matching not found try with different words')
        return Wikipedia()

def mouse_(word='a'):
  while 1:
    if word=='a':
        word=speech_recognizer()
    mouse=Controller()
    if 'down' in word:
        mouse.move(0,40)
    elif 'up' in word or 'upper side' in word:
        mouse.move(0,-40)
    elif 'right' in word:
        mouse.move(40,0)
    elif 'left' in word:
        mouse.move(-40,0)
    elif 'on first link' in word :
        mouse.position=(250,300)
    elif 'first link' in word:
        mouse.position=(250,300)
        mouse.press(Button.left)
        mouse.release(Button.left)
    elif 'at middle' in word:
        mouse.position(670,400)
    if 'left click' in word or 'click left' in word:
        mouse.press(Button.left)
        mouse.release(Button.left)
    if'right click' in word or 'click right' in word:
         mouse.press(Button.right)
         mouse.release(Button.right)
    elif 'stop song' in word or 'play' in word or 'paly song' in word:
        mouse.position=(400,300)
        mouse.press(Button.left)
        mouse.release(Button.left)     
    else :
        return word
    word='a'
   
def conversation(matched_index):
    global user
    user=db_inf['name'][matched_index]
    if matched_index==0:
        print('welcome admin,how can i help you')
        say('welcome admin,how can i help you')
    else:    
        print('welcome to personel jarvis,  how can i help you')
        say('welcome to personel jarvis,  how can i help you')
    
    while True:
        word=speech_recognizer()
        print('Jarvis :recognized word :',word)
        log_(word,False)
        res=''
        if 'google' in word or 'browser' in word or 'youtube' in word or 'tell me' in word or 'what' in word or 'recomended' in word or 'search' in word or 'website' in word:
            browser(word)
            word=mouse_()
        elif 'stop song' in word or 'play' in word or 'paly song' in word:
            mouse_(word)
        elif 'who are you' in word or 'give your intro' in word:
            res="i'm a personel jarvis of pankaj.i can also help you by providing some imformation if you want"
            print('Jarvis :'+res)
            say(res)
        elif 'hello' in word or 'hi' in word:
            res='hii!...how can i help you'
            print('jarvis :'+res)
            say(res)
        elif 'manufacturer' in word:
            res='pankaj kumar,he made me durring summer training in techienest,jaipur by saurabh sir.at that time he was persuing B.tech from nit jalandhar'
            print('Jarvis :'+res)
            say(res)
        elif 'how are you' in word:
            res='fine and i am not intrested in know your fucking mood,want any help than stay otherwise get out from here'
            print('Jarvis :'+res)
            say(res)
        elif "wikipedia" in word:
            Wikipedia()
        
        elif "today's date" in word or 'date' in word:
            d=str(date.today())
            res="today's date is :"+d
            print('Jarvis :'+res)
            say(res)
        elif 'time' in word or 'current time' in word:
            time=t.ctime()
            time=str(time.split(' ')[4])
            res='current time :'+time
            print('Jarvis :'+res)
            say('current time is'+str(time.split(':')[0:2]))

        elif "weather" in  word or "temperature" in  word:
            say("Tell your city")
            log_("Tell your city")
            city_name=speech_recognizer()
            print("city you said is",city_name)
            #city_name=input("enter city name to confirm")
            api_key = "cca979ed5fb2c8d3a9c99594191482f9"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
            json_data=requests.get(complete_url).json()
            try:
                temp=json_data['main']
                temp=str(int(int(temp['temp'])-273.15))
                temp1=json_data['weather'][0]['description']
                d =" Current Temperature in "+city_name+" is "+temp+" degree celsius with "+temp1
                print("Jarvis : ",d)
                say(d)
                log_(d)
            except KeyError:
                print("Key invalid or city not found")    

        elif "location" in word:
            g = geocoder.ip('me')
            lat=g.latlng
            str1= "latitude position is "+str(lat[0])
            str2= "longitude position is "+str(lat[1])
            print("Jarvis: ",str1)
            print("Jarvis: ",str2)
            d= str1 +str2
            log_(d)
            say(str1)
            say(str2)
        elif 'bye' in word or 'bye jarvis' in word:
            log_(word)
            break
        log_(res)
        if matched_index==0:
            if 'open vlc' in word or 'play song' in word:
                #print('processing...')
                #say('processing...')
                global player
                player=vlc_player(word)
            if 'next song' in word or 'pause' in word or 'play' in word or 'stop song' in word or 'close' in word:
                try:
                    player=vlc_player(word,player)
                except:
                    pass
        
        

flag=1
global matched_index
while True:
    if flag!=0:
        matched_index=face_recognizer()
        if not(str(date.today())+'*' in log_data):
            print('you are first recognizer!')
            log.write('**********************************************************\n')
            log.write(str(date.today())+'*\n')
    conversation(matched_index)
    log.write('                *********                  ')
    log.close()
    log=open('log.txt','r+')
    log_data=log.read()
    flag=1

    
            
