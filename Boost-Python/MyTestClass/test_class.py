from TestClass import MyStack

############################################
print "Using vector constructor..."

stack = MyStack()

stack.push(3.2)
stack.push(3.1)
stack.push(3)

while not stack.empty():
    print stack.pop()
###########################################

###########################################
print "Using vector constructor..."

lst = [1,2,1.3]
stack.set(lst)

if stack.empty():
    print "Stack is already empty. Won't enter loop"
else:
    print "Stack isn't empty. Popping values."
while not stack.empty():
    print stack.pop()
###########################################
