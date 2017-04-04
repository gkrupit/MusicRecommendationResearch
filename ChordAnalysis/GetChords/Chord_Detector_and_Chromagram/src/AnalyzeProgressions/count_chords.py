import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as pylab
import pandas as pd

chords = {
            '0' : 'C',
            '1m' : 'Dbm',
            '5' : 'F',
            '9m' : 'Am',
            '7' :  'G',
            '2m' : 'Dm',
            '4m' : 'Em',
            '2' : 'D',
            '10' : 'Bb',
            '11m' : 'Bm',
            '7m' : 'Gm',
            '6m' : 'Gbm',
            '5m' : 'Fm',
            '0m' : 'Cm',
            '9' : 'A'
         }

possible_chords = []
for i in range(12):
    possible_chords.append(str(i))
    possible_chords.append(str(i) + 'm')

def count_chords():
    progression_dir = '../chords/'
    progression_files = [ f for f in os.listdir(progression_dir) if f.endswith('.txt') ]

    chord_counts = dict()

    for filename in progression_files:
        lines = []
        with open(progression_dir + filename, 'rb') as f:
            lines = [ line.strip() for line in f.readlines() ]

        chords = lines[1:]
        chords = [ item.split() for item in chords ]
        chords = [ [ chord, int(count)] for [ chord, count ] in chords ]
        for chord, count in chords:
            try:
                chord_counts[chord] += count
            except KeyError:
                chord_counts[chord] = count

    return chord_counts

def song_contains():
    progression_dir = '../chords/'
    progression_files = [ f for f in os.listdir(progression_dir) if f.endswith('.txt') ]

    chord_counts = { chord : 0 for chord in possible_chords }


    num_songs = len(progression_files)
    for filename in progression_files:
        lines = []
        with open(progression_dir + filename, 'rb') as f:
            lines = [ line.strip() for line in f.readlines() ]

        chords = lines[1:]
        chords = { item.split()[0] for item in chords } # only keep set of chords
        for chord in chords:
            chord_counts[chord] += 1



    final_chord_counts = dict()
    for chord in chord_counts:
        if chord_counts[chord] > 10:
            final_chord_counts[chord] = int(round(1. * chord_counts[chord] /num_songs,2) * 100)


    return final_chord_counts






pylab.rcParams['font.size'] = 14
chord_counts = count_chords()
total_chords = sum(chord_counts.values())
chord_percentages = dict()
for chord, count in sorted(chord_counts.items(), key=lambda item: item[1], reverse=True):
    percentage = round(1. * chord_counts[chord] / total_chords, 2) * 100
    if percentage >= 2:
        chord_percentages[chord] = percentage






X = (map(lambda (c, p): chords[c], sorted(chord_percentages.items(), key=lambda item: item[1], reverse=True)))
y_pos = np.arange(len(X))
Y = []
for chord, percent in sorted(chord_percentages.items(), key=lambda item: item[1], reverse=True):
    Y.append(percent)

X.append('Other')
other_percent = 100 - sum(Y)
Y.append(other_percent)

N = len(Y)


ind = np.arange(N)  # the x locations for the groups
width = 0.6       # the width of the bars

fig, ax = plt.subplots()
rects = ax.bar(ind, Y, width, color='b')

#women_means = (25, 32, 34, 20, 25)
#women_std = (3, 5, 2, 3, 3)
#rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

# add some text for labels, title and axes ticks
ax.set_ylabel('% Used')
ax.set_title('Chords Found using Original Method for Songs in Study')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(X)
plt.ylim(0, 110)
ax.yaxis.set_visible(False)

#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

for rect in rects:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., height + 0.2,
            '%d%%' % int(height),
            ha='center', va='bottom')

#autolabel(rects2)

plt.show()










chord_freqs = song_contains()
for chord, freq in sorted(chord_freqs.items(), key=lambda item: item[1], reverse=True):
    print chord, ' : ',freq

X = (map(lambda (c, p): chords[c], sorted(chord_freqs.items(), key=lambda item: item[1], reverse=True)))
y_pos = np.arange(len(X))
Y = []
for chord, percent in sorted(chord_freqs.items(), key=lambda item: item[1], reverse=True):
    Y.append(percent)

N = len(Y)


ind = np.arange(N)  # the x locations for the groups
width = 0.6       # the width of the bars

fig, ax = plt.subplots()
rects = ax.bar(ind, Y, width, color='b')

#women_means = (25, 32, 34, 20, 25)
#women_std = (3, 5, 2, 3, 3)
#rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

# add some text for labels, title and axes ticks
ax.set_ylabel('% Used')
#ax.set_title('Chords Found using Original Method for Songs in Study')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(X)
plt.ylim(0, 110)
ax.yaxis.set_visible(False)

#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

for rect in rects:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2. + 0.1, height + 0.2,
            '%d%%' % int(height),
            ha='center', va='bottom')

#autolabel(rects2)

plt.show()
