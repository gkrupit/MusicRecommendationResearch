from Chromagram import Chromagram
from ChordDetector import ChordDetector

import subprocess
from pydub import AudioSegment
import sys
import scipy.io.wavfile
import numpy as np
import threading

class ChordFinderThread(threading.Thread):
    def __init__(self, skip):
        threading.Thread.__init__(self)
        self.skip = skip
    def run(self):
        print "Starting thread %d" % self.skip
        ThreadFunction(self.skip)
        print "Exiting thread %d" % self.skip

FRAMES_PER_BUFFER = 4096

freq2note = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def PrintChroma(chromagram):
    for freq, intensity in enumerate(chromagram):
        print "%s: %d" % (freq2note[freq], intensity)

input_mp3 = sys.argv[1]
input_wav = input_mp3[0:len(input_mp3) - 4] + ".wav"
song_mp3 = AudioSegment.from_mp3(input_mp3)
song_mp3.export(input_wav, format='wav')

samplerate, data = scipy.io.wavfile.read(input_wav)

left, right = data[0::2], data[1::2]



'''
Each thread handles a different (mod num_frames)
OR
Need a concurrent list that each thread appends to
and
need a concurrent list to store samples
to ensure that chords stay in consistent order as samples
'''

num_threads = 100
num_samples = len(left) #- FRAMES_PER_BUFFER
frame_count = num_samples / FRAMES_PER_BUFFER
print 'Number of frames to analyze: %d' % frame_count
chords = []
for i in range(num_threads):
    chords.append([])

def ThreadFunction(skip):
    chromagram = Chromagram(FRAMES_PER_BUFFER,samplerate)
    for frame in range(skip, frame_count, num_threads):
        print "Frame Number: %d" % frame
        start_sample = frame * FRAMES_PER_BUFFER
        end_sample = start_sample + FRAMES_PER_BUFFER
        segment = left.tolist()[start_sample : end_sample]
        segment = [item[0] for item in segment]
        print "Segement: [%d, %d]" % (start_sample, end_sample)
        chromagram.processAudioFrame(segment)

        if chromagram.isReady():
            #print "Printing chromagram for samples [%d,%d]" % (start_sample, end_sample)
            chroma = chromagram.getChromagram()
            PrintChroma(chroma)
            #print "Not ready in a row previous: %d" % not_ready_count
            #print "Frame Number: %d" % frame
            print "\n"
            #not_ready_count = 0
            chord_detector = ChordDetector()
            chord_detector.detectChord(chroma)
            print "Chord root: %s" % freq2note[chord_detector.rootNote]
            chords[skip].append(freq2note[chord_detector.rootNote])
        else:
            print "Chromagram was not ready"
            chords[skip].append('null')
            #not_ready_count += 1


threads = []
for skip in range(num_threads):
    threads.append(ChordFinderThread(skip))
    threads[skip].start()


chords = [chord for chord_list in chords for chord in chord_list]

for frame, chord in enumerate(chords):
    print 'Frame: %d. Chord: %s' %(frame, 'not found' if chord == 'not found' else chord)

'''
not_ready_count = 0
for frame in range(frame_count):
    start_sample = frame * FRAMES_PER_BUFFER
    end_sample = start_sample + FRAMES_PER_BUFFER
    segment = left.tolist()[start_sample : end_sample]
    segment = [item[0] for item in segment]
    print "Segement: [%d, %d]" % (start_sample, end_sample)
    chromagram.processAudioFrame(segment)

    if chromagram.isReady():
        print "Printing chromagram for samples [%d,%d]" % (start_sample, end_sample)
        chroma = chromagram.getChromagram()
        PrintChroma(chroma)
        print "Not ready in a row previous: %d" % not_ready_count
        print "Frame Number: %d" % frame
        print "\n"
        not_ready_count = 0
        chord_detector = ChordDetector()
        chord_detector.detectChord(chroma)
        print "Chord root: %d" % chord_detector.rootNote
    else:
        print "Chromagram was not ready"
        not_ready_count += 1
'''
