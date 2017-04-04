//=======================================================================
/** @file Chromagram.h
 *  @brief Chromagram - a class for calculating the chromagram in real-time
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

#ifndef __CHROMAGRAM_H
#define __CHROMAGRAM_H

#define _USE_MATH_DEFINES
#include <math.h>
#include <vector>

#ifdef USE_FFTW
#include "fftw3.h"
#endif

#ifdef USE_KISS_FFT
#include "../libs/kiss_fft130/kiss_fft.h"
#endif

/* Include libraries for boost-python */
#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/stl_iterator.hpp>



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
/** A class for calculating a Chromagram from input audio
 * in a real-time context */
class Chromagram
{

public:
    /** Constructor
     * @param frameSize the input audio frame size
     * @param fs the sampling frequency
     */
    Chromagram (int frameSize, int fs);

    /** Destructor */
    ~Chromagram();

    /** Process a single audio frame. This will determine whether enough samples
     * have been accumulated and if so, will calculate the chromagram
     * @param inputAudioFrame an array containing the input audio frame. This should be
     * the length indicated by the input audio frame size passed to the constructor
     * @see setInputAudioFrameSize
     */
    //void processAudioFrame (double* inputAudioFrame);

    /** Process a single audio frame. This will determine whether enough samples
     * have been accumulated and if so, will calculate the chromagram
     * @param inputAudioFrame a vector containing the input audio frame. This should be
     * the length indicated by the input audio frame size passed to the constructor
     * @see setInputAudioFrameSize
     */
    void processAudioFrame (std::vector<double> inputAudioFrame);

    /** Sets the input audio frame size
     * @param frameSize the input audio frame size
     */
    void setInputAudioFrameSize (int frameSize);

    /** Set the sampling frequency of the input audio
     * @param fs the sampling frequency in Hz
     */
    void setSamplingFrequency (int fs);

    /** Set the interval at which the chromagram is calculated. As the algorithm requires
     * a significant amount of audio to be accumulated, it may be desirable to have the algorithm
     * not calculate the chromagram at every new audio frame. This function allows you to set the
     * interval at which the chromagram will be calculated, specified in the number of samples at
     * the audio sampling frequency
     * @param numSamples the number of samples that the algorithm will receive before calculating a new chromagram
     */
    void setChromaCalculationInterval (int numSamples);

    /** @returns the chromagram vector */
    std::vector<double> getChromagram();

    /** @returns true if a new chromagram vector has been calculated at the current iteration. This should
     * be called after processAudioFrame
     */
    bool isReady();

private:

    void setupFFT();
    void calculateChromagram();
    void calculateMagnitudeSpectrum();
	void downSampleFrame (std::vector<double> inputAudioFrame);
    void makeHammingWindow();
    double round (double val);

    std::vector<double> window;
    std::vector<double> buffer;
    std::vector<double> magnitudeSpectrum;
    std::vector<double> downsampledInputAudioFrame;
    std::vector<double> chromagram;

    double referenceFrequency;
    double noteFrequencies[12];

    int bufferSize;
    int samplingFrequency;
    int inputAudioFrameSize;
    int downSampledAudioFrameSize;
    int numHarmonics;
	int numOctaves;
	int numBinsToSearch;
    int numSamplesSinceLastCalculation;
    int chromaCalculationInterval;
    bool chromaReady;

#ifdef USE_FFTW
    fftw_plan p;
	fftw_complex* complexOut;
    fftw_complex* complexIn;
#endif

#ifdef USE_KISS_FFT
    kiss_fft_cfg cfg;
    kiss_fft_cpx* fftIn;
    kiss_fft_cpx* fftOut;
#endif

};

#endif /* defined(__CHROMAGRAM_H) */

BOOST_PYTHON_MODULE(Chromagram) {
  using namespace boost::python;

  // Register interable conversions.
    iterable_converter()
      // Build-in support for vector<double>/list conversion
      //.from_python<std::vector< std::vector<double> > >()
      .from_python<std::vector<double> >()
    ;


    class_<std::vector<double> >("vector<double>")
      .def(vector_indexing_suite<std::vector<double> >() );

  class_<Chromagram> ("Chromagram", init<int, int>())
    .def("processAudioFrame", &Chromagram::processAudioFrame)
    .def("setInputAudioFrameSize", &Chromagram::setInputAudioFrameSize)
    .def("setSamplingFrequency", &Chromagram::setSamplingFrequency)
    .def("setChromaCalculationInterval", &Chromagram::setChromaCalculationInterval)
    .def("getChromagram", &Chromagram::getChromagram)
    .def("isReady", &Chromagram::isReady)

  ;
}
