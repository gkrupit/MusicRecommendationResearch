import os
import signal
import subprocess
import time
import random
from Tkinter import *

class MP3Player:
    def __init__(self, music_directory, song_orders):
        self.max_songs_to_play = 10
        self.playlist = [ song for song in song_orders ]
        self.song_orders = song_orders
        self.music_directory = music_directory
        self.already_played = []
        self.elapsed_song_times = []
        self.ratings = []
        self.start_song_time = -1
        self.current_song_process = -1
        self.current_song = ''
        self.prev_song = ''
        self.song_count = 0

        self.root = Tk()
        self.app = Frame(self.root)
        self.app.pack(side='bottom')
        self.next_button = Button(self.app, text="Next song please!", command=self.NextButtonClicked)
        self.exit_button = Button(self.app, text="Exit Player", command=self.Exit)
        self.next_button.pack()
        self.exit_button.pack()

        self.rating_root = None
        self.last_rating = IntVar()
        self.last_rating.set(1)



    def Start(self):
        self.root.mainloop()

    '''
      Results File Format:
        line 1: experiment #
        line 2: distance | random    (distance = was distance used to get next song, random = songs randomly chosen)
        lines 3 - end:  <Song Name>, <Amount of time played>, <1-10 rating, how much did they like?>
          (note: first song, distance from previous = -1 )

    '''

    def WriteResults(self):
        experiment_number = 1
        existing_files = [ f for f in os.listdir('./Results/') if f.endswith('.txt') ]
        if existing_files:
            experiment_number = len(existing_files) + 1
        with open('Results/e%d.txt' % experiment_number, 'w') as f:
            f.write('%d\n' % experiment_number)
            if True: # will be replaced with if using recommendation algorithm
                f.write('distance\n')
            else:
                f.write('random\n')

            for (song, time, rating) in zip(self.already_played, self.elapsed_song_times, self.ratings):
                f.write('%s,%s,%s\n' % (song, time, rating))


    def NextButtonClicked(self):
        if self.IsCurrentlyPlaying():
            self.DoneWithSong()
            self.next_button['text'] = 'Play Next Song'
        else:
            self.PlayNext()
            self.next_button['text'] = 'Stop Playing Song'

    def ChooseNextSong(self):
        time_last_song_played = self.elapsed_song_times[-1]
        order = self.song_orders[self.prev_song]
        print '------------------------------'
        print 'Choosing song to play after <%s>' % (self.prev_song)
        print '------------------------------'
        '''
        Next song = closest in distance to previous song that hasn't been played yet
        '''
        #max_time = 60
        #if time_last_song_played > max_time:
    #        time_last_song_played = max_time

        #last_index = len(order) - 1

        #next_song_index = int((1 - (time_last_song_played / max_time)) * last_index)

        start_index = 0
        if time_last_song_played < 10:
            start_index = len(order) // 2
        elif time_last_song_played < 20:
            start_index = len(order) // 3
        elif time_last_song_played < 30:
            start_index = len(order) // 4
        elif time_last_song_played < 60:
            start_index = len(order) // 5
        else: # listened to for more than 15 seconds
            start_index = 0

        for i,song_distance in enumerate(order[start_index:]):
            if song_distance[0] not in self.already_played:
                print 'Prev song:', self.prev_song
                print 'Choosing new song:', song_distance[0]
                print 'Prev song played for', time_last_song_played, 'seconds.'
                print 'New songs from index', start_index
                print 'New Song at index', i + start_index
                return song_distance[0]

        print 'All songs have been played -- closing player.'
        self.Exit()

    def GetRating(self):
        self.rating_root = Tk()
        rating_app = Frame(self.rating_root)

        #Choices for radio button: [ ("1", 1), ("2", 2), ... , ("10", 10)]
        ratings = [ (str(n), n) for n in range(1, 10 + 1) ]

        self.last_rating.set(1)
        rating_buttons = []
        rating_label = Label(self.rating_root, text='How much did you enjoy the last song?',justify = LEFT,padx = 20)
        finalize_rating_button = Button(self.rating_root, text='I am happy with my rating.', justify=CENTER, command=self.rating_root.destroy)
        for txt, val in ratings:
            radiobutton = Radiobutton(self.rating_root,
                        text=txt,
                        padx = 20,
                        variable=self.last_rating,
                        value=val)
            rating_buttons.append(radiobutton)
        rating_label.pack()
        for button in rating_buttons:
            button.pack(anchor=W)
        finalize_rating_button.pack()
        self.rating_root.mainloop()
        return self.last_rating

    def DoneWithSong(self):
        if not self.IsCurrentlyPlaying():
            return

        self.StopPlayingSong()

        self.ratings.append(self.GetRating())
        '''
        rating = raw_input('On a scale of 1-10, how much did you enjoy that song? 1=Not at all ... 10=Loved it   ')
        while True:
            try:
                rating = int(rating)
                if rating < 1 or rating > 10:
                    raise ValueError
                break
            except ValueError:
                 rating = raw_input('Rating must be integer between 1 and 10. How much did you enjoy the last song?  ')
        self.ratings.append(rating)
        '''

        print 'Click \'Next Song\' when you\'re ready to hear the next one!'


    def PlaySong(self, song):
        play_cmd = 'mpg321 ' + self.music_directory + song + '.mp3'
        self.start_song_time = time.time()
        self.current_song_process = subprocess.Popen(play_cmd, shell=True, preexec_fn=os.setsid)
        self.current_song = song
        self.already_played.append(song)

    def StopPlayingSong(self):
        if not self.IsCurrentlyPlaying():
            return

        os.killpg(os.getpgid(self.current_song_process.pid), signal.SIGTERM)
        self.elapsed_song_times.append(self.ElapsedTime())
        self.start_song_time = -1
        self.current_song_process = -1
        self.prev_song = self.current_song
        self.current_song = ''

    def PlayNext(self):
        if self.song_count == self.max_songs_to_play:
            print '\n\n\n\n\n'
            print 'Finished 10 song trial.'
            self.Exit() # Destroy MP3 Player
            return

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
        return self.current_song_process != -1

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
                    and len(self.times) == self.max
