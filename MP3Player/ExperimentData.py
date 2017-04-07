import matplotlib.pyplot as plt
import numpy as np
from mutagen.mp3 import MP3
from matplotlib import pylab
import plotly.plotly as py
import plotly.graph_objs as go
from itertools import groupby

results_directory = './Results/'
MP3_directory = '../../AllMusic/'

class ExperimentData:
    def __init__(self, filename):
        self.filename = filename
        self.experiment_number = -1
        self.songs_played = []
        self.times = []
        self.percentage_listened = []
        self.ratings = []
        self.type = ''
        self.num_songs = -1
        self.X = []
        self.ParseResults()
        self.num_jumpss = { 'random' : 0, 'recommend' : 0 }
        self.song_counts = dict()

    def GetX(self):
        return self.X

    def GetType(self):
        return self.type

    @staticmethod
    def GetSongLength(song_name):
        mp3_filename = MP3_directory + song_name + '.mp3'
        return MP3(mp3_filename).info.length

    def GetPercentListened(self):
        return self.percentage_listened

    @staticmethod
    def AverageSongRating(songname, experiments):
        pass

    @staticmethod
    def AverageRatingPerSongExperiments(experiments, song_counts):
        pass


    @staticmethod
    def AverageRatingPerSong(experiments, which):
        print which
        song_counts = ExperimentData.CountSongs(experiments)
        rating_per_song = { song : 0 for song in song_counts }
        for e in experiments:
            for song,rating in zip(e.songs_played, e.ratings):
                rating_per_song[song] += rating

        avg_rating_per_song = dict()

        for song in rating_per_song:
            avg_rating_per_song[song] = 1. * rating_per_song[song] / song_counts[song]

        #for song,count in sorted(song_counts.items(), key=lambda pair: pair[1]):
        #    print '%s: %d, %.2f' % (song,count,avg_rating_per_song[song])
        avg_times_played = np.mean(song_counts.values())
        print '%s: %f' % (which, avg_times_played)


        song_count_list = sorted(song_counts.items(), key=lambda pair: pair[1], reverse=True)
        fig = plt.figure()
        names,counts = zip(*song_count_list)
        ratings = [ avg_rating_per_song[song] for song in names ]

        pylab.rcParams['font.size'] = 8
        fig = plt.figure()
        ax = plt.subplot(111)
        color_map = plt.get_cmap('Greens')

        colors = [ color_map(rating/10) for rating in ratings ]
        #print ratings
        #print colors
        width=0.8
        bars = ax.bar(range(len(names)), counts, color=colors, width=width)
        ax.set_xticks(np.arange(len(names)) + width/2)
        ax.set_xticklabels(names, rotation=90)
        fig.autofmt_xdate()

        #for song,bar in zip(names, )
        pylab.rcParams['font.size'] = 10
        ax.set_xlabel('Song Name')
        ax.set_ylabel('Number of Times Played over ' + which + ' Experiments')
        plt.title('Number of Plays Per Song, Average Rating per Song')
        plt.show()
        pylab.rcParams['font.size'] = 12





    def RemoveBadSongs(self):
        bad_songs = ['LetItBe_C']
        for song in bad_songs:
            index = -1
            try:
                index = self.songs_played.index(song)
            except ValueError: # Bad song not in experiment
                continue
            del self.songs_played[index]
            del self.times[index]
            del self.percentage_listened[index]
            del self.ratings[index]
            del self.X[index]


    @staticmethod
    def CountSongs(experiments):
        songs = []
        for e in experiments:
            songs += e.songs_played

        song_counts = dict()
        for song, group in groupby(sorted(songs)):
            song_counts[song] = len(list(group))

        #for song, count in sorted(song_counts.items(), key=lambda item: item[1], reverse=True):
        #    print '%s: %d' % (song, count)

        return song_counts




    def ParseResults(self):
        lines = []
        with open(results_directory + self.filename, 'r') as f:
            lines = [ line.strip() for line in f.readlines() ]

        self.experiment_number = int(lines[0])
        self.type = lines[1]

        song_data = [ line.split(',') for line in lines[2:] ]

        self.ratings = [ int(data[2]) for data in song_data ]
        self.songs_played = [ data[0] for data in song_data ]
        self.times = [ float(data[1]) for data in song_data ]
        for (time, song) in zip( self.times, self.songs_played ):
            song_length = ExperimentData.GetSongLength(song)
            percentage = float(time) / song_length * 100
            if percentage > 100:
                percentage = 100
            self.percentage_listened.append(percentage)

        self.num_songs = len(self.songs_played)
        self.X = range(1, self.num_songs + 1)

        self.RemoveBadSongs()

    def Print(self):
        print '----------------------------'
        print 'Experiment %d:' % self.experiment_number
        print '  Songs Played:'
        for song in self.songs_played:
            print '    ',song
        print

        print '  Times:'
        for time in self.times:
            print '    ', time
        print

        print '  Ratings:'
        for rating in self.ratings:
            print '    ', rating
        print '----------------------------'

    def Time(self, n):
        return self.times[n]

    def Rating(self, n):
        return self.ratings[n]

    def GetTimes(self):
        return self.times

    def GetRatings(self):
        return self.ratings

    def PlotTimes(self):
        plt.scatter(self.X, self.times, 'rx')
        plt.show()

    def PlotDurationPercentages(self):
        plt.scatter(self.X, self.percentage_listened, 'rx')
        plt.show()

    def PlotRatings(self):
        plt.scatter(self.X, self.ratings, 'gx')
        plt.show()

    def PlotRatingsAndPercentages(self):
        fig, ax1 = plt.subplots()
        ax1.plot(self.X, self.ratings, 'b')
        ax1.set_xlabel('Song # In Trial')
        #axes = plt.gca()
        #axes.set_xlim([xmin,xmax])
        ax1.set_ylim([1,10])
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Rating (1-10)', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(self.X, self.percentage_listened, 'r')
        ax2.set_ylabel('% of Song Listened To', color='r')
        ax2.set_ylim([0,100])
        ax2.tick_params('y', colors='r')

        fig.tight_layout()
        plt.xticks(np.arange(min(self.X), max(self.X)+1, 1))
        plt.title('Experiment #%d' % self.experiment_number)


        plt.show()





    def PlotRatingsAndTimes(self):
        fig, ax1 = plt.subplots()
        ax1.plot(self.X, self.ratings, 'b')
        ax1.set_xlabel('Song # In Trial')
        #axes = plt.gca()
        #axes.set_xlim([xmin,xmax])
        ax1.set_ylim([1,10])
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Rating (1-10)', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(self.X, self.times, 'r')
        ax2.set_ylabel('Time Played (seconds)', color='r')
        ax2.tick_params('y', colors='r')

        fig.tight_layout()
        plt.xticks(np.arange(min(self.X), max(self.X)+1, 1))
        plt.title('Experiment #%d - %s' % self.experiment_number)
        plt.show()
        #plt.plot(self.X, self.times, 'r', self.X, self.ratings, 'g')
        #plt.show()


    def Plot(self):
        self.PlotRatingsAndPercentages()

    def NumSongs(self):
        return num_songs

    def GetExperimentNumber(self):
        return self.experiment_number

    @staticmethod
    def ScaleRatings(ratings):
        new_minimum = 1
        new_maximum = 10
        minimum = min(ratings)
        maximum = max(ratings)
        ratings = map(lambda r: (new_maximum - new_minimum) *
                             (float(r) - minimum) / (maximum - minimum) + new_minimum, ratings)
        return ratings


    @staticmethod
    def JumpType(r1, r2):
        threshold = 5.5
        if r1 <= threshold and r2 <= threshold:
            return 'staylow'

        if r1 <= threshold and r2 > threshold:
            return 'up'

        if r1 > threshold and r2 <= threshold:
            return 'down'

        if r1 > threshold and r2 > threshold:
            return 'stayhigh'






    @staticmethod
    def AnalyzeJumps(successive_ratings):
        jumps = dict()
        count = 0
        for r1, r2 in successive_ratings:
            jump_type = ExperimentData.JumpType(r1,r2)
            try:
                jumps[jump_type].append((r1,r2))
            except KeyError:
                jumps[jump_type] = [ (r1,r2) ]
            count += 1

        return jumps, count



    @staticmethod
    def RatingVsTimeByUser(results):
        experiments = results['random'] + results['recommend']
        color = []
        area = []
        X = []
        y = []
        for i,e in enumerate(experiments):
            num_songs = len(e.GetRatings())
            color += e.GetRatings()
            area += [ time * 5 for time in e.GetPercentListened() ]
            X += range(1, num_songs + 1)
            y += [i * 7  + 1] * num_songs

        # making the scatter plot
        sct = plt.scatter(X, y, c=color, s=area, linewidths=2, edgecolor='w')
        plt.colorbar(sct)
        #plt.sct.set_alpha(0.75)

        plt.axis([0,11,0,len(y) + 1])
        plt.xlabel('Song # In Experiment')
        plt.ylabel('Subject')
        plt.show()



    @staticmethod
    def RatingVsTimeSuccessiveBubble(results):
        experiments = results['random'] + results['recommend']
        rating_vs_time = []
        for e in experiments:
            ratings = e.ratings
            times = e.percentage_listened
            successive_ratings = zip(ratings, ratings[1:])
            successive_times = zip(times, times[1:])
            rating_vs_time += zip(successive_ratings,successive_times)


        color = []
        area = []
        X = []
        y = []
        print rating_vs_time
        for i,((r1,r2),(t1,t2)) in enumerate(rating_vs_time):
            rating_change = r2 - r1
            time_change = t2 - t1
            if rating_change >= 0:
                color.append(rating_change+8)
            else:
                color.append(-rating_change)

            #color.append(r1 - r2)
            #area.append(abs((t1 - t2)*10))
            area.append(abs(time_change)*25)
            X.append(r1 - r2)
            y.append(i+1)

        # making the scatter plot
        sct = plt.scatter(X, y, c=color, s=area, linewidths=2, edgecolor='w')
        plt.colorbar(sct)
        #plt.sct.set_alpha(0.75)

        plt.axis([-10,10,0,200])
        plt.xlabel('Change in Rating')
        plt.ylabel('Change in Percent Listened')
        plt.title('Trend in Rating vs. Time Listened')
        plt.show()


    @staticmethod
    def RatingVsTimeSuccessiveScatter(results):
        experiments = results['random'] + results['recommend']
        experiments = [ e for e in experiments if e.GetExperimentNumber() != 19 and e.GetExperimentNumber() != 20 ]
        rating_vs_time = []
        for e in experiments:
            ratings = e.ratings
            times = e.percentage_listened
            successive_ratings = zip(ratings, ratings[1:])
            successive_times = zip(times, times[1:])
            rating_vs_time += zip(successive_ratings,successive_times)


        color = []
        area = []
        X_trend = []
        X_notrend = []
        y_trend = []
        y_notrend = []
        print rating_vs_time
        for i,((r1,r2),(t1,t2)) in enumerate(rating_vs_time):
            if (r2 >= r1 and t2 >= t1) or (r2 <= r1 and t2 <= t1):
                X_trend.append(r2 - r1)
                y_trend.append(t2 - t1)
            else:
                X_notrend.append(r2 - r1)
                y_notrend.append(t2 - t1)

        # making the scatter plot
        plt.plot(X_trend, y_trend,'go')
        plt.plot(X_notrend, y_notrend,'rx')

        X = X_trend + X_notrend
        y = y_trend + y_notrend
        print len(X),len(y)

        m, b = np.polyfit(X, y, 1)

        print len(X)
        Y = map(lambda x: m * x + b, X)
        print len(X), len(Y)
        plt.plot(X,Y,'-')
        #plt.sct.set_alpha(0.75)

        plt.axis([-10,10,-100,100])
        plt.xlabel('Successive Change in Rating')
        plt.ylabel('Successive Change in Percent Listened To')
        plt.title('Change in Rating vs Change in Percent of Song Listened To')
        plt.show()


    @staticmethod
    def RatingVsTime(results):
        experiments = results['random'] + results['recommend']
        color = []
        area = []
        X = []
        y = []
        for i,e in enumerate(experiments):
            num_songs = len(e.GetRatings())
            color += e.GetRatings()
            area += [ time * 5 for time in e.GetPercentListened() ]
            X += [i+1]*len(e.GetRatings())
            y += [ time for time in e.GetPercentListened() ]

        # making the scatter plot
        sct = plt.scatter(X, y, c=color, s=area, linewidths=2, edgecolor='w')
        plt.colorbar(sct)
        #plt.sct.set_alpha(0.75)

        plt.axis([0,len(experiments)+1,0,110])
        plt.xlabel('Subject Number')
        plt.ylabel('Percent Listened To')
        plt.title('Rating vs Percent of Song Listened To')
        plt.show()



    @staticmethod
    def RatingVsTimeSuccessive(results):
        experiments = results['random'] + results['recommend']
        behavior = []
        for e in experiments:
            e_behavior = { 'same' : 0, 'different' : 0 }
            ratings = e.ratings
            #ratings = ExperimentData.ScaleRatings(ratings)
            times = e.percentage_listened
            successive_ratings = zip(ratings, ratings[1:])
            successive_times = zip(times, times[1:])
            for (r1,r2),(t1,t2) in zip(successive_ratings, successive_times):
                if r1 <= r2 and t1 <= t2: # both rating and time went up
                    e_behavior['same'] += 1
                elif r1 > r2 and t1 > t2: # both rating and time went down
                    e_behavior['same'] += 1
                else: # rating, time behavior were different
                    e_behavior['different'] += 1

            behavior.append(e_behavior)


        better = 0
        worse = 0
        threshold = 0.5
        for e_behavior in behavior:
            total = e_behavior['same'] + e_behavior['different']
            percent_same = 1. * e_behavior['same'] / total
            if percent_same >= threshold:
                better += 1
            else:
                worse += 1

        total = better + worse
        percent_better = 1. * better / total * 100
        print '%.2f users followed the trend at least %f of the time' % (percent_better, threshold)


    '''
      Analyze all successive rating jump types
      Two bar plots:
        1. Actual data, Scaled % / Random %
        2. Scaled data, Scaled % / Random %
    '''
    @staticmethod
    def AnalyzeAll(experiments):

        '''
          Show pie charts with original, unscaled ratings
        '''
        successive_actual_ratings = { 'random' : [], 'recommend' : [] }
        successive_scaled_ratings = { 'random' : [], 'recommend' : [] }
        all_actual_ratings = []
        all_scaled_ratings = []

        for e in experiments['random']:
            actual_ratings = e.GetRatings()
            scaled_ratings = ExperimentData.ScaleRatings(actual_ratings)
            all_actual_ratings += actual_ratings
            all_scaled_ratings += scaled_ratings
            successive_actual_ratings['random'] += zip(actual_ratings, actual_ratings[1:])
            successive_scaled_ratings['random'] += zip(scaled_ratings, scaled_ratings[1:])

        for e in experiments['recommend']:
            actual_ratings = e.GetRatings()
            scaled_ratings = ExperimentData.ScaleRatings(actual_ratings)
            all_actual_ratings += actual_ratings
            all_scaled_ratings += scaled_ratings
            successive_actual_ratings['recommend'] += zip(actual_ratings, actual_ratings[1:])
            successive_scaled_ratings['recommend'] += zip(scaled_ratings, scaled_ratings[1:])


        print 'Average actual rating: %.2f' % (np.mean(all_actual_ratings))
        print 'Median actual rating: %.2f' % (np.median(all_actual_ratings))
        print
        print 'Average scaled rating: %.2f' % (np.mean(all_scaled_ratings))
        print 'Median scaled rating: %.2f' % (np.median(all_scaled_ratings))
        random_actual_jumps, random_actual_jump_count = ExperimentData.AnalyzeJumps(successive_actual_ratings['random'])
        recommend_actual_jumps, recommend_actual_jump_count = ExperimentData.AnalyzeJumps(successive_actual_ratings['recommend'])

        random_scaled_jumps, random_scaled_jump_count = ExperimentData.AnalyzeJumps(successive_scaled_ratings['random'])
        recommend_scaled_jumps, recommend_scaled_jump_count = ExperimentData.AnalyzeJumps(successive_scaled_ratings['recommend'])

        scaled_ratio = dict()
        actual_ratio = dict()
        print 'Actual'
        for jump_type in random_actual_jumps:
            random_actual_percent = round(1. * len(random_actual_jumps[jump_type]) / random_actual_jump_count, 3)
            recommend_actual_percent = round(1. * len(recommend_actual_jumps[jump_type]) / recommend_actual_jump_count, 3)
            #print '  recommend/random: %.2f' % (recommend_actual_percent / random_actual_percent)
            print '    random. %s = %.1f' % (jump_type, random_actual_percent*100)
            print '    recommend. %s = %.1f' % (jump_type, recommend_actual_percent*100)
            actual_ratio[jump_type] = round(recommend_actual_percent / random_actual_percent, 3)

        print 'Scaled'
        for jump_type in random_scaled_jumps:
            random_scaled_percent = round(1. * len(random_scaled_jumps[jump_type]) / random_scaled_jump_count, 3)
            recommend_scaled_percent = round(1. * len(recommend_scaled_jumps[jump_type]) / recommend_scaled_jump_count, 3)
            #print '  recommend/random: %.2f' % (recommend_scaled_percent / random_scaled_percent)
            print '    random. %s = %.1f' % (jump_type, random_scaled_percent*100)
            print '    recommend. %s = %.1f' % (jump_type, recommend_scaled_percent*100)
            scaled_ratio[jump_type] = round(recommend_scaled_percent / random_scaled_percent, 3)

        print 'Ratios (Recommend / Scaled)'
        for jump_type in scaled_ratio:
            print '  Scaled. %s: %f' % (jump_type, scaled_ratio[jump_type])
            print '  Actual. %s: %f' % (jump_type, actual_ratio[jump_type])


        labels = [
                    'Low Rating -> Low Rating',
                    'High Rating -> Low Rating',
                    'Low Rating -> High Rating',
                    'High Rating -> High Rating'
                 ]

        jump_types = ('staylow', 'down','up', 'stayhigh')
        N = 4
        actual = [ actual_ratio[jump_type] for jump_type in jump_types ]

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, actual, width, color='g')

        scaled = [ scaled_ratio[jump_type] for jump_type in jump_types ]

        rects2 = ax.bar(ind + width, scaled, width, color='b')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Ratio: Recommend / Random')
        ax.set_title('Actual vs. Scaled Ratings: kALE/Random Ratio by Rating Transition Type')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(labels)
        ax.set_ylim([0,2])


        ax.legend((rects1[0], rects2[0]), ('Actual Ratings', 'Scaled Ratings to Fit Range [1,10]'))


        def autolabel(rects, values):
            """
            Attach a text label above each bar displaying its height
            """
            for rect, value in zip(rects, values):
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%.3f' % value,
                        ha='center', va='bottom')

        autolabel(rects1, actual)
        autolabel(rects2, scaled)

        plt.show()

        '''
        print 'Random Jumps:'
        for jump_type in random_jumps:
            print '  ',jump_type, ': ', round(1. * len(random_jumps[jump_type]) / random_jump_count, 3) * 100

        print 'Recommend Jumps'
        for jump_type in recommend_jumps:
            print '  ',jump_type, ': ', round(1. * len(recommend_jumps[jump_type]) / recommend_jump_count, 3) * 100

        sizes = [
                    len(random_jumps['up']),
                    len(random_jumps['down']),
                    len(random_jumps['stayhigh']),
                    len(random_jumps['staylow'])
                ]

        explode = (0, 0.1, 0.1, 0.0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        #pylab.rcParams['font.size'] = 30
        fig1, ax1 = plt.subplots()
        r = (255/255, 1.*128/255, 1.*128/255)
        b = (1.*153/255, 1.*194/255, 255/255)
        c = (1.*194/255, 1.*240/255, 1.*240/255)
        g = (0,1.*128/255,0)
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c],labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Randomly Generated Songs: Actual Rating Change from Song to Song',y=1.04)

        #plt.savefig('./figures/random_actual.png')
        plt.show()

        sizes = [
                    len(recommend_jumps['up']),
                    len(recommend_jumps['down']),
                    len(recommend_jumps['stayhigh']),
                    len(recommend_jumps['staylow'])
                ]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c], labels=labels,autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('kALE Recommendation System: Actual Rating Change from Song to Song',y=1.04)
        #plt.savefig('./figures/recommend_actual.png')

        plt.show()
        '''


        '''
          Show pie charts with scaled ratings
        '''
        '''
        successive_ratings = { 'random' : [], 'recommend' : []}
        all_ratings = []
        random_ratings = []
        recommend_ratings = []

        for e in experiments['random']:
            ratings = e.GetRatings()
            all_ratings += ratings
            ratings = ExperimentData.ScaleRatings(ratings)
            successive_ratings['random'] += zip(ratings, ratings[1:])

        for e in experiments['recommend']:
            ratings = e.GetRatings()
            all_ratings += ratings
            ratings = ExperimentData.ScaleRatings(ratings)
            successive_ratings['recommend'] += zip(ratings, ratings[1:])


        #print 'Average rating: %.2f' % (np.mean(all_ratings))
        #print 'Median rating: %d' % (np.median(all_ratings))
        random_jumps, random_jump_count = ExperimentData.AnalyzeJumps(successive_ratings['random'])
        recommend_jumps, recommend_jump_count = ExperimentData.AnalyzeJumps(successive_ratings['recommend'])

        print 'Random Jumps:'
        for jump_type in random_jumps:
            print '  ',jump_type, ': ', round(1. * len(random_jumps[jump_type]) / random_jump_count, 3) * 100

        print 'Recommend Jumps'
        for jump_type in recommend_jumps:
            print '  ',jump_type, ': ', round(1. * len(recommend_jumps[jump_type]) / recommend_jump_count, 3) * 100

        sizes = [
                    len(random_jumps['up']),
                    len(random_jumps['down']),
                    len(random_jumps['stayhigh']),
                    len(random_jumps['staylow'])
                ]

        explode = (0, 0.1, 0.1, 0.0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        #pylab.rcParams['font.size'] = 30
        fig1, ax1 = plt.subplots()
        r = (255/255, 1.*128/255, 1.*128/255)
        b = (1.*153/255, 1.*194/255, 255/255)
        c = (1.*194/255, 1.*240/255, 1.*240/255)
        g = (0,1.*128/255,0)
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c],labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(' Randomly Generated Songs: Scaled Rating Change from Song to Song',y=1.04)

        #plt.savefig('./figures/random_scaled.png')

        plt.show()

        sizes = [
                    len(recommend_jumps['up']),
                    len(recommend_jumps['down']),
                    len(recommend_jumps['stayhigh']),
                    len(recommend_jumps['staylow'])
                ]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c], labels=labels,autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('kALE Recommendation System: Scaled Rating Change from Song to Song',y=1.04)
        #plt.savefig('./figures/recommend_scaled.png')

        plt.show()
    '''

    '''
      Analyze all successive rating jump types
      Four Pie Charts:
        1. Random, Actual data
        2. Recommend, Actual data
        3. Random, scaled data
        4. Recommend, scaled data
    '''
    '''
    @staticmethod
    def AnalyzeAll(experiments):

        labels = [
                    'Low Rating -> High Rating',
                    'High Rating -> Low Rating',
                    'High Rating -> High Rating',
                    'Low Rating -> Low Rating'
                 ]


        successive_ratings = { 'random' : [], 'recommend' : []}
        all_ratings = []
        random_ratings = []
        recommend_ratings = []

        for e in experiments['random']:
            ratings = e.GetRatings()
            all_ratings += ratings
            #ratings = ExperimentData.ScaleRatings(ratings)
            successive_ratings['random'] += zip(ratings, ratings[1:])

        for e in experiments['recommend']:
            ratings = e.GetRatings()
            all_ratings += ratings
            #ratings = ExperimentData.ScaleRatings(ratings)
            successive_ratings['recommend'] += zip(ratings, ratings[1:])


        #print 'Average rating: %.2f' % (np.mean(all_ratings))
        #print 'Median rating: %d' % (np.median(all_ratings))
        random_jumps, random_jump_count = ExperimentData.AnalyzeJumps(successive_ratings['random'])
        recommend_jumps, recommend_jump_count = ExperimentData.AnalyzeJumps(successive_ratings['recommend'])

        print 'Random Jumps:'
        for jump_type in random_jumps:
            print '  ',jump_type, ': ', round(1. * len(random_jumps[jump_type]) / random_jump_count, 3) * 100

        print 'Recommend Jumps'
        for jump_type in recommend_jumps:
            print '  ',jump_type, ': ', round(1. * len(recommend_jumps[jump_type]) / recommend_jump_count, 3) * 100

        sizes = [
                    len(random_jumps['up']),
                    len(random_jumps['down']),
                    len(random_jumps['stayhigh']),
                    len(random_jumps['staylow'])
                ]

        explode = (0, 0.1, 0.1, 0.0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        #pylab.rcParams['font.size'] = 30
        fig1, ax1 = plt.subplots()
        r = (255/255, 1.*128/255, 1.*128/255)
        b = (1.*153/255, 1.*194/255, 255/255)
        c = (1.*194/255, 1.*240/255, 1.*240/255)
        g = (0,1.*128/255,0)
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c],labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Randomly Generated Songs: Actual Rating Change from Song to Song',y=1.04)

        #plt.savefig('./figures/random_actual.png')
        plt.show()

        sizes = [
                    len(recommend_jumps['up']),
                    len(recommend_jumps['down']),
                    len(recommend_jumps['stayhigh']),
                    len(recommend_jumps['staylow'])
                ]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c], labels=labels,autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('kALE Recommendation System: Actual Rating Change from Song to Song',y=1.04)
        #plt.savefig('./figures/recommend_actual.png')

        plt.show()

        successive_ratings = { 'random' : [], 'recommend' : []}
        all_ratings = []
        random_ratings = []
        recommend_ratings = []

        for e in experiments['random']:
            ratings = e.GetRatings()
            all_ratings += ratings
            ratings = ExperimentData.ScaleRatings(ratings)
            successive_ratings['random'] += zip(ratings, ratings[1:])

        for e in experiments['recommend']:
            ratings = e.GetRatings()
            all_ratings += ratings
            ratings = ExperimentData.ScaleRatings(ratings)
            successive_ratings['recommend'] += zip(ratings, ratings[1:])


        #print 'Average rating: %.2f' % (np.mean(all_ratings))
        #print 'Median rating: %d' % (np.median(all_ratings))
        random_jumps, random_jump_count = ExperimentData.AnalyzeJumps(successive_ratings['random'])
        recommend_jumps, recommend_jump_count = ExperimentData.AnalyzeJumps(successive_ratings['recommend'])

        print 'Random Jumps:'
        for jump_type in random_jumps:
            print '  ',jump_type, ': ', round(1. * len(random_jumps[jump_type]) / random_jump_count, 3) * 100

        print 'Recommend Jumps'
        for jump_type in recommend_jumps:
            print '  ',jump_type, ': ', round(1. * len(recommend_jumps[jump_type]) / recommend_jump_count, 3) * 100

        sizes = [
                    len(random_jumps['up']),
                    len(random_jumps['down']),
                    len(random_jumps['stayhigh']),
                    len(random_jumps['staylow'])
                ]

        explode = (0, 0.1, 0.1, 0.0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        #pylab.rcParams['font.size'] = 30
        fig1, ax1 = plt.subplots()
        r = (255/255, 1.*128/255, 1.*128/255)
        b = (1.*153/255, 1.*194/255, 255/255)
        c = (1.*194/255, 1.*240/255, 1.*240/255)
        g = (0,1.*128/255,0)
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c],labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(' Randomly Generated Songs: Scaled Rating Change from Song to Song',y=1.04)

        #plt.savefig('./figures/random_scaled.png')

        plt.show()

        sizes = [
                    len(recommend_jumps['up']),
                    len(recommend_jumps['down']),
                    len(recommend_jumps['stayhigh']),
                    len(recommend_jumps['staylow'])
                ]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode,colors=[b,r,g,c], labels=labels,autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('kALE Recommendation System: Scaled Rating Change from Song to Song',y=1.04)
        #plt.savefig('./figures/recommend_scaled.png')

        plt.show()
    '''

    @staticmethod
    def PlotAll(experiment_list):
        if not experiment_list:
            print 'No experiments to plot.'
            return

        num_songs_per_experiment = len(experiment_list[0].GetX())

        cm = plt.get_cmap('gist_rainbow')
        fig = plt.figure()
        ax = fig.add_subplot(111)


#        time_by_song_index = [ [ e.Time(n) for i in range(e.NumSongs()) ] for e in experiment_list ]


        for e in experiment_list:
            plt.plot(e.GetX(), e.GetRatings(), label='Experiment %d' % (e.GetExperimentNumber()))
        plt.title('Ratings/Song: All Experiments')
        plt.xticks(np.arange(1, num_songs_per_experiment + 1, 1)) # 1 through Number of Songs
        plt.show()
        plt.gcf().clear()

        for e in experiment_list:
            plt.plot(e.GetX(), e.GetTimes(), label='Experiment %d' % (e.GetExperimentNumber()))
        plt.title('Time Listened/Song: All Experiments')
        plt.xticks(np.arange(1, num_songs_per_experiment + 1, 1))
        plt.show()
        plt.gcf().clear()
