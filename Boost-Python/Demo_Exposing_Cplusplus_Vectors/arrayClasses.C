// Demonstration/tutorial file copyright Craig Finch 2007.
// Released under the Boost Software License, which is available at
// http://www.boost.org/LICENSE_1_0.txt

#include <vector>
#include <ostream>
//#include <boost/python.hpp>   // if you include this, then you don't
// need to #include <boost/python/module.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/module.hpp>

// Class Declarations
class Node {
    public:
    float value;

    // Commented-out methods are not strictly necessary, but nice to
    // implement so that your object will act Pythonic

//    Node():value(0.0) {}
//    Node(float value):value(value) {}
//    float repr() const { return value; }
//    void reset() { value = 0.0; }
    bool operator==(Node const& n) const { return value == n.value; }
//    bool operator!=(Node const& n) const { return value != n.value; }
};

class Mesh {
    public:
    std::vector<Node> nodes;

    void printMesh (void);
};

// Class definitions
void Mesh::printMesh () {
    std::cout << nodes.size() << " nodes" << std::endl;
    for (int i=0; i<nodes.size(); i++) {
        std::cout << nodes[i].value << std::endl;
    }
}

using namespace boost::python;

// Boost.python definitions to expose classes to Python
BOOST_PYTHON_MODULE(arrayClasses) {
    class_<Node> ("Node")
        .def_readwrite("value", &Node::value)
    ;
    // Line below is necessary to expose the vector "nodes" to Python
    // and have it function as expected in Python
    class_< std::vector<Node> > ("nodeArray")
        .def(vector_indexing_suite< std::vector<Node> >())
    ;
    class_<Mesh> ("Mesh")
        .def_readwrite ("nodes", &Mesh::nodes)
        .def("printMesh", &Mesh::printMesh)
    ;
}
