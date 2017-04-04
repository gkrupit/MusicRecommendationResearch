//=======================================================================
/** @file ChordDetector.h
 *  @brief ChordDetector - a class for estimating chord labels from chromagram input
 *  @author Adam Stark
 *  @copyright Copyright (C) 2008-2014  Queen Mary University of London
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
//=======================================================================

#ifndef CHORDDETECT_H
#define CHORDDETECT_H

#include <vector>

/* Include libraries for boost-python */
#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/stl_iterator.hpp>

/*
PyObject* PyInit_AudioAnalyzer(void)
{

}*/

//http://stackoverflow.com/questions/15842126/feeding-a-python-list-into-a-function-taking-in-a-vector-with-boost-python
/// @brief Type that allows for registration of conversions from
///        python iterable types.
struct iterable_converter
{
  /// @note Registers converter from a python interable type to the
  ///       provided type.
  template <typename Container>
  iterable_converter&
  from_python()
  {
    boost::python::converter::registry::push_back(
      &iterable_converter::convertible,
      &iterable_converter::construct<Container>,
      boost::python::type_id<Container>());

    // Support chaining.
    return *this;
  }
/*
  to_python()
  {
    boost::python::converter::registry::push_back(
      &iterable_converter::convertible,
      boost::python::type_id<Container>(),
      &iterable_converter::construct<Container>);
  }

  template<class T>
  boost::python::list std_vector_to_py_list(const std::vector<T>& v)
  {
      boost::python::object get_iter = boost::python::iterator<std::vector<T> >();
      boost::python::object iter = get_iter(v);
      boost::python::list l(iter);
      return l;
  }
*/


  /// @brief Check if PyObject is iterable.
  static void* convertible(PyObject* object)
  {
    return PyObject_GetIter(object) ? object : NULL;
  }

  /// @brief Convert iterable PyObject to C++ container type.
  ///
  /// Container Concept requirements:
  ///
  ///   * Container::value_type is CopyConstructable.
  ///   * Container can be constructed and populated with two iterators.
  ///     I.e. Container(begin, end)
  template <typename Container>
  static void construct(
    PyObject* object,
    boost::python::converter::rvalue_from_python_stage1_data* data)
  {
    namespace python = boost::python;
    // Object is a borrowed reference, so create a handle indicting it is
    // borrowed for proper reference counting.
    python::handle<> handle(python::borrowed(object));

    // Obtain a handle to the memory block that the converter has allocated
    // for the C++ type.
    typedef python::converter::rvalue_from_python_storage<Container>
                                                                storage_type;
    void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;

    typedef python::stl_input_iterator<typename Container::value_type>
                                                                    iterator;

    // Allocate the C++ type into the converter's memory block, and assign
    // its handle to the converter's convertible variable.  The C++
    // container is populated by passing the begin and end iterators of
    // the python object to the container's constructor.
    new (storage) Container(
      iterator(python::object(handle)), // begin
      iterator());                      // end
    data->convertible = storage;
  }
};


//=======================================================================
/** A class for estimating chord labels from chromagram input */
class ChordDetector
{
public:

    /** An enum describing the chord qualities used in the algorithm */
    enum ChordQuality
    {
        Minor,
        Major,
        Suspended,
        Dominant,
        Dimished5th,
        Augmented5th
    };

	/** Constructor */
	ChordDetector();

    /** Detects the chord from a chromagram. This is the vector interface
     * @param chroma a vector of length 12 containing the chromagram
     */
    void detectChord (std::vector<double> chroma);

    /** Detects the chord from a chromagram. This is the array interface
     * @param chroma an array of length 12 containing the chromagram
     */

    /** The root note of the detected chord */
	int rootNote;

    /** The quality of the detected chord (Major, Minor, etc) */
	int quality;

    /** Any other intervals that describe the chord, e.g. 7th */
	int intervals;

private:
  void detectChordPointer (double* chroma);
	void makeChordProfiles();
	void classifyChromagram();
	double calculateChordScore (double* chroma, double* chordProfile, double biasToUse, double N);
	int minimumIndex (double*array, int length);

	double chromagram[12];
	double chordProfiles[108][12];
	double chord[108];
	double bias;
};

#endif



BOOST_PYTHON_MODULE(ChordDetector) {
  using namespace boost::python;

  class_<ChordDetector>("ChordDetector")
    .def("detectChord", &ChordDetector::detectChord)
    .def_readwrite("rootNote", &ChordDetector::rootNote)
    .def_readwrite("quality", &ChordDetector::quality)
    .def_readwrite("intervals", &ChordDetector::intervals)
  ;
}
