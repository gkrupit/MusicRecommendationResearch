#ReadProgressions and do pairwise comparisons
import os
import compare
import sys
import time

progression_directory = '../chords/'
comparison_directory = 'comparisons/'
subLength = 5#int(sys.argv[1])

songs = [ f for f in os.listdir(progression_directory) if f.endswith('.txt') ]

song_names = [ song.replace('.txt','') for song in songs ]

def CompareSongs(subLength):
    comparisons = dict()

    for song1 in songs:
        song1name = song1.replace('.txt','')
        song1 = progression_directory + song1
        for song2 in songs:
            song2name = song2.replace('.txt', '')
            print 'Comparing:', song1name, song2name
            #print '--------------------', song1name, song2name
            song2 = progression_directory + song2
            if song1 == song2:
                comparisons[(song1name,song2name)] = 0 #song has distance 0 to itself
                continue
            comparisons[(song1name,song2name)] = compare.CompareSongs(song1, song2, subLength)

    comparison_file = '%ssub_length%d.csv' % (comparison_directory,subLength)
    with open(comparison_file, 'w') as f:
        f.write(',')
        for song in song_names:
            f.write(song + ',')
        f.write('\n')
        for song1 in song_names:
            print 'Writing comparisons for', song1
            out = song1
            for song2 in song_names:
                out += ',' + str(comparisons[(song1,song2)])
                print '  ',song2
            f.write(out + '\n')

    return comparisons


def PrintAll(all_comparisons):
    print 'Printing pairwise distances'
    for i,song1 in enumerate(song_names):
        for song2 in song_names[i+1:]:
            for subLength in sorted(all_comparisons):
                try:
                    song_pair = (song1,song2)
                    prev = all_comparisons[subLength - 1][song_pair]
                    current = all_comparisons[subLength][song_pair]
                    if prev != 0 and current != 0:
                        print '(%s,%s),%d : %f' % (song1,song2,subLength,round(current/prev,3))
                except KeyError:
                    continue

def GenerateLists(all_comparisons,distance):
    print 'Generating distances for each song'
    distances = all_comparisons[distance]
    song_orders = dict()
    for song1 in song_names:
        song1order = []
        for song2 in song_names:
            song_pair = (song1,song2)
            song1order.append((song2,distances[song_pair]))
        song1order = sorted(song1order, key=lambda elem: elem[1]) #sort by distance of song
        song_orders[song1] = song1order
    return song_orders

def main():
    all_comparisons = dict()
    all_comparisons[subLength] = CompareSongs(subLength)
    PrintAll(all_comparisons)
    orders = GenerateLists(all_comparisons,subLength)
    print 'Generated playlist order for each song in order of distance:'
    for song in orders:
        print 'Song:',song
        for i,song2 in enumerate(orders[song]):
            print '  %d. %s, %f' % (i,song2[0], song2[1])


main()
print 'Ending program...'
