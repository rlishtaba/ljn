#coding:utf8

from functools import partial
from inspect import ismethod
from threading import Lock
from weakref import ref
import logging

log = logging.getLogger(__name__)

class BoundMethodRef(object):
    def __init__(self, method):
        self._func = method.im_func
        self._obj = ref(method.im_self)

    def __call__(self):
        obj = self._obj()
        if obj is None:
            return None
        return partial(self._func, obj)

class EventPublisher(object):
    def __init__(self, *args):
        self._lock = Lock()
        self._listeners = []

    def _purge(self):
        listeners = self._listeners
        for i in range(len(listeners) - 1, -1, -1):
            if listeners[i][1]() is None:
                del listeners[i]

    def connect(self, func, priority=100):
        with self._lock:
            for p, f in self._listeners:
                if f() == func:
                    return

            func = BoundMethodRef(func) if ismethod(func) else ref(func)

            self._listeners.append((priority, func))
            self._purge()
            self._listeners.sort(reverse=True)

    def disconnect(self, func):
        with self._lock:
            self._purge()

            for i in range(len(self._listeners)):
                if self._listeners[i][1]() == func:
                    del self._listeners[i]
                    return

    def emit(self, *args):
        with self._lock:
            listeners = self._listeners[:]

        for l in listeners:
            func = l[1]()
            if func is not None:
                try:
                    func(*args)
                except Exception:
                    log.exception('emit event to %s error!' % func)
