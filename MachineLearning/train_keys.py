from sklearn import datasets
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier

from sklearn.svm import LinearSVC
import os
import numpy as np

keys = [
         'C',
         'Cm',
         'Db',
         'Dbm',
         'D',
         'Dm',
         'Eb',
         'Ebm',
         'E',
         'Em',
         'F',
         'Fm',
         'F#',
         'F#m',
         'G',
         'Gm',
         'Ab',
         'Abm',
         'A',
         'Am',
         'Bb',
         'Bbm',
         'B',
         'Bm'
       ]

print len(keys)
training_histograms = '../ChordAnalysis/GetChords/Chord_Detector_and_Chromagram/src/ChordHistograms/'
histograms_to_predict = '../ChordAnalysis/GetChords/Chord_Detector_and_Chromagram/src/ChordHistogramsToDetermine/'

chords = []
for i in range(12):
    chords.append(str(i))
    chords.append(str(i) + 'm')

chord2val = {}
for i, chord in enumerate(chords):
    chord2val[chord] = i

class KnownSong:
    def __init__(self, filename):
        self.name = filename
        with open(training_histograms + filename) as f:
            lines = [ line.strip() for line in f.readlines() ]
            self.key = lines[0]
            self.distribution = lines[1 : ]
            self.frequencies = dict()
            for i, data in enumerate(self.distribution):
                data = data.split(',')
                self.frequencies[data[0]] = data[2]

        self.all_frequencies = []
        for chord in chords:
            frequency = 0
            try:
                frequency = float(self.frequencies[chord])
            except KeyError:
                pass

            self.all_frequencies.append(frequency)

        self.all_frequencies = np.array(self.all_frequencies)

    def Frequencies(self):
        return self.all_frequencies

    def Key(self):
        return self.key


    def Print(self):
        print 'Filename:', self.name
        print 'Key:', self.key
        print 'Frequencies:'
        for i, chord in enumerate(chords):
            print chord, self.all_frequencies[i]

class UnknownSong:
    def __init__(self, filename):
        self.name = filename
        with open(histograms_to_predict + filename) as f:
            lines = [ line.strip() for line in f.readlines() ]
            self.key = -1
            self.distribution = lines[1 : ]
            self.frequencies = dict()
            for i, data in enumerate(self.distribution):
                data = data.split(',')
                self.frequencies[data[0]] = data[2]

        self.all_frequencies = []
        for chord in chords:
            frequency = 0
            try:
                frequency = float(self.frequencies[chord])
            except KeyError:
                pass

            self.all_frequencies.append(frequency)

        self.all_frequencies = np.array(self.all_frequencies)

    def Frequencies(self):
        return self.all_frequencies

    def Key(self):
        return self.key

    def SetKey(self, new_key):
        self.key = new_key

    def Print(self):
        print 'Filename:', self.name
        print 'Key:', self.key
        print 'Frequencies:'
        for i, chord in enumerate(chords):
            print chord, self.all_frequencies[i]

    def __str__(self):
        return self.name



known_songs = []
for file in os.listdir(training_histograms):
    if file != '.DS_Store':
        song = KnownSong(file)
        known_songs.append(song)

songs_to_predict = []
for file in os.listdir(histograms_to_predict):
    if file != '.DS_Store':
        song = UnknownSong(file)
        songs_to_predict.append(song)


X = []
y = []
for song in known_songs:
    X.append(song.Frequencies())
    y.append(song.Key())

X = np.array(X)
y = np.array(y)
#for c in range(24):
#    print y.count(str(c))
classifier_2 = OneVsOneClassifier(LinearSVC(random_state=0))
classifier = OneVsRestClassifier(LinearSVC(random_state=0))
classifier.fit(X,y)
classifier_2.fit(X,y)


histograms_to_predict = [ song.Frequencies() for songs in songs_to_predict ]
predictions = classifier.predict(histograms_to_predict)

predicted_keys = zip(songs_to_predict, predictions)
#for prediction in predicted_keys:
#    print '%s: %s' % (prediction[0], prediction[1])

for song in songs_to_predict:
    key_value = classifier.predict([song.Frequencies()])
    key_value = int(key_value[0])
    print song,keys[key_value]
