junk = *.o analyze_MP3

COMPILER = g++
FLAGS = -g -std=c++11

MP3_FILE =

tools = ../../Software
chroma_directory = $(tools)/Chord-Detector-and-Chromagram
chroma_src_directory = $(chroma_directory)/src

fft_directory = $(chroma_directory)/libs/kiss_fft130

default: chromagram.o chord_detector.o analyze_MP3

chromagram.o: $(chroma_src_directory)/Chromagram.h
	$(COMPILER) $(FLAGS) -DUSE_KISS_FFT -c $(fft_directory)/kiss_fft.c $(chroma_src_directory)/Chromagram.cpp

chord_detector.o: $(chroma_src_directory)/ChordDetector.h
	$(COMPILER) $(FLAGS) -c $(chroma_src_directory)/ChordDetector.cpp

analyze_MP3: $(chroma_src_directory)/Chromagram.h $(chroma_src_directory)/ChordDetector.h
	$(COMPILER) $(FLAGS) $@.cpp -o $@

run:
	./analyze_MP3

clean:
	rm $(junk)
