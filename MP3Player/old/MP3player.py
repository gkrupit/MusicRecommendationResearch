#!/usr/bin/python
import random
import os
import signal
import subprocess
import time
from termios import tcflush, TCIFLUSH
import sys

from Tkinter import *

root = Tk()
app = Frame(root)
app.pack(side='bottom')

def PlayFirst():
    print 'Play first song'

def NextSong():
    print 'Playing next song'

start_playing = Button(app, text="Enter Program", command=PlayFirst)
next_song = Button(app, text="Next song please!", command=NextSong)
start_playing.pack()
next_song.pack()

def absoluteFilePaths(directory):
    return_list = []

    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            if f.endswith((".mp3")):
                FullFileName = os.path.abspath(os.path.join(dirpath, f))
                print FullFileName
                return_list.append(FullFileName.replace(" ","\ "))

    return return_list

folder_location = '../../AllMusic/'
file_list = absoluteFilePaths(folder_location)
wordlen=len(file_list)
os.system('modprobe snd_bcm2835')
os.system('amixer cset numid=3 1')
while True:
    print "------------------------------------"
    i=random.randint(0, wordlen-1)
    print i
    with open('out.txt', 'w') as out:
        proc = subprocess.Popen('mpg321 '+file_list[i], shell=True, preexec_fn=os.setsid, stdout=out)
    #proc = subprocess.call('mpg321 '+file_list[i], shell=True)
    start = time.time()
    print 'Wait 10 seconds before you can skip...'
    while 1:
        if time.time() - start > 10:
            break
    tcflush(sys.stdin, TCIFLUSH)
    s = raw_input('Hit Enter to skip song... ')
    end = time.time()
    print 'Time played:', end - start, 'seconds'
    if s == 'exit':
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        break



    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
