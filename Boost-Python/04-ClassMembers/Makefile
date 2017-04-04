# location of the Python header files

PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)

# location of the Boost Python include files and library

#BOOST_INC = /usr/include
BOOST_INC = /usr/local/Cellar/boost/1.61.0_1/include
BOOST_LIB = /usr/local/Cellar/boost-python/1.62.0/lib

# compile mesh classes
TARGET = member

$(TARGET).so: $(TARGET).o
	g++ -shared $(TARGET).o -L$(BOOST_LIB) -lboost_python -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET).so

$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp

clean:
	rm *.o *.so
