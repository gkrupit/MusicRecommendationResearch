#include <vector>

#include "TestClass.h"

MyStack::MyStack() { }

MyStack::MyStack(std::vector<double> _values)
{
  values = _values;
}

void MyStack::set(std::vector<double> newValues)
{
  values = newValues;
}

double MyStack::top()
{
  return values.back();
}

void MyStack::push(double value)
{
  values.push_back(value);
}

double MyStack::pop()
{
  double top = this->top();
  values.pop_back();
  return top;
}

bool MyStack::empty()
{
  return values.empty();
}

int MyStack::size() { return values.size(); }
