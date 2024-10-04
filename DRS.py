import tkinter
import cv2
import PIL.Image , PIL.ImageTk
from functools import partial
import time
import threading
from playsound import playsound
import  imutils
import speech_recognition as sr
import pyaudio
SET_WIDTH = 650
SET_HEIGHT=368
flag=True
def pending(decision):
    #decision pending
    frame = cv2.cvtColor(cv2.imread("decision.png"), cv2.COLOR_BGR2RGB)
    frame= PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,ancho=tkinter.NW)

    #wait
    time.sleep(2)
    #sponsor
    frame1 = cv2.cvtColor(cv2.imread("nasir.png"), cv2.COLOR_BGR2RGB)
    frame1= PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
    canvas.image=frame1
    canvas.create_image(0,0,image=frame1,ancho=tkinter.NW)
    #wait
    time.sleep(1)

    #out not out
    if decision=='out':
        frame2 = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)
        frame2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
        canvas.image = frame2
        canvas.create_image(0, 0, image=frame2, ancho=tkinter.NW)
        playsound('out.mp3')
    else:
        frame2 = cv2.cvtColor(cv2.imread("notout.png"), cv2.COLOR_BGR2RGB)
        frame2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
        canvas.image = frame2
        canvas.create_image(0, 0, image=frame2, ancho=tkinter.NW)
        playsound("not out.mp3")

stream=cv2.VideoCapture('video2.mp4')

def play(speed):
    global flag
    print(f'you speed is {speed}')
    frame3=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame3+speed)

    grabbed,frame=stream.read()
    hey=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hey=imutils.resize(hey,width=SET_WIDTH,height=SET_HEIGHT)
    hey = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(hey))
    canvas.image=hey
    canvas.create_image(0,0,image=hey,ancho=tkinter.NW)
    if flag:
        canvas.create_text(300, 25, fill='red', font='Times 25  bold', text='DECISION PENDING...UMPIRE-NASIR')
    flag=not flag
def out():
    #pending('out')
    thread=threading.Thread(target=pending,args=('out',))
    thread.daemon=1
    thread.start()
    print("Player is out")
def not_out():
    thread=threading.Thread(target=pending,args=('notout',))
    thread.daemon=1
    thread.start()
    print("Player is not out")
def hello():
    def takeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            r.energy_threshold = 500
            r.pause_threshold = 0.5
            audio = r.listen(source)
        try:
            print('Recognising...')
            query = r.recognize_google(audio, language='en-in')
            print(f'User said {query}\n')

        except Exception as e:
            print(e)

            print("Say that again please...")
            return 'None'
        return query

    while True:
        takeCommand()
        if 'out' in takeCommand():
            out()
            break
        elif 'not out' in takeCommand() or 'not out' in takeCommand():
            not_out()
            break





window=tkinter.Tk()
window.title("Nasir review system")
cv_img=cv2.cvtColor(cv2.imread("1.png"),cv2.COLOR_BGR2RGB)
canvas=tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas=canvas.create_image(0,0,ancho=tkinter.NW,image=photo)

canvas.pack()
thread=threading.Thread(target=hello)
thread.start()
#button to control playback
btn=tkinter.Button(window,text="<<Previous (fast)",width=50,command=partial(play,-20))
btn.pack()
btn=tkinter.Button(window,text="<<Previous (slow)" ,width=50,command=partial(play,-2))
btn.pack()
btn=tkinter.Button(window,text="Next (fast)>>" ,width=50,command=partial(play,25))
btn.pack()
btn=tkinter.Button(window,text="Next (slow)>>" ,width=50,command=partial(play,1))
btn.pack()
btn=tkinter.Button(window,text="Give OUT" ,width=50,command=out)
btn.pack()
btn=tkinter.Button(window,text="Give Not Out" ,width=50,command=not_out)
btn.pack()
window.mainloop()


