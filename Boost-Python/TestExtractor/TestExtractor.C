#include <boost/python.hpp>
#include "boost/python/extract.hpp"
#include <iostream>

using namespace boost::python;

// Fill structures like this one with data from Python objects
struct dataStructure {
	public: dataStructure(int x) : v(x) {}

	public: int value() { return v; }
	
	private:
	int v;
};

// Class contains methods to interface with Python
class testClass {

	// Demonstrate extracting a derived object type that is built-in to Boost
	public: int getString(str s);

	// Demonstrate extracting a custom derived object type
	public: int getCustom(object x);

};

int testClass::getString(str s) { 
	// extract a C string from the Python string object
	char const* c_str = extract<char const*>(s);
	std::cout << c_str << std::endl;

	// Get the Python string's length and convert it to an int
	return extract<int>(s.attr("__len__")());
}

int testClass::getCustom(object x) {
	// Extract as a pointer
	dataStructure& dataPointer = extract<dataStructure&>(x);
	std::cout << dataPointer.value() << std::endl;

	// Works the same way if you extract it as an object
	dataStructure dataObject = extract<dataStructure>(x);
	std::cout << dataObject.value() << std::endl;

	return 0;
}

// Expose classes and methods to Python
BOOST_PYTHON_MODULE(TestExtractor) {
	class_<testClass> ("interfaceObject")
		.def("getString", &testClass::getString)
		.def("getCustom", &testClass::getCustom)
	;
	
	class_<dataStructure>("dataStructure", init<int>())
		.def("value", &dataStructure::value)
		;
}
