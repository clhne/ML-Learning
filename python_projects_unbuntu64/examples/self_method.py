#!/usr/bin/python
#coding=utf-8
#实例类方法需要添加self,self在python中不是关键字，它代表当前对象的地址，能避免非限定调用造成的全局变量
class test(object):
    def add(self, a, b):
        print (a + b)
    def display(self):
        print 'hello'
test = test()
test.add(1, 3)
test.display()

#普通方法不需要添加self
def addtwo(a, b):
    print a+b
print addtwo(1, 2)
