#!/usr/bin/python
class Person:
    population = 0
    def __init__(self,name):
        self.name = name
        print '(Initializing %s)' % self.name
        Person.population += 1
    def __del__(self):
        print '%s says bye.' % self.name
        Person.population -= 1
        if Person.population == 0:
            print 'I am the last one.'
        else:
            print 'There are still %d people left. ' % Person.population
    def sayHi(self):
        print 'Hi, my name is %s' % self.name
    def howMany(self):
        if Person.population == 1:
            print 'I am the only person here.'
        else:
            print 'We have %d persons here.' % Person.population
swaroop = Person('Swaroop')
swaroop.sayHi()
swaroop.howMany()
kalam = Person('Abdul Kalam')
kalam.sayHi()
kalam.howMany()
swaroop.sayHi()
swaroop.howMany()
