from Player import MP3Player
import os
import csv
import sys
import numpy as np

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

def IndicesForSong(song_orders, to_find):
    indices = {}
    for song_list in song_orders.values():
        song_order = [ song for (song, distance) in song_list ]
        index = song_order.index(to_find)
        if index not in indices:
            indices[index] = 1
        else:
            indices[index] += 1
    return indices


def EvaluateOrders(song_orders):
    for song_to_find in ['10-million-years',
                         'Farther-along-love-war-the-sea-in-between-2011',
                         'Dont-wait-for-me-jacaranda-2008']:
        indices = IndicesForSong(song_orders, song_to_find)
        print song_to_find
        for index, count in sorted(indices.items(), key=lambda (i,c): c, reverse=True)[:5]:
            print '  %d: %d times' % (index, count)

def main():
    song_list = AbsoluteSongPaths(MP3_directory)
    song_orders = GetSongOrders(distance_file)
    for song in sorted(song_orders):
        print song

    last_index = len(song_orders) - 1
    score = lambda r: np.exp(-1.*r/4)
    min_score = score(10.)
    max_score = score(1)
    next_index = lambda r: int(last_index * (score(r) - min_score) / (max_score - min_score))


    for r in range(1,10+1):
        print '%d: %d' % (r,next_index(r))



    player = MP3Player(MP3_directory, song_orders, mode, trial_length)
    # min_score = player.GetScore(1.)
    # for r in range(1,10+1):
    #     next_index =
    #     print '%d: %.2f' % (r,player.GetScore(r))

    EvaluateOrders(song_orders)

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
