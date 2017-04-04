from Tkinter import *

from threading import Thread
import pyglet
import os

MP3_directory = '../MusicRecommendation/ChordAnalysis/GetChords/Chord_Detector_and_Chromagram/src/Music/'

mp3_list = os.listdir(MP3_directory)
mp3_list = [ MP3_directory + file for file in mp3_list if file.endswith('.mp3') ]

root = Tk()
app = Frame(root)
app.pack(side='bottom')

player = pyglet.media.Player()
print 'About to load song', mp3_list[0]
#music_file = pyglet.media.load(mp3_list[0])

current_song_index = 0

def play_song(mp3):
    print 'About to play', mp3
    player.queue(mp3)
    player.play()


def startPlaying():
    print 'In startPlaying'
    current_song_index = 0
    current_song = mp3_list[current_song_index]
    music_file = pyglet.media.load(current_song)
    #play_song(music_file)

def nextSong():
    current_song_index += 1
    current_song = mp3_list[current_song_index]
    #music_file = pyglet.media.load(current_song)
    play_song(music_file)

def playFirst():
    global sound_thread
    sound_thread = Thread(target=startPlaying)
    sound_thread.start()

def playNextSong():
    global sound_thread
    sound_thread = Thread(target=nextSong)
    soung_thread.start()

start_playing = Button(app, text="Enter Program", command=playFirst)
#next_song = Button(app, text="Next song please!", command=playNextSong)
start_playing.pack()

root.mainloop()
pyglet.app.exit()
