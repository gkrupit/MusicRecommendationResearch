char const* greet()
{
       return "hello, world";
}

int add2(int x, int y)
{
  return x + y;
}

#include <boost/python.hpp>

BOOST_PYTHON_MODULE(hello_ext)
{
      using namespace boost::python;
          def("greet", greet);

          def("add2", add2, int x, int y);
}
