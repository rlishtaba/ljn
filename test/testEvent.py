#coding:utf8
from unittest.case import TestCase
from ljn.Event import EventPublisher

data = []

class A(object):
    def foo(self, a):
        data.append('a.foo %s' % a)

def f1(a):
    data.append('test1 %s' % a)

def f2(a):
    data.append('test2 %s' % a)

class EventTestCase(TestCase):
    def test(self):
        import logging
        logging.basicConfig()

        a = A()
        e = EventPublisher()
        e.connect(f1)
        e.connect(f2, 200)
        e.connect(a.foo)
        e.emit(5)
        self.assertEqual(data, ['test2 5', 'test1 5', 'a.foo 5'])
        del data[:]
        e.emit(6)
        self.assertEqual(data, ['test2 6', 'test1 6', 'a.foo 6'])
        del data[:]

        del a
        e.emit(7)
        self.assertEqual(data, ['test2 7', 'test1 7'])
        del data[:]
