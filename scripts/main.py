import ocrhandler
import mousehandler
import VoiceInput
import textparser
import thread
import webhandler
import applicationhandler
import threading
import keyboardhandler
import pyautogui

audioQueue = []
textQueue = []
commandQueue=[]


def GetContinuousText(audio):
    textQueue.append(VoiceInput.GetText(audio).lower())


def RunCommand(com):
    c = com[0]
    v = com[1]

    if c == "search":
        webhandler.GoogleSearch(v)
    elif c == "url":
        webhandler.OpenURL(v)
    elif c == "app":
        applicationhandler.OpenApp(v)
    elif c == "mouseMove":
        filename = ".screenshot.png"
        img = ocrhandler.GetScreenShot(filename)
        s= ocrhandler.LocateText(img,v,filename)

        if s:
            mousehandler.Move(s[0][0], s[0][1])
        else:
            print "\nNOT FOUND\n"

    elif c == "mouseClick":
        mousehandler.Click()
    elif c == "mouseDoubleClick":
        mousehandler.DoubleClick()
    elif c == "mouseScroll":
        t = 1
        if v == "up":
            t = -1
        mousehandler.Scroll(t)
    elif c == "keyboardType":
        keyboardhandler.TypeText(v)
    elif c == "keyboardHold":
        keyboardhandler.HoldKey(v)
    elif c == "keyboardRelease":
        keyboardhandler.ReleaseKey(v)



        
def GetTextHelper():
    if audioQueue:
        textQueue.append(VoiceInput.GetText(audioQueue.pop(0)).lower())
    return

    
def GetAudioThread():
    while True:
        audioQueue.append(VoiceInput.GetVoice())

    
def GetTextThread():
    #while True:
    #    if audioQueue:
    #        textQueue.append(VoiceInput.GetText(audioQueue.pop(0)).lower())
    while True:
        if audioQueue:
            threading.Thread(target=GetTextHelper)
    
    
def GetCommandThread():
    while True:
        if textQueue:
            com = textparser.GetCommand(textQueue.pop(0))
            if len(com)>0:
                commandQueue.append(com)
                
def RunCommandThread():
    while True:
        if commandQueue:
            RunCommand(commandQueue.pop(0))
def main():
    
    a = threading.Thread(target=GetAudioThread)
    b = threading.Thread(target=GetTextThread)
    c = threading.Thread(target=GetCommandThread)
    d = threading.Thread(target=RunCommandThread)
    
    a.start()
    b.start()
    c.start()
    d.start()
    
    
    


if __name__ == "__main__":
    main()
