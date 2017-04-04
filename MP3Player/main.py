from Player import MP3Player
import os
import csv
import sys

MP3_directory = '../../AllMusic/'
distance_file = '../sub_length5.csv'
mode = sys.argv[1]
trial_length = 10#int(sys.argv[2])

def GetSongOrders(distance_file):
    orders = dict()
    with open(distance_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        song_list = next(reader)[1:] #remove first elem, which is empty
        for row in reader:
            song = row[0] #get parent song for ordering
            distances = zip(song_list, row[1:]) #pair each song with distance from parent song
            song_order = sorted(distances, key=lambda pair: pair[1]) #sort by distances to parent
            orders[song] = song_order

    return orders

def AbsoluteSongPaths(dir):
    mp3_list = os.listdir(MP3_directory) #Get all song names
    mp3_list = [ file for file in mp3_list if file.endswith('.mp3') ] # only keep mp3's from directory
    return mp3_list

def main():
    song_list = AbsoluteSongPaths(MP3_directory)
    song_orders = GetSongOrders(distance_file)
    player = MP3Player(MP3_directory, song_orders, mode, trial_length)
    if player == None:
        return
    print '\n\n\n'
    #player.PrintPlayHistory()
    if player.FinishedSuccessfully():
        player.WriteResults()
    else:
        print 'Trial not successful Exiting.'

main()
print 'Exiting program.'
