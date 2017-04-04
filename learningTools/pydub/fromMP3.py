from pydub import AudioSegment

song = AudioSegment.from_mp3("../../../MusicSamples/Mr_Mrs_Smith_-_Blazin_Guns.mp3")

channels = song.channels
data = song._data
print('Channels',channels)
print('Data', data)
