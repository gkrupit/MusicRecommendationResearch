#Demonstration/tutorial file copyright Craig Finch 2007.
#Released under the Boost Software License, which is available at
#http://www.boost.org/LICENSE_1_0.txt

import arrayClasses

# Create two nodes
n1 = arrayClasses.Node()
n1.value = 1.7

n2 = arrayClasses.Node()
n2.value = 2.4

# Create a mesh class that holds a vector of nodes
mesh = arrayClasses.Mesh()

# add the nodes to the vector, Python-style
mesh.nodes.append(n1)
mesh.nodes.append(n2)

# verify that node were added
print "From Python:"
print mesh.nodes[0].value
print mesh.nodes[1].value

# verify that we can access vector elements from C++
print "From C++:"
mesh.printMesh()
