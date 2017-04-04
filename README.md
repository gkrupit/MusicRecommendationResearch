# MusicRecommendation

This project is the basis for a content-based music recommendation algoritm that uses similar chord progression as a metric for song recommendation. (In the future, other content based metrics drawn from wavelet analysis will be used in addition to chord progression).

Overview of the content-based system:

1. For each MP3, determine the BPM, chord progression, chord historgram, and key. (In directory ChordAnalysis)

  1. BPM: algoritm is found here: https://github.com/scaperot/the-BPM-detector-python/blob/master/bpm_detection/bpm_detection.py
  
  2. Chord progression: https://github.com/adamstark/Chord-Detector-and-Chromagram, converted to Python 2.x using Boost-Python
  
    1. The initial chord progression is not very accurate, so using some basic music theory and assumptions about the accuracy of the chromagram/chord analysis of the mp3, correct some obvious mistakes (Some of this is in the directory CorrectProgression)
    
  1. Chord Histogram - Used as input data for machine learning (In directory MachineLearning)
  
  2. Key: Machine learning.  Once key is found, transpose chord progression to C for normalized comparison with other progressions.
  
2. Compare Chord Progressions (In directory CompareProgressions) using original distance measurement between chord progressions

  1. Distance 1: The distance between chord progressions is based on similarity of k-length subprogressions.  All consecutive k-length subprogressions in two songs are compared using the traditional Edit Distance algorithm (will be modified in the future for this application), where the minimum edit distance of 0 means the subprogression are identical, while the maximum edit distance of k means the progressions are completely distinct.
  
  2. Distance 2: Similar to Distance 1, the distance between chord progressions is based on similarity of k-length subprogressions.  In this distance measurement, only identical subprogressions are considered.  The individual chords in song A that are part of an identical subprogression in song B are recorded.  These chords are counted for each song, and the percentage of each song that are part of identical subprogressions in the other are determined.  The disance is currently implemented as the average of these percentages.    
