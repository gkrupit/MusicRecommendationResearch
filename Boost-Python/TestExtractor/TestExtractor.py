import TestExtractor

t = TestExtractor.interfaceObject()

strlen = t.getString("Python string")

print strlen

x = TestExtractor.dataStructure(18)
print x.value()

t.getCustom(x)

