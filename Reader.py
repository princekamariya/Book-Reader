import tkinter as tk
from tkinter import *
import PyPDF2
import pyttsx3
from tkinter import filedialog
import threading
import pytesseract
from PIL import Image
import pygame
import speech_recognition as sr
import pywhatkit
import datetime
import pyjokes
import keyboard
import os
from gtts import *

pygame.mixer.init()
engine = pyttsx3.init()

root = tk.Tk()
root.title('Book Reader - Read your PDF!')
root.iconbitmap('F:/React/')
root.geometry("600x700")

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

class Speaking(threading.Thread):
    def __init__(self, sentence, **kw):
        super().__init__(**kw)
        self.words = sentence.split()
        self.paused = False

    def run(self):
        self.running = True
        while self.words and self.running:
            if not self.paused:
                word = self.words.pop(0)
                my_text.insert(END, word + " ")
                print(word, " ")
                engine.setProperty('rate', 300)
                engine.say(word)
                engine.runAndWait()
        print("finished")
        self.running = False

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False


speak = None


def read():
    outfile = "temp.wav"
    engine.save_to_file(my_text.get('1.0', END), outfile)
    engine.runAndWait()
    pygame.mixer.init()
    pygame.mixer.music.load(outfile)
    pygame.mixer.music.play()


def stop():
    pygame.mixer.music.stop()


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()

engine = pyttsx3.init()
engine.setProperty("rate", 178)

def fileDailog():
    fileName = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                               filetype=(("jpeg", "*.jpg"), ("png", "*.png")))

    print(fileName)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = Image.open(fileName+'')

    text = pytesseract.image_to_string(img)

    textfile = open('file.txt', 'w')
    textfile.write(text)
    print("Text is written in file!")
    textfile.close()

    textfile = open('file.txt')
    text = textfile.read()

    lang = 'en'

    object = gTTS(text=text, lang=lang, slow=False)
    object.save("speech.mp3")

    os.system("speech.mp3")


def clear_text_box():
    my_text.delete(1.0, END)


def open_pdf():
    open_file = filedialog.askopenfilename(
        initialdir="F:/React/",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")
        )
    )
    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        no = 1.0
        for i in range(pdf_file.getNumPages()):
            page = pdf_file.getPage(i)
            page_stuff = page.extractText()
            my_text.insert(no, page_stuff)
            no = no + 1.0


def read_pdf():
    open_file = filedialog.askopenfilename(
        initialdir="F:/React/",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")
        )
    )
    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        no = 1.0
        for i in range(pdf_file.getNumPages()):
            page = pdf_file.getPage(i)
            page_stuff = page.extractText()
            my_text.insert(no, page_stuff)
            no = no + 1.0
        for i in range(pdf_file.getNumPages()):
            page = pdf_file.getPage(i)
            page_stuff = page.extractText()
            my_text.insert(no, page_stuff)
            no = no + 1.0
            speak = pyttsx3.init()
            speak.say(page_stuff)
            speak.runAndWait()

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa','')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play','')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'open' in command:
        talk('Please Upload PDF from your PC')
        button1.invoke()
    elif 'image' in command:
        talk('Please Upload Image from your PC')
        button7.invoke()
    elif 'stop' in command:
        talk('Now I am currently Paused, Just tell me Alexa Start Whenever you want to continue your reading')
        button2.invoke()
    elif 'start' in command:
        talk('I am Starting reading, Just tell me Alexa Stop whenever you want to Stop me')
        button6.invoke()
    elif 'exit' in command:
        talk('Thank you, Have a nice Day')
        button4.invoke()
    elif 'read' in command:
        talk('I am Starting reading, Just tell me Alexa Stop whenever you want to Stop me')
        button5.invoke()
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is '+ time)
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk("Please say the command again")

def infinite():
    while True:
        run_alexa()

keyboard.add_hotkey("F4", run_alexa)

keyboard.add_hotkey("F5",infinite)

button1 = Button(root, text="OpenPDF", width=12, bg='#03A9F4', fg='#fff', command=open_pdf)
button1.grid(row=4, column=0, padx=10, pady=10)

button2 = Button(root, text="Pause", width=12, bg='#03A9F4', fg='#fff', command=pause)
button2.grid(row=4, column=1, padx=10, pady=10)

button6 = Button(root, text="UnPause", width=12, bg='#03A9F4', fg='#fff', command=unpause)
button6.grid(row=5, column=0, padx=10, pady=10)

button3 = Button(root, text="Clear", width=12, bg='#03A9F4', fg='#fff', command=clear_text_box)
button3.grid(row=4, column=2, padx=10, pady=10)

button4 = Button(root, text="Exit", width=12, bg='#03A9F4', fg='#fff', command=root.quit)
button4.grid(row=4, column=3, padx=10, pady=10)

button5 = Button(root, text="Read", width=12, bg='#03A9F4', fg='#fff', command=read)
button5.grid(row=5, column=1, padx=10, pady=10)

button7 = Button(root, text="Upload Image", width=12, bg='#03A9F4', fg='#fff', command=fileDailog)
button7.grid(row=5, column=2, padx=10, pady=10)

my_text = Text(root, height=60, width=62)
my_text.grid(row=6, columnspan=4)

# Set the position of button on the top of window.
root.mainloop()