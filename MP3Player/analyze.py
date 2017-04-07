# analyze.py
# Analyze Results from Experiments

import os
from ExperimentData import ExperimentData

results_directory = './Results/'

'''
Read in each results file.
Structure of files:
    line 1: experiment #
    line 2: distance | random    (distance = was distance used to get next song, random = songs randomly chosen)
    lines 3 - 12:  <Song Name>, <Amount of time played>, <1-10 rating, how much did they like?>
'''

MP3_directory = '../../AllMusic/'

def ParseResults(result_filenames):
    experiments = { 'random' : [], 'recommend' : []}
    for filename in result_filenames:
        e = ExperimentData(filename)
        experiments[e.GetType()].append(e)

    return experiments

def main():

    result_filenames = [ f for f in os.listdir('./Results/') if f.endswith('.txt') ] #Result File Names
    results = ParseResults(result_filenames)

    #ExperimentData.AnalyzeAll(results)
    #ExperimentData.RatingVsTimeSuccessive(results)
    #ExperimentData.RatingVsTimeByUser(results)
    #ExperimentData.RatingVsTime(results)
    #ExperimentData.RatingVsTimeSuccessiveBubble(results)
    #ExperimentData.RatingVsTimeSuccessiveScatter(results)

    #song_counts = ExperimentData.CountSongs(results)

    ExperimentData.AverageRatingPerSong(results['random'] + results['recommend'], 'All')
    ExperimentData.AverageRatingPerSong(results['random'], 'Random')
    ExperimentData.AverageRatingPerSong(results['recommend'], 'kALE')


    #ExperimentData.PlotAll(results)


print
main()
print
