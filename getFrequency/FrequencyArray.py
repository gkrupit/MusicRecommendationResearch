#FrequencyArray

import subprocess
from pydub import AudioSegment
import sys
import scipy.io.wavfile

import wave
import numpy as np
'''
inname = '../../MusicSamples/Mr_Mrs_Smith_-_Blazin_Guns.mp3'
outname = 'testOut.wav'
try:
    check_call(['mpg123', '-w', outname, inname])
except CalledProcessError as e:
    print e
    sys.exit(1)
'''

input_mp3 = "../../MusicSamples/Mr_Mrs_Smith_-_Blazin_Guns.mp3"
input_wav = input_mp3[0:len(input_mp3) - 4] + ".wav"
song_mp3 =AudioSegment.from_mp3("../../MusicSamples/Mr_Mrs_Smith_-_Blazin_Guns.mp3")
song_mp3.export(input_wav, format='wav')
#subprocess.call(['ffmpeg', '-i', input_mp3, input_wav])
'''
channels = song.channels
data = song._data
print('Channels',channels)
print('Data', data)
'''

samplerate, data = scipy.io.wavfile.read(input_wav)
#wr = wave.open(input_wav, 'r')
#sz = wr.getframerate()

print("Sample rate:", samplerate)

#da = np.fromstring(wr.readframes(sz), dtype=np.int16)
#wr.close()

left, right = data[0::2], data[1::2]
left_frequencies = np.fft.fft(left)
right_frequencies = np.fft.fft(right)
'''
print('Left, after fft')
for frequency in left_frequencies:
    print(frequency)
print()
print('Right, after fft')
for frequency in right_frequencies:
    print(frequency)
'''
import matplotlib.pyplot as plt
t = np.arange(256)
sp = np.fft.fft(np.sin(t))
freq = np.fft.fftfreq(t.shape[-1])
#plt.plot(freq, sp.real, freq, sp.imag)
plt.plot(left_frequencies)
plt.show()
