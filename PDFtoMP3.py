from tkinter import Tk
from tkinter.filedialog import askopenfilename
import PyPDF2
from gtts import gTTS
from os.path import splitext

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
fileLocation = askopenfilename()  # open the dialog GUI

file = open(fileLocation, 'rb')
reader = PyPDF2.PdfFileReader(file)
string = ""
totalPages = reader.numPages

for i in range(0,totalPages):
    page = reader.getPage(i)
    text = page.extractText()
    string += text

final_file = gTTS(text=string, lang='en')
outName = splitext(fileLocation)[0] + '.mp3'
final_file.save(outName)