from tkinter import *
import pygame
from tkinter import filedialog, ttk
import time
from mutagen.mp3 import MP3

root = Tk();
root.title('PDF Audio Player')
root.geometry("560x400")

# Initialise Pygame Mixer
pygame.mixer.init()

# Add One or More PDF(s) Function
def addPDF():
    PDFs = filedialog.askopenfilenames(title="Choose PDF(s)", filetypes=(("PDF Files", "*.PDF"),))
    
    # Loop through PDFs and replace Directory info and PDF
    for PDF in PDFs:
        PDF = PDF.replace('C:/Users/kusha/Downloads/', '')
        PDF = PDF.replace(".pdf", '')
        # Insert Into Playlist
        audioBookBox.insert(END, PDF)

# AudiBook Length Function
def playtime():
    # Checking For Double Timing
    if(stopped):
        return

    # Current Audio Book Elapsed Time
    currTime = pygame.mixer.music.get_pos() // 1000 # Divide by 1000 to get the time in seconds

    # Temporary Label to get data
    # sliderLabel.config(text=f'Slider: {int(audioSlider.get())+1} and Song Pos: {int(currTime)+1}')

    # Convert to time format(HH:MM:SS)
    converted_currTime = time.strftime('%H:%M:%S', time.gmtime(currTime))

    # Get Currently Playing Audio Book
    audio = audioBookBox.get(ACTIVE)  # returns only the title of the Currently Selected PDF
    audio = f'C:/Users/kusha/Downloads/{audio}.mp3'  # re-Build the directory

    # Load Audio Book with Mutagen
    loadAudio = MP3(audio)
    # Get Audio Book Length
    global audioLen
    audioLen = loadAudio.info.length

    # Convert to time format(HH:MM:SS)
    converted_audioLen = time.strftime('%H:%M:%S', time.gmtime(audioLen))

    # Increase Curr Time by 1 sec to remove latency
    currTime += 1

    if(int(audioSlider.get()) == int(audioLen)):
        statusBar.config(text=f'Time Elapsed: {converted_audioLen}  of  {converted_audioLen}')
    elif(paused):
        pass
    elif(int(audioSlider.get()) == currTime):
        # Slider Hasn't been Moved
        # Update Slider To position
        sliderPos = int(audioLen)
        audioSlider.config(to=sliderPos, value=currTime)
    else:
        # Slider Has been Moved
        # Update Slider To position
        sliderPos = int(audioLen)
        audioSlider.config(to=sliderPos, value=int(audioSlider.get()))

        # Convert to time format(HH:MM:SS)
        converted_currTime = time.strftime('%H:%M:%S', time.gmtime(int(audioSlider.get()) + 1))

        # Output Time To Status Bar
        statusBar.config(text=f'Time Elapsed: {converted_currTime}  of  {converted_audioLen}')

        # Move Slider by one second
        nextSec = int(audioSlider.get()) + 1
        audioSlider.config(value=nextSec)

    # # Output Time To Status Bar
    # statusBar.config(text=f'Time Elapsed: {converted_currTime}  of  {converted_audioLen}')

    # Update Slider Position to Current Audio Position...
    # audioSlider.config(value=currTime)

    # For Updating time After Every Second
    statusBar.after(1000, playtime)

# Remove One PDF Function
def removePDF():
    stop()
    audioBookBox.delete(ACTIVE) # Delete Currently Selected Song
    pygame.mixer.music.stop() # Stop Audio If It's Playing

# Remove All PDFs Function
def removeAllPDFs():
    stop()
    audioBookBox.delete(0, END)
    pygame.mixer.music.stop() # Stop Audio If It's Playing

# Backward Button Function
def prevAudioBook():
    # Reset Slider And Status bar
    statusBar.config(text='')
    audioSlider.config(value=0)

    # Get The current Audio Book Tuple Number
    curr_AudioBook = audioBookBox.curselection()

    # Subtract one to the current song number
    prev_AudioBook = curr_AudioBook[0] - 1

    # Grab Previous Audio Book title From Playlist and Play it
    audio = audioBookBox.get(prev_AudioBook)  # returns only the title of the PDF
    audio = f'C:/Users/kusha/Downloads/{audio}.mp3'  # re-Build the directory
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play(loops=0)

    # Clear Active Bar For the Current Audio Book
    audioBookBox.selection_clear(0, END)

    # Move Underline to Previous Audio Book
    audioBookBox.activate(prev_AudioBook)

    # Set Active Bar To Previous Audio Book
    audioBookBox.selection_set(prev_AudioBook, last=None)

# Forward Button Function
def nextAudioBook():
    # Reset Slider And Status bar
    statusBar.config(text='')
    audioSlider.config(value=0)

    # Get The current Audio Book Tuple Number
    curr_AudioBook = audioBookBox.curselection()

    # Add one to the current song number
    next_AudioBook = curr_AudioBook[0] + 1

    # Grab Next Audio Book title From Playlist and Play it
    audio = audioBookBox.get(next_AudioBook) # returns only the title of the PDF
    audio = f'C:/Users/kusha/Downloads/{audio}.mp3' # re-Build the directory
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play(loops=0)

    # Clear Active Bar For the Current Audio Book
    audioBookBox.selection_clear(0, END)

    # Move Underline to Next Audio Book
    audioBookBox.activate(next_AudioBook)

    # Set Active Bar To Next Audio Book
    audioBookBox.selection_set(next_AudioBook, last=None)

# Play Selected PDF (Function)
def play():
    global stopped
    stopped = False
    audio = audioBookBox.get(ACTIVE) # returns only the title of the PDF
    audio = f'C:/Users/kusha/Downloads/{audio}.mp3' # re-Build the directory

    pygame.mixer.music.load(audio)
    pygame.mixer.music.play(loops=0)

    # Call the Play time Function to Get The Length Of The Audio Book
    playtime()

    # Get the Current Volume
    currVolume = pygame.mixer.music.get_volume()
    currVolume *= 100  # Multiply By 100 So that it's easier to work with

    # Change Volume Meter Picture
    if (int(currVolume) < 1):
        volumeMeter.config(image=vol0)
    elif (int(currVolume) > 0 and int(currVolume) <= 25):
        volumeMeter.config(image=vol1)
    elif (int(currVolume) >= 25 and int(currVolume) <= 50):
        volumeMeter.config(image=vol2)
    elif (int(currVolume) >= 50 and int(currVolume) <= 75):
        volumeMeter.config(image=vol3)
    elif (int(currVolume) >= 75 and int(currVolume) <= 100):
        volumeMeter.config(image=vol4)

# Create Global Pause Variable
global paused
paused = False

# Pause and unpause Selected PDF (Function)
def pause(isPaused):
    global paused
    paused = isPaused

    if(paused):
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Stop Selected PDF (Function)
global stopped
stopped = False
def stop():
    # Reset Slider And Status bar
    statusBar.config(text='')
    audioSlider.config(value=0)

    #Stop Song From Playing
    pygame.mixer.music.stop()
    audioBookBox.selection_clear(ACTIVE)

    # Clear The Status Bar
    statusBar.config(text='')

    # Set Stop Variable to True
    global stopped
    stopped = True

    volumeMeter.config(image=vol0)

# Create Audio Slider Function
def audioSlide(x):
    audio = audioBookBox.get(ACTIVE)  # returns only the title of the PDF
    audio = f'C:/Users/kusha/Downloads/{audio}.mp3'  # re-Build the directory

    pygame.mixer.music.load(audio)
    pygame.mixer.music.play(loops=0, start=int(audioSlider.get()))

# Create Volume Slider Function
def volumeSlide(x):
    pygame.mixer.music.set_volume(volumeSlider.get())

    # Get the Current Volume
    currVolume = pygame.mixer.music.get_volume()
    currVolume *= 100 #Multiply By 100 So that it's easier to work with

    # Change Volume Meter Picture
    if(int(currVolume) < 1):
        volumeMeter.config(image=vol0)
    elif(int(currVolume) > 0 and int(currVolume) <=25):
        volumeMeter.config(image=vol1)
    elif (int(currVolume) >= 25 and int(currVolume) <= 50):
        volumeMeter.config(image=vol2)
    elif (int(currVolume) >= 50 and int(currVolume) <= 75):
        volumeMeter.config(image=vol3)
    elif (int(currVolume) >= 75 and int(currVolume) <= 100):
        volumeMeter.config(image=vol4)

# Create Master Frame
masterFrame = Frame(root)
masterFrame.pack(pady=20)

# Create Volume Label Frame
volumeFrame = LabelFrame(masterFrame, text='Volume')
volumeFrame.grid(row=0, column=1, padx=30)

# Create Playlist Box
audioBookBox = Listbox(masterFrame, bg="black", fg="gray", width = 70, selectbackground="gray", selectforeground="black")
audioBookBox.grid(row=0, column=0)

# Define Player Control Button Images
backBtnImg = PhotoImage(file='Project Pics/back50.png')
forwardBtnImg = PhotoImage(file='Project Pics/forward50.png')
playBtnImg = PhotoImage(file='Project Pics/play50.png')
pauseBtnImg = PhotoImage(file='Project Pics/pause50.png')
stopBtnImg = PhotoImage(file='Project Pics/stop50.png')

# Define Volume Control Images
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file='Project Pics/volume0.png')
vol1 = PhotoImage(file='Project Pics/volume1.png')
vol2 = PhotoImage(file='Project Pics/volume2.png')
vol3 = PhotoImage(file='Project Pics/volume3.png')
vol4 = PhotoImage(file='Project Pics/volume4.png')

# Create Player Control Frame
controlsFrame = Frame(masterFrame)
controlsFrame.grid(row=1, column=0, pady=20)

# Create Volume Meter Frame
volumeMeter = Label(masterFrame, image=vol0)
volumeMeter.grid(row=1, column=1, padx=10)

# Create Player Control Buttons
backBtn = Button(controlsFrame, image=backBtnImg, borderwidth=0, command=prevAudioBook)
forwardBtn = Button(controlsFrame, image=forwardBtnImg, borderwidth=0, command=nextAudioBook)
playBtn = Button(controlsFrame, image=playBtnImg, borderwidth=0, command=play)
pauseBtn = Button(controlsFrame, image=pauseBtnImg, borderwidth=0, command=lambda: pause(paused))
stopBtn = Button(controlsFrame, image=stopBtnImg, borderwidth=0, command=stop)

backBtn.grid(row=0, column=0, padx=10)
forwardBtn.grid(row=0, column=1, padx=10)
playBtn.grid(row=0, column=2, padx=10)
pauseBtn.grid(row=0, column=3, padx=10)
stopBtn.grid(row=0, column=4, padx=10)

# Create Menu
myMenu = Menu(root)
root.config(menu=myMenu)

# Add the PDFs in the menu
addPDFMenu = Menu(myMenu)
myMenu.add_cascade(label="Add PDF", menu=addPDFMenu)
# Add one or more PDFs to the Playlist
addPDFMenu.add_command(label="Add PDF(s)", command=addPDF)

# Create Delete PDF Menu
removePDFMenu = Menu(myMenu)
myMenu.add_cascade(label="Remove PDF", menu=removePDFMenu)
# Delete one or more PDFs from the Playlist
removePDFMenu.add_command(label="Remove PDF", command=removePDF)
# Delete all PDFs From the Playlist
removePDFMenu.add_command(label="Remove All PDFs", command=removeAllPDFs)

# Create Status Bar
statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Audio Book Position Slider
audioSlider = ttk.Scale(masterFrame, from_=0, to=100, orient=HORIZONTAL, value=0, command=audioSlide, length=360)
audioSlider.grid(row=2, column=0, pady=20)

# Create Volume Slider
volumeSlider = ttk.Scale(volumeFrame, from_=1, to=0, orient=VERTICAL, value=1, command=volumeSlide, length=125)
volumeSlider.pack(pady=10)

# Create Temporary Slider Label
# sliderLabel = Label(root, text="0")
# sliderLabel.pack(pady=10)

root.mainloop()