junk = *.o *.so

COMPILER = g++
FLAGS = -g -std=c++11

tools =
chroma_directory = ..
chroma_src_directory = .
fft_directory = $(chroma_directory)/libs/kiss_fft130

# location of the Python header files
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)

# location of the Boost Python include files and library
BOOST_INC = /usr/local/Cellar/boost/1.61.0_1/include
BOOST_LIB = /usr/local/Cellar/boost-python/1.62.0/lib

MP3_FILE =

# Chromagram and ChordDetector classes
# TARGET = Chromagram ChordDetector

default: Chromagram.so ChordDetector.so

Chromagram.so: Chromagram.o
	$(COMPILER) $(FLAGS) -shared *.o -L$(BOOST_LIB) \
	  -lboost_python -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $@

ChordDetector.so: ChordDetector.o
	$(COMPILER) $(FLAGS) -shared ChordDetector.o -L$(BOOST_LIB) \
	  -lboost_python -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $@

Chromagram.o: Chromagram.h
	$(COMPILER) $(FLAGS) -c -DUSE_KISS_FFT $(fft_directory)/kiss_fft.c Chromagram.cpp -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC

ChordDetector.o: ChordDetector.h
	$(COMPILER) $(FLAGS) -c -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC ChordDetector.cpp

clean:
	rm $(junk)
