import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
import warnings

warnings.filterwarnings("ignore")

books=pd.read_csv('C:\\Users\\Manjunath\\Desktop\\BTech Projects\\Major_Project\\AI Assistant\\csv files\\BX-Books.csv',sep=";",error_bad_lines=False,warn_bad_lines=False,encoding='latin-1')
books["Book-Title"]=books["Book-Title"].str.lower()
books=books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]
books.rename(columns={'Book-Title':'title','Book-Author':'author','Year-Of-Publication':'year'},inplace=True)
users=pd.read_csv('C:\\Users\\Manjunath\\Desktop\\BTech Projects\\Major_Project\\AI Assistant\\csv files\\BX-Users.csv',sep=";",error_bad_lines=False,warn_bad_lines=False,encoding='latin-1')
ratings=pd.read_csv('C:\\Users\\Manjunath\\Desktop\\BTech Projects\\Major_Project\\AI Assistant\\csv files\\BX-Book-Ratings.csv',sep=";",error_bad_lines=False,warn_bad_lines=False,encoding='latin-1')
users.Age.hist(bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
plt.title('Age Distribution\n')
plt.xlabel('age')
plt.ylabel('count')
plt.savefig('age_dist.png', bbox_inches='tight')
book_data=books
book_data.year = pd.to_numeric(book_data.year, errors='coerce')
book_data.year.replace(0, np.nan, inplace=True)
year = book_data.year.value_counts().sort_index()
year = year.where(year>5) 
plt.figure(figsize=(10, 8))
plt.rcParams.update({'font.size': 15}) 
plt.bar(year.index, year.values)
plt.xlabel('Year of Publication')
plt.ylabel('counts')
x=ratings['User-ID'].value_counts()>200
y=x[x].index
y
ratings=ratings[ratings['User-ID'].isin(y)]
ratings_books=ratings.merge(books,on='ISBN')
grp_rating=ratings_books.groupby('title')['Book-Rating'].count().reset_index()
grp_rating.rename(columns={'Book-Rating':'no-of-rating'},inplace=True)
final_ratings=ratings_books.merge(grp_rating,on='title')
final_ratings.rename(columns={'Book-Rating':'BookRating','no-of-rating':'noofrating'},inplace=True)
plt.rc("font", size = 15)
final_ratings.BookRating.value_counts(sort = False).plot(kind = 'bar')
plt.title('Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.plot()
plt.savefig("Ratings Distribution.jpg", bbox_inches = "tight", dpi = 100)
grp_rating.columns
final_ratings.shape
final_ratings=final_ratings[final_ratings['noofrating']>=50]
final_ratings.drop_duplicates(['User-ID','title'],inplace=True)
book_pivot=final_ratings.pivot_table(columns='User-ID',index='title',values='BookRating')
book_pivot.fillna(0,inplace=True)
import scipy
from scipy.spatial.distance import correlation
from scipy.sparse import csr_matrix
book_sparse=csr_matrix(book_pivot)
from sklearn.neighbors import NearestNeighbors
model=NearestNeighbors(algorithm='brute')
model.fit(book_sparse)
distances, suggestions= model.kneighbors(book_pivot.iloc[147,:].values.reshape(1,-1),n_neighbors=6)

def Recommend_Book(Name_of_Book):
    book_id=np.where(book_pivot.index==Name_of_Book)[0][0]
   # print(book_id)
    distances, suggestions= model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1),n_neighbors=6)
    a=[]
    for i in range(1,len(suggestions[0])):
        a.append(book_pivot.index[suggestions[0][i]])
    return a

def Recommend_BookT(no_before_book=None):
    return no_before_book

g=Recommend_Book('dead run')
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
movies=pd.read_csv(r'C:\\Users\\Manjunath\\Desktop\\BTech Projects\\Major_Project\\AI Assistant\\csv files\\movies.csv')
ratings=pd.read_csv(r'C:\\Users\\Manjunath\\Desktop\\BTech Projects\\Major_Project\\AI Assistant\\csv files\\ratings.csv')
movies["title"]=movies["title"].str.replace("[)(,.:;!%$@^&*?<>{}\|/~`]","")
movies["title"]=movies["title"].str.lower()
dataset=pd.merge(ratings,movies,on='movieId')
dataset.tail()
import datetime
from datetime import datetime,date
dataset['datetime']=pd.to_datetime(dataset['timestamp'])
a=dataset
a=a.groupby('title')['rating'].mean()
sorted_ratings_mov=a.sort_values(ascending=False)
b=dataset.groupby('title')['rating'].count()
new_record=pd.DataFrame()
new_record['Average_ratings']=a
new_record['count of total ratings']=b
import seaborn as sns
sns.set_style('white')

import pandas.util.testing as tm
movie_matrix=dataset.pivot_table(index='userId',columns='title',values='rating')
rt=movie_matrix['xxx 2002']
mv=movie_matrix.corrwith(rt)
movie_smlr_mv=pd.DataFrame(mv,columns=['Correlation'])
movie_smlr_mv.dropna(inplace=True)

def Recommend_MOVIE(mv_n):
    rtg=movie_matrix[mv_n]
    mve=movie_matrix.corrwith(rtg)
    #movie_smlr_mv=pd.DataFrame(mve,columns=['Correlation'])
    #movie_smlr_mv.dropna(inplace=True)
    #a.sort_values(by=['Correlation'])
    mve.dropna(inplace=True)
    mve=mve.sort_values(ascending=False)
    mve=mve.head(5)
    return mve

def Recommend_MOVIET():
    return sorted_ratings_mov.head(5)

#a=Recommend_MOVIE('toy story 1995')


import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import time
import subprocess
import winshell
import ctypes

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")  
    else:
        speak("Good Evening Sir!")  
    speak("I am your assistant. Please tell me how may I help you")
    query()

ok=0  
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.record(source,duration=5)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
        #ok=1
    except Exception as e:
        speak("Say that again please...")  
        return "None"
    return query

def Movie_Recommenders(id):
    if id==0:
        speak('Search for any similar Movie?')
        print('Search for any similar Movie?')
    elif id==1:
        speak('Tell that again')
        print('Tell that again')
    q=takeCommand().lower()
    ok=0
    if 'go back' in q:
        return
    if 'yes' in q:
        speak('Tell Movie Name')
        print('Tell Movie Name')
        mov_name=takeCommand().lower()
        ok=1
        a=Recommend_MOVIE(mov_name)
        print('Recommended Movies for:'+str(mov_name))
        speak('Recommended Movies for:'+str(mov_name))
        print(a)
    elif 'no' in q:
        a=Recommend_MOVIET()
        print('Recommended movies are:')
        speak('Recommended movies are')
        ok=1
        print(a)
    if ok==0:
        Movie_Recommenders(1)
    return

def Book_Recommenders(id):
    if id==0:
        speak('Search for any similar Book?')
        print('Search for any similar Book?')
    elif id==1:
        speak('Tell that again')
        print('Tell that again')
    q=takeCommand().lower()
    ok=0
    if 'go back' in q:
        return
    if 'yes' in q:
        speak('Tell Book Name')
        print('Tell Book Name')
        bk_name=takeCommand().lower()
        ok=1
        a=Recommend_Book(bk_name)
        print('Recommended Books for:'+str(bk_name))
        speak('Recommended Books for'+str(bk_name))
        for x in a:
            print(x)
    elif 'no' in q:
        a=Recommend_BookT()
        print('Recommended Books are:')
        speak('Recommended books are')
        ok=1
        for x in a:
            print(x)
    if ok==0:
        Book_Recommenders(1)
    return

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('18211A1224@bvrit.ac.in', 'sridhar73') 
    server.sendmail('18211A1224@bvrit.ac.in', to, content)
    server.close()

import cv2
from deepface import DeepFace
import time
from pygame import mixer
import random

emotions = {"angry" : 0, "disgust" : 0, "fear" : 0, "happy" : 0, "neutral" : 0, "sad" : 0, "surprise" : 0}
songs = [["No Pelli.mp3","Single-Pasanga.mp3"],["Manasaa.mp3","Naalona Pongenu.mp3"],["Lala Bheemla.mp3","Rowdy Baby.mp3"],
         ["Hoyna Hoyna.mp3","Ye Chota Nuvvunna.mp3"],["The Karma Theme.mp3"],["Adiga Adiga.mp3","Emai Poyave.mp3"],
         ["Gunjukunna.mp3","Pavizha-Mazha.mp3"]]

def playSong(final_emotion):
    ind = list(emotions.keys()).index(final_emotion)
    song = random.choice(songs[ind])
    path = "C:\\Users\\Manjunath\\Desktop\\BTech Projects\\Major_Project\\AI Assistant\\songs\\"+final_emotion+"\\"+song
    speak("It seams you are"+final_emotion+"sir")
    speak("playing"+song)
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)

def music():
    capture = cv2.VideoCapture(0)
    for i in range(20):
        _, frame = capture.read()
        prediction = DeepFace.analyze(frame, actions = ["emotion"])
        emotion = prediction["dominant_emotion"]
        emotions[emotion] += 1
    final_emotion = ""
    count = 0
    for emotion in emotions.keys():
        if emotions[emotion]>=count:
            final_emotion = emotion
            count = emotions[emotion]
    capture.release()
    cv2.destroyAllWindows
    playSong(final_emotion)


def query():
    while True:
        query = takeCommand().lower()
        #query = "open google"
        #query="open google"
        if'wikipedia' in query:
            speak('Searching Wikipedia...')
            #query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            speak('Searching youtube ...')
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak('Searching google ...')
            webbrowser.open("google.com")
        elif 'open firefox' in query:
            speak('Searching firefox ...')
            webbrowser.open("firefox.com")
        elif 'hi' in query:
            speak('Hi Sir , tell me , how can i help you')
        elif 'open stackoverflow' in query:
            speak('Searching stackoverflow ...')
            webbrowser.open("stackoverflow.com")
        elif ('play music' in query) or ('play songs' in query) or ('play song' in query):
            music_dir= r'C:\Users\Manjunath\Desktop\BTech Projects\Major_Project\AI Assistant\songs\happy'
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[3]))
        elif 'exit' in query:
            print('Thank you Sir, see you again, have a good day')
            speak('Thank you Sir, see you again, have a good day')
            break
        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")
        elif 'change background' in query:
            ctypes.windll.user32.SystemParametersInfoW(20,0,"Location of wallpaper",0)
            speak("Background changed successfully")
        
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)
        elif 'who are you' in query:
            speak('Im your Voice assistant sir')
        elif 'time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime} Sir")
        elif 'date' in query:
            strDate=datetime.date.today()
            speak(f"Todays date is {strDate} Sir")
        elif 'open powerpoint' in query:
            codePath=r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
            os.startfile(codePath)
        elif 'open notepad' in query:
            codePath=r"C:\Windows\System32\notepad.exe"
            os.startfile(codePath)
        elif 'open zoom' in query:
            speak('opening zoom')
            webbrowser.open("zoom.com")
        elif 'open facebook' in query:
            speak('opening facebook')
            webbrowser.open("facebook.com")
        elif ('open instagram' in query) or ('open insta' in query):
            speak('opening Instagram')
            webbrowser.open("instagram.com")
        elif ' book' in query:
            Book_Recommenders(0)
        elif 'movie' in query:
            Movie_Recommenders(0)
        elif 'music' in query:
            music()
        elif 'email to aravind' in query:
            try:
                speak("what should i say")
                content=takeCommand()
                to="18211a1224@bvrit.ac.in"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry sir, Im not able to send this mail.")

#__name__="main"
if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("600x400")
    window.title("Assistant")
    #mic_img = Image.open("C:\\Users\\Manjunath\\Desktop\\Major project\\AI Assistant\\age_dist.png")
    #mic_img = mic_img.resize((200,200))
    #mic_img = ImageTk.PhotoImage(mic_img)
    #image=mic_img,
    mic_img = tk.Button(window, text="mic", height = 200, width = 200, borderwidth = 5, command = wishMe).place(relx=0.5, rely = 0.5, anchor = "center")
    window.mainloop()
