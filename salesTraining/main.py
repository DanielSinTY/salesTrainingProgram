
from pathlib import Path
import pygame
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
import wave
import numpy 
import argparse
import tempfile
import queue
import sys
import threading
import sounddevice as sd
import soundfile as sf
import os
import time
from pygame import mixer
import time
import drive
import analyze
import joblib
from tkinter.filedialog import askopenfilename, askopenfilenames
import shutil
import trainMLP
import tkinter.scrolledtext as scrolledtext
original=sys.stdout.write

# Redirect the print function so that verbose of sklearn can be shown on tkinter window
def redirector(inputStr):
    global trainingText
    global window
    if not inputStr.strip():
        return
    bar='█'*50
    
    trainingText.set(f"Analyzing successful data: |{bar}| {100}% Completed\nAnalyzing poor data: |{bar}| {100}% Completed\n"+inputStr.strip())
    window.update()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

# Get path to assets for tkinter to load button images
def relative_to_assets(path: str) -> Path:
    return resource_path(ASSETS_PATH / Path(path))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize all recording and playback device
mixer.init()
MUSIC_END = pygame.USEREVENT+1
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
pygame.init()
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

#Initialize the program window
window = Tk()

window.geometry("960x540")
window.geometry("+100+50")
photo = PhotoImage(file = relative_to_assets('icon.png'))
window.iconphoto(False, photo)
window.winfo_toplevel().title("S.T.E.P.")

window.configure(bg = "#EAFCFF")
window.resizable(False, False)

#Screen shown to ask users to upload files to train the model
def uploadData():
    global goodFiles
    global badFiles
    goodFiles=[]
    badFiles=[]
    for i in window.winfo_children():
        i.destroy()
    canvas = Canvas(
    window,
    bg = "#D6F0F3",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("train_button_1.png"))
    homeBtn = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=home,
        relief="flat"
    )
    homeBtn.place(
        x=25.0,
        y=383.0,
        width=326.0,
        height=120.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("train_button_2.png"))
    uploadGoodBtn = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: uploadDataFiles(1),
        relief="flat"
    )
    uploadGoodBtn.place(
        x=25.0,
        y=45.0,
        width=400.0,
        height=160.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("train_button_3.png"))
    uploadBadBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: uploadDataFiles(0),
        relief="flat"
    )
    uploadBadBtn.place(
        x=528.0,
        y=45.0,
        width=400.0,
        height=160.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("train_button_4.png"))
    startTrainBtn = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=trainModel,
        relief="flat"
    )
    startTrainBtn.place(
        x=605.0,
        y=393.0,
        width=323.0,
        height=103.0
    )
    window.mainloop()

# Screen shown when training the model
def trainModel():
    global trainingText
    
    for i in window.winfo_children():
        i.destroy()
    canvas = Canvas(
    window,
    bg = "#D6F0F3",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    trainingText=tk.StringVar()
    
    trainingText.set("Analyzing successful files:")
    sys.stdout.write=redirector
    tk.Message(window,textvariable=trainingText,bg="#D6F0F3",font=("Inter", 20 * -1),width=900).place(x=20,y=20)
    trainMLP.train(goodFiles,badFiles,trainingText,window)
    
    sys.stdout.write=original
    for i in window.winfo_children():
        i.destroy()
    
    canvas = Canvas(
    window,
    bg = "#D6F0F3",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("done_button_1.png"))
    homeBtn = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=home,
        relief="flat"
    )
    homeBtn.place(
        x=317.0,
        y=343.0,
        width=326.0,
        height=105.0
    )

    canvas.create_text(
        357.0,
        94.0,
        anchor="nw",
        text="Completed",
        fill="#27672A",
        font=("Actor Regular", 64 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("done_image_1.png"))
    image_1 = canvas.create_image(
        324.0,
        139.0,
        image=image_image_1
    )
    window.mainloop()


# Allows users to upload files for training
def uploadDataFiles(type):
    global goodFiles
    global badFiles
    
    files=askopenfilenames(filetype=(("Audio","*.wav"),("Transcript",".txt")))
    filesMsgText=''
    for i,name in enumerate(files):
        if i<10:
            filesMsgText+=name+"\n"
        else:
            filesMsgText+=f"and {len(files)-10} more"
            break
    if type:
        global goodFiles
        global goodFilesMsg
        try:
            goodFilesMsg.destroy()
        except :
            pass
        goodFilesMsg=tk.Message(window,text=filesMsgText,bg="#D6F0F3",font=("Inter", 10 * -1),width=400).place(x=25,y=210)
        goodFiles=files

    else:
        global badFiles
        global badFilesMsg
        try:
            badFilesMsg.destroy()
        except :
            pass
        badFilesMsg=tk.Message(window,text=filesMsgText,bg="#D6F0F3",font=("Inter", 10 * -1),width=400).place(x=528,y=210)
        
        badFiles=files
    window.mainloop()

# Screen shown when users want to analyse a speech
def startAnalysis():
    if mixer.get_init():
        mixer.music.stop()
        mixer.quit()
    window.configure(bg = "#D5EFF3")

    for i in window.winfo_children():
        i.destroy()
    canvas = Canvas(
    window,
    bg = "#D5EFF3",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("evaluate_button_1.png"))
    homeBtn = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=home,
        relief="flat"
    )
    homeBtn.place(
        x=25.0,
        y=383.0,
        width=326.0,
        height=120.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("evaluate_button_2.png"))
    uploadBtn = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=upload,
        relief="flat"
    )
    uploadBtn.place(
        x=577.0,
        y=150.0,
        width=356.0,
        height=142.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("evaluate_button_3.png"))
    startRecBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=startRec,
        relief="flat"
    )
    startRecBtn.place(
        x=26.0,
        y=150.0,
        width=326.0,
        height=142.0
    )

    canvas.create_text(
        428.0,
        183.0,
        anchor="nw",
        text="OR",
        fill="#000000",
        font=("ABeeZee Regular", 48 * -1)
    )
    window.mainloop()

# Screen shown for users to upload audio file for analysis
def upload():
    for i in window.winfo_children():
        i.destroy()
    canvas = Canvas(
    window,
    bg = "#D6F0F3",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("upload_image_1.png"))
    image_1 = canvas.create_image(
        684.0,
        213.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        448.0,
        70.0,
        920.0,
        135.0,
        fill="#C4C4C4",
        outline="")

    canvas.create_text(
        465.0,
        83.0,
        anchor="nw",
        text="Uploaded recordings: ",
        fill="#000000",
        font=("Actor Regular", 40 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("upload_button_1.png"))
    chooseFileBtn = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=chooseFile,
        relief="flat"
    )
    chooseFileBtn.place(
        x=70.0,
        y=69.0,
        width=328.0,
        height=104.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("upload_button_2.png"))
    homeBtn = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=home,
        relief="flat"
    )
    homeBtn.place(
        x=70.0,
        y=385.0,
        width=326.0,
        height=120.0
    )
    button_image_3 = PhotoImage(
    file=relative_to_assets("upload_button_3.png"))
    nextBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=finishRec,
        relief="flat"
    )
    nextBtn.place(
        x=560.0,
        y=393.0,
        width=335.0,
        height=112.0
    )
    window.mainloop()

# Allows user to choose file to be analysed
def chooseFile():
    global fileMsg
    file_path = askopenfilename(filetypes=[('Audio',"*.wav")])
    
    if file_path is not None:
        shutil.copy2(file_path, resource_path('temp.wav'))
    
    try:
        fileMsg.destroy()
    except NameError:
        pass
    fileMsg=tk.Message(window,text=file_path,bg="#FFFFFF",font=("Inter", 24 * -1),width=450).place(x=448,y=150)

# Initializzation for recording
def recording():
    global q
    
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.filename is None:
        args.filename = resource_path('temp.wav')
    if os.path.exists(args.filename):
        os.remove(args.filename)
    
    # Make sure the file is opened before recording anything:
    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                            channels=args.channels, callback=callback):
            
            while True:
                global stopThread
                if stopThread:
                    file.close()
                    break
                file.write(q.get())

# Count the time passed since starting recording
def countTime():
    global elapsedTimeText
    startTime=time.time()
    while True:
        global stopTimeThread
        if stopTimeThread:
            break
        stopTime=time.time()
        elapsedTime=stopTime-startTime
        s=int(elapsedTime%60)
        m=int((elapsedTime//60)%60)
        h=int(elapsedTime//3600)
        
        
        elapsedTimeText.set(f"{h:02d}:{m:02d}:{s:02d}")

# Check when the recording playback has finished
def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            window.after(100, check_event)
            stopListen()
            pygame.event.clear()

    window.after(100, check_event)

# Start the recording
def startRec():
    global startRecBtn
    global myrecording
    global stopThread
    global elapsedTimeText
    global stopTimeThread
    stopTimeThread=False
    for i in window.winfo_children():
        i.destroy()
 
    stopThread=False
   
    recThread=threading.Thread(target=recording)
    recThread.start()
    
    button_image_1 = PhotoImage(
    file=relative_to_assets("stop_button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=stopRec,
        relief="flat"
    )
    button_1.place(
        x=69.0,
        y=134.0,
        width=411.0,
        height=113.0
    )
    elapsedTimeText=tk.StringVar()
    elapsedTimeText.set("00:00:00")
    tk.Label(window,text="Elapsed Time:",bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=600,y=134)
    tk.Label(window,textvariable=elapsedTimeText,bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=600,y=200)
    timeThread=threading.Thread(target=countTime)
    timeThread.start()
    window.mainloop()

# Stop the recording
def stopRec():
    global myrecording
    global parser
    global stopThread
   
    stopThread=True
    global stopTimeThread
    stopTimeThread=True
    finishRec()

# Screen shown when users have finished recording or uploaded an audio file to be analysed
def finishRec():
    global listenBtn
    
    for i in window.winfo_children():
        i.destroy()
    canvas = Canvas(
    window,
    bg = "#D6F0F3",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("finish_button_1.png"))
    predictBtn= Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=predict,
        relief="flat"
    )
    predictBtn.place(
        x=601.0,
        y=405.0,
        width=335.0,
        height=112.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("finish_button_2.png"))
    homeBtn = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=home,
        relief="flat"
    )
    homeBtn.place(
        x=49.0,
        y=397.0,
        width=326.0,
        height=120.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("finish_button_3.png"))
    listenBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=listen,
        relief="flat"
    )
    listenBtn.place(
        x=553.0,
        y=156.0,
        width=383.0,
        height=114.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("finish_button_4.png"))
    restartBtn = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=startAnalysis,
        relief="flat"
    )
    restartBtn.place(
        x=26.0,
        y=162.0,
        width=386.0,
        height=108.0
    )
    window.mainloop()

# Play the recorded/uploaded audio,change the listen button to stop button
def listen():
    global listenBtn
    global stopListenBtn
    listenBtn.destroy()
    mixer.init()
    pygame.mixer.music.set_endevent(MUSIC_END)
    mixer.music.load(resource_path('temp.wav')) #Loading Music File
    button_image_3 = PhotoImage(
        file=relative_to_assets("stop_button_1.png"))
    stopListenBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=stopListen,
        relief="flat"
    )
    stopListenBtn.place(
        x=553.0,
        y=156.0,
        
    )
    mixer.music.play()
    window.mainloop()

# Stop the playback of recording, change the stop button back to listen to recording button
def stopListen():
    global listenBtn
    global stopListenBtn
    stopListenBtn.destroy()
    if mixer.get_init():
        mixer.music.stop()
        mixer.quit()
    button_image_3 = PhotoImage(
        file=relative_to_assets("finish_button_3.png"))
    listenBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=listen,
        relief="flat"
    )
    listenBtn.place(
        x=553.0,
        y=156.0,
        width=383.0,
        height=114.0
    )
    window.mainloop()
    
# Analyse the recording and predict customers' purchasing decision
def predict():
    if mixer.get_init():
        mixer.music.stop()
        mixer.quit()
    for i in window.winfo_children():
        i.destroy()
    window.update()
    loadingModelText=tk.StringVar()
    loadingModelText.set("Loading Model:...")
    
    tk.Label(window,textvariable=loadingModelText,bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=20,y=20)
    window.update()
    drive.download("model.joblib")

    if os.path.exists(resource_path("model.joblib")):
        
        model=joblib.load(resource_path("model.joblib"))
        loadingModelText.set("Loading Model: Completed")
        analyzingText=tk.StringVar()
        analyzingText.set("Analyzing performance:...")
        
        tk.Label(window,textvariable=analyzingText,bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=20,y=140)
        window.update()
        
        performance,sentences=analyze.analyzeSpeech(model,resource_path('temp.wav'))
        
        if performance=="error":
            analyzingText.set("Analyzing performance:Error")
            for i in window.winfo_children():
                i.destroy()
            canvas = Canvas(
                window,
                bg = "#D6F0F3",
                height = 540,
                width = 960,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )

            canvas.place(x = 0, y = 0)
            tk.Label(window,text="Error analyzing the audio,",bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=40,y=20)
            tk.Label(window,text="please try again",bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=40,y=140)
            
            button_image_1 = PhotoImage(
                file=relative_to_assets("good_button_1.png"))
            homeBtn = Button(
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=home,
                relief="flat"
            )
            homeBtn.place(
                x=575.0,
                y=341.0,
                width=326.0,
                height=105.0
            )

            button_image_2 = PhotoImage(
                file=relative_to_assets("good_button_2.png"))
            newRecBtn = Button(
                image=button_image_2,
                borderwidth=0,
                highlightthickness=0,
                command=startAnalysis,
                relief="flat"
            )
            newRecBtn.place(
                x=49.0,
                y=341.0,
                width=386.0,
                height=105.0
            )
            window.mainloop()

        else:
            analyzingText.set(f"Analyzing performance:Completed")
            for i in window.winfo_children():
                i.destroy()
            canvas = Canvas(
                window,
                bg = "#D6F0F3",
                height = 540,
                width = 960,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )

            canvas.place(x = 0, y = 0)
            button_image_1 = PhotoImage(
                file=relative_to_assets("good_button_1.png"))
            homeBtn = Button(
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=home,
                relief="flat"
            )
            homeBtn.place(
                x=575.0,
                y=341.0,
                width=326.0,
                height=105.0
            )

            button_image_2 = PhotoImage(
                file=relative_to_assets("good_button_2.png"))
            newRecBtn = Button(
                image=button_image_2,
                borderwidth=0,
                highlightthickness=0,
                command=startAnalysis,
                relief="flat"
            )
            newRecBtn.place(
                x=49.0,
                y=341.0,
                width=386.0,
                height=105.0
            )
            transcript="Transcript:\n"
            for sentence in sentences:
                transcript+=sentence+'.\n'
            txt = scrolledtext.ScrolledText(window, undo=True,height=8,width=90)
            txt['font'] = ('consolas', '12')
            txt.insert(tk.INSERT,transcript)
            txt.configure(state ='disabled')
            txt.place(x=49,y=160)
            if performance:

                image_image_1 = PhotoImage(
                    file=relative_to_assets("good_image_1.png"))
                image_1 = canvas.create_image(
                    365.0,
                    100.0,
                    image=image_image_1
                )

                canvas.create_text(
                    401.0,
                    100.0,
                    anchor="nw",
                    text="Successful",
                    fill="#27672A",
                    font=("Actor Regular", 48 * -1)
                )
            else:
                image_image_1 = PhotoImage(
                    file=relative_to_assets("bad_image_1.png"))
                image_1 = canvas.create_image(
                492.0,
                100.0,
                image=image_image_1
                )
            window.mainloop()
    else:
        for i in window.winfo_children():
                i.destroy()
        canvas = Canvas(
                window,
                bg = "#D6F0F3",
                height = 540,
                width = 960,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )

        canvas.place(x = 0, y = 0)
        tk.Label(window,text="Model cannot be loaded,",bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=40,y=20)
        tk.Label(window,text="please train a model before using it.",bg="#D6F0F3",font=("Inter", 48 * -1)).place(x=40,y=140)
        button_image_1 = PhotoImage(
                file=relative_to_assets("good_button_1.png"))
        homeBtn = Button(
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=home,
                relief="flat"
            )
        homeBtn.place(
                x=317.0,
                y=341.0,
                width=326.0,
                height=105.0
            )
        window.mainloop()

# Delete the AI model
def delModel():
    MsgBox = tk.messagebox.askquestion ('Delete Model','Are you sure you want to delete the model?',icon = 'warning')
    if MsgBox == 'yes':
       drive.delete('model.joblib')
       tk.messagebox.showinfo('Model Deleted','The model is deleted.')      

# Home screen shown when the app is initialized       
def home():
    if mixer.get_init():
        mixer.music.stop()
        mixer.quit()
    for i in window.winfo_children():
        i.destroy()
    canvas = Canvas(
        window,
        bg = "#EAFCFF",
        height = 540,
        width = 960,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("home_button_1.png"))
    analyzeBtn = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=startAnalysis,
        relief="flat"
    )
    analyzeBtn.place(
        x=25.0,
        y=209.0,
        width=397.3999938964844,
        height=150.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("home_button_2.png"))
    trainBtn = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=uploadData,
        relief="flat"
    )
    trainBtn.place(
        x=537.0,
        y=209.0,
        width=397.402587890625,
        height=150.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("home_button_3.png"))
    deleteBtn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=delModel,
        relief="flat"
    )
    deleteBtn.place(
        x=336.0,
        y=406.0,
        width=288.77923583984375,
        height=109.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("home_image_1.png"))
    image_1 = canvas.create_image(
        480.0,
        68.0,
        image=image_image_1
    )

    canvas.create_text(
        219.0,
        50.0,
        anchor="nw",
        text="AI Sales performance ",
        fill="#000000",
        font=("Inter", 48 * -1)
    )
    
    check_event()
    window.mainloop()

home()
