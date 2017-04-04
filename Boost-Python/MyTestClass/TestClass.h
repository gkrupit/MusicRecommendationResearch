#include <iostream>
#include <vector>

#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/stl_iterator.hpp>


//http://stackoverflow.com/questions/15842126/feeding-a-python-list-into-a-function-taking-in-a-vector-with-boost-python
namespace py = boost::python;
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

static struct PyModuleDef TestClassModuleDef =
{
    PyModuleDef_HEAD_INIT,
    "TestClass", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    TestClassModule_methods
};

PyMODINIT_FUNC PyInit_exmod(void) {
    return PyModule_Create(&fizzbuzzModuleDef);
}

class MyStack
{
  public:
    MyStack();
    MyStack(std::vector<double> _values);
    void set(std::vector<double> newValues);
    double top();
    void push(double value);
    double pop();
    bool empty();
    int size();


  private:
    std::vector<double> values;
};


using namespace boost::python;

BOOST_PYTHON_MODULE(TestClass) {

  // Register interable conversions.
    iterable_converter()
      // Build-in type.
      .from_python<std::vector<double> >()
      .from_python<std::vector< std::vector<double> > >()
      // Each dimension needs to be convertable.
      .from_python<std::vector<std::string> >()
      .from_python<std::vector<std::vector<std::string> > >()
      // User type.
      //.from_python<std::list<foo> >()
      ;

  class_<MyStack> ("MyStack")
    //.def("MyStack", init< std::vector<double> >())
    .def("set", &MyStack::set)
    .def("top", &MyStack::top)
    .def("push", &MyStack::push)
    .def("pop", &MyStack::pop)
    .def("empty", &MyStack::empty)
    .def("size", &MyStack::size)
  ;

}
