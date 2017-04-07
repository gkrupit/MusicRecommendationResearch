import os
import signal
import subprocess
import time
import random
import termios
import thread
import time
from Tkinter import *
import mutex
import psutil
import pylab
import math
import numpy as np
from mutagen.mp3 import MP3

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

results_dir = './Results/'

class MP3Player:
    def __init__(self, music_directory, song_orders, mode, trial_length):
        self.mode = mode
        if mode == 'recommend':
            self.ChooseNextSong = self.RecommendNextSong
        elif mode == 'random':
            self.ChooseNextSong = self.RandomNextSong
        else:
            print 'Invalid mode: <%s>. Exiting player.' % mode
            return None

        self.loved_songs = [] #songs that user really enjoyed

        self.max_songs_to_play = trial_length
        self.max_time = 60.
        self.max_rating = 10.
        self.min_time = 0.0
        self.min_rating = 1.
        #self.min_score = 0.0114942528736#self.GetScore(self.max_time, self.max_rating)
        #self.max_score = 0.111111111111#self.GetScore(self.min_time,self.min_rating)
        self.min_score = self.GetScore(self.max_rating)
        self.max_score = self.GetScore(self.min_rating)
        print 'min: ',self.min_score,'  max: ', self.max_score
        self.rating_cutoff = 8
        self.playlist = [ song for song in song_orders ]
        self.song_orders = song_orders
        self.music_directory = music_directory
        self.already_played = []
        self.elapsed_song_times = []
        self.ratings = []
        self.start_song_time = -1
        self.current_song_process = None
        self.stopped_song_early = False
        self.current_song = ''
        self.prev_song = ''
        self.song_count = 0
        self.PlotScores()
        self.experiment_number = self.DetermineExperimentNumber()
        self.root = Tk()
        self.app = Frame(self.root)
        self.app.pack(side='bottom')
        self.next_button = Button(self.app, text="Start the Experiment!", command=self.NextButtonClicked)
        self.exit_button = Button(self.app, text="Exit Player", command=self.Exit)
        self.next_button.pack()
        self.exit_button.pack()
        #self.root.mainloop()

    def DetermineExperimentNumber(self):
        pattern = re.compile('e(\d+).txt')
        matches = [ pattern.match(f) for f in os.listdir(results_dir) if f.endswith('.txt') ]
        if not matches:
            return 1 #First experiment
        previous_experiments = [ int(match.group(1)) for match in matches ]
        last_experiment_number = max(previous_experiments)
        return last_experiment_number + 1

    '''
      Results File Format:
        line 1: experiment #
        line 2: distance | random    (distance = was distance used to get next song, random = songs randomly chosen)
        lines 3 - end:  <Song Name>, <Amount of time played>, <1-10 rating, how much did they like?>
          (note: first song, distance from previous = -1 )

    '''

    def WriteResults(self):
        with open('%se%d.txt' % (results_dir, self.experiment_number), 'w') as f:
            f.write('%d\n' % self.experiment_number)
            f.write(self.mode)
            f.write('\n')

            for (song, time, rating) in zip(self.already_played, self.elapsed_song_times, self.ratings):
                f.write('%s,%s,%s\n' % (song, time, rating))

    def ExperimentOver(self):
        return self.song_count == self.max_songs_to_play

    def NextButtonClicked(self):
        if self.IsCurrentlyPlaying():
            self.stopped_song_early = True
            self.DoneWithSong()
            self.next_button['text'] = 'Play Next Song'
        else:
            if self.ExperimentOver():
                print '\n\n\n\n\n'
                print 'Finished %d song trial.' % self.max_songs_to_play
                self.Exit() # Destroy MP3 Player
                return
            self.stopped_song_early = False
            self.PlayNext()
            self.next_button['text'] = 'Stop Playing Song'

    def PlotScores(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        #score = lambda time, rating: np.exp(-rating/self.max_rating) / time / 10
        #score = lambda time, rating: np.tanh(rating / 10 ) / time
        score = lambda rating: np.exp(-rating/4)
        ratings = np.arange(self.min_rating, self.max_rating + 0.1, 1)
        #times = np.arange(self.min_time, self.max_time + 0.1, 0.5)
        #ratings, times = np.meshgrid(ratings, times)
        scores = score(ratings)

        max_score = score(self.min_rating)
        min_score = score(self.max_rating)
        print min_score, max_score
        print np.min(scores), np.max(scores)

        '''
        min_score = score(self.max_time, self.max_rating)
        max_score = score(self.min_time, self.min_rating)
        print min_score, max_score
        print score(0.0, 1)

        scores = score(ratings, times)

        print 'min: ', min_score,'  max: ', max_score
        for i,time in enumerate(scores):
            for j,scorex in enumerate(time):
                #print i * 0.5, j + 1
                if scorex == 1./9:
                    print i * 0.5, j + 1
                    print '  ', scorex
                    print '  ',score(i * 0.5, j + 1)
                if np.abs(scorex - 0.0114942528736) < 0.00000001:
                    print i * 0.5, j + 1
                    print '  ', scorex
                    print '  ',score(i * 0.5, j + 1)
                #print '  ', score
        #max_score = np.max(scores)
        #min_score = np.min(scores)
        print 'calc min:', np.min(scores), '  calc max:', np.max(scores)
        print 'fun min:', score(60.0,10), '  fun max: ', score(0.0,1)


        #adjust = lambda score: (score - min) / (max - min)
        #scores = adjust(scores)

        #print np.min(scores),np.max(scores)
        '''
        last_index = len(self.playlist) - 1
        print last_index

        indices = (last_index) * (scores - min_score) / (max_score - min_score)



        #scores = (1 - scores / max_score) * (len(self.playlist) - 1)
        #next_index_ratio = lambda score: 1 - score / max_score



        #print score(self.max_time, self.max_rating), max_score
        #print 1 - score(self.max_time, self.max_rating) / next_index_ratio(max_score)

        #ratios = next_index_ratio(scores)
        #indices = ratios * ( len(self.playlist) - 1 )
        # Plot a basic wireframe.
        ax.plot(ratings, indices)
        #ax.plot_wireframe(ratings, times, indices, rstride=5, cstride=1)
        ax.set_xlabel('Rating')
        #ax.set_ylabel('Duration Listened (seconds)')
        ax.set_ylabel('Next Song Index')
        plt.title('Index of Next Song Given Previous Song Results')

        plt.show()



    def RandomNextSong(self):
        next_song = random.choice(self.playlist)
        while next_song in self.already_played:
            next_song = random.choice(self.playlist)
        #self.already_played.append(next_song)
        #self.playlist.remove(next_song)
        print 'Random next song: ', next_song
        return next_song

    def GetScore(self, rating):
        #time = min(time, self.max_time) # if time > max_time, set time = max_time
        raw_score = self.GetRawScore(rating)
        #adjusted_score = 1 - self.AdjustScore(raw_score)
        #print 'Raw: ', raw_score
        #print 'Adjusted: ', adjusted_score
        return raw_score

    def GetRawScore(self, rating):
        return np.exp(-1.*rating/4)

    def AdjustScore(self, score):
         return (score - self.min_score) / (self.max_score - self.min_score)

    def GetNextSongIndex(self):
        score = self.GetLastScore()
        last_index = len(self.playlist) - 1
        print 'min:', self.min_score
        print 'max:', self.max_score
        print 'score', score
        print 'score - min', score - self.min_score
        print 'max - min', self.max_score - self.min_score
        print (score - self.min_score) / (self.max_score - self.min_score)

        next_index = last_index * (score - self.min_score) / (self.max_score - self.min_score)
        return int(next_index)


    def GetScoreIndex(self, index):
        time = self.elapsed_song_times[index]
        rating = self.ratings[index]
        print time, rating
        return self.GetScore(rating)

    def GetLastScore(self):
        return self.GetScoreIndex(-1)


    def RecommendNextSong(self):
        order = [ song_distance[0] for song_distance in self.song_orders[self.prev_song] ]
        print '------------------------------'
        print 'Choosing song to play after <%s>' % (self.prev_song)
        print '------------------------------'
        '''
        Next song = closest in distance to previous song that hasn't been played yet
        '''

        last_song_score = self.GetLastScore()

        last_index = len(order) - 1
        #next_song_index = int((1 - (float(last_song_score) / max_score)) * last_index)
        next_song_index = self.GetNextSongIndex()
        print 'Index: ',next_song_index

        further = order[next_song_index : ]
        closer = order[ 0 : next_song_index ]
        closer.reverse()
        reorder_songs = [ j for i in zip(further,closer) for j in i ]
        leftover = []
        if len(further) > len(closer):
            leftover = further[ len(closer) : ]
        elif len(closer) > len(further):
            leftover = closer[ len(further) : ]

        reorder_songs += leftover

        try:
            next_song = next(song for song in reorder_songs if song not in self.already_played)
        except StopIteration:
            print 'All songs have been played. Exiting'
            self.Exit()


        '''
        print '----------------------------------------'
        print '   Previous song:', self.prev_song
        print '   Song chosen using recommendation algorithm:', next_song
        print '   Prevoius time: ', self.elapsed_song_times[-1]
        print '   Previous rating:', self.ratings[-1]
        print '   Previous song score:', last_song_score
        print '   Max Score: ', self.max_score
        print '   Next song starting position:', next_song_index
        print '   Actual Index in list:', order.index(next_song)
        print '----------------------------------------'
        '''

        return next_song



        # start_index = 0
        # last_song_score = time_last_song_played * rating_last_song
        # if time_last_song_played < 10:
        #     start_index = len(order) // 2
        # elif time_last_song_played < 20:
        #     start_index = len(order) // 3
        # elif time_last_song_played < 30:
        #     start_index = len(order) // 4
        # elif time_last_song_played < 60:
        #     start_index = len(order) // 5
        # else: # listened to for more than 15 seconds
        #     start_index = 0

        # for song in further:
        #     if song not in self.already_played:
        #         return song
        #
        # for song in closer:
        #     if song not in self.already_played:
        #         return song


    def DoneWithSong(self):
        if not self.IsCurrentlyPlaying():
            return

        self.StopPlayingSong()
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        print 'On a scale of 1-10, how much did you enjoy that song? 1=Not at all ... 10=Loved it   '
        rating = sys.stdin.readline()
        while True:
            try:
                rating = int(rating)
                if rating < 1 or rating > 10:
                    raise ValueError
                break
            except ValueError:
                print 'Rating must be integer between 1 and 10. How much did you enjoy the last song?  '
                rating = sys.stdin.readline()
        self.ratings.append(rating)
        print 'Finished with song %d / %d' % (self.song_count, self.max_songs_to_play)
        print 'Click \'Next Song\' when you\'re ready to hear the next one!'

    def EndOfSong(self):
        current_song_file = self.music_directory + self.current_song + '.mp3'
        duration = MP3(current_song_file).info.length
        print 'Waiting', duration, 'for song to end'
        while self.ElapsedTime() < duration:
            if self.stopped_song_early:
                return

            time_remaining = int(duration - self.ElapsedTime())
            if time_remaining % 5 == 0:
                print time_remaining, 'seconds remaining'
            time.sleep(1)
            continue

        # If user listens to entire song, simlulate clicking 'stop song' button
        if not self.stopped_song_early:
            print 'Clicking Button from EndOfSong()'
            self.NextButtonClicked()


    def PlaySong(self, song):
        play_cmd = 'mpg321 ' + self.music_directory + song + '.mp3'
        self.start_song_time = time.time()

        self.current_song_process = subprocess.Popen(play_cmd, shell=True, preexec_fn=os.setsid, stdout=None)
        self.current_song = song
        self.already_played.append(song)

        try:
            thread.start_new_thread( self.EndOfSong, () )
        except:
            print "Error: unable to start thread. Don't listen to the entire song!"


    def StopPlayingSong(self):
        if not self.IsCurrentlyPlaying():
            return

        try:
            os.killpg(os.getpgid(self.current_song_process.pid), signal.SIGTERM)
        except OSError:
            pass

        self.elapsed_song_times.append(self.ElapsedTime())
        self.start_song_time = -1
        self.current_song_process = None
        self.prev_song = self.current_song
        self.current_song = ''


    def PlayNext(self):
        if self.IsCurrentlyPlaying():
            self.StopPlayingSong()

        next_song = ''
        if self.prev_song == '':
            next_song = random.choice(self.playlist)
        else:
            next_song = self.ChooseNextSong()
        self.PlaySong(next_song)
        self.song_count += 1

    def IsCurrentlyPlaying(self):
        if self.current_song_process == None:
            return False

        return True

    def ElapsedTime(self):
        return time.time() - self.start_song_time

    def PrintPlayHistory(self):
        songs_elapsed = zip(self.already_played, self.elapsed_song_times)
        for i, (current_song, elapsed) in enumerate(songs_elapsed):
            how_similar_to_prev = -1
            if i == 0:
                print '1st Song: %s' % current_song
                print '  Time played: %f' % elapsed
            else:
                prev_song = songs_elapsed[i-1][0]
                print 'Song %d: %s' % (i+1, current_song)
                print '  Time played: %f' % elapsed
                (index, d) = [ (i, d) for i, (song, d) in enumerate(self.song_orders[prev_song]) if song == current_song][0]
                print '  How similar to previous song?'
                print '    Place in ordered list: %d. Distance: %f ' % (index, float(d))

    def Exit(self):
        if self.IsCurrentlyPlaying():
            self.StopPlayingSong()
        self.root.destroy()

    def FinishedSuccessfully(self):
        return len(self.already_played) == self.max_songs_to_play \
                    and len(self.ratings) == self.max_songs_to_play \
                    and len(self.elapsed_song_times) == self.max_songs_to_play
