'''
Based on player from
http://stackoverflow.com/questions/26564449/playing-mp3-files-using-python-2-7-buttons-tkinter
'''

from Tkinter import *

from threading import Thread
import pyglet
import sys
import os
import csv
import random

MP3_directory = '../MusicRecommendation/ChordAnalysis/GetChords/Chord_Detector_and_Chromagram/src/AllMusic/'
mp3_list = os.listdir(MP3_directory)
mp3_list = [ MP3_directory + file for file in mp3_list if file.endswith('.mp3') ]

root = Tk()
app = Frame(root)
app.pack(side='bottom')

player = pyglet.media.Player()
current_song_index = 0

def GetSongOrders():
    orders = dict()
    with open('sub_length3.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        song_list = next(reader)[1:] #remove first elem, which is empty
        for row in reader:
            song = row[0] #get parent song for ordering
            distances = zip(song_list, row[1:]) #pair each song with distance from parent song
            song_order = sorted(distances, key=lambda pair: pair[1]) #sort by distances to parent
            orders[song] = song_order

    return orders




def startPlaying():
    #print 'In startPlaying'
    #global current_song_index
    #current_song_index = 0

    #current_song = MP3_directory + playlist[current_song_index][0]
    #print 'Playing song', current_song, 'Distances:',
    #music_file = pyglet.media.load(current_song)
    #player.queue(music_file)
    player.play()

def init_playlist():
    global orders
    orders = GetSongOrders()
    #print orders

    playlist = random.choice(orders.values())
    songs = [ MP3_directory + song[0] + '.mp3' for song in playlist]
    worked = []
    didnt_work = []
    for song in [song[0] for song in playlist]:
        #if song[0].isalpha():
            song = song[0].upper() + song[1:]
            song = MP3_directory + song + '.mp3'
            #print 'Adding following file to playlist:',song
            try:
                music_file = pyglet.resource.media(song)
            except fpectl.FloatingPointError:
                didnt_work.append(song)

            player.queue(music_file)

'''
    print 'Playlist:'
    for song in songs:
        print song
'''



def nextSong():
    pass

def playFirst():
    global sound_thread
    sound_thread = Thread(target=player.play)
    sound_thread.start()

def playNextSong():
    global sound_thread
    sound_thread = Thread(target=player.next)
    sound_thread.start()

start_playing = Button(app, text="Enter Program", command=playFirst)
next_song = Button(app, text="Next song please!", command=playNextSong)
start_playing.pack()
next_song.pack()

init_playlist()

root.mainloop()
pyglet.app.exit()
