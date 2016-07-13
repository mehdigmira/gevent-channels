# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from gevent import wait
from gevent.event import Event
from gevent.queue import Queue


class Channel:
    def __init__(self):
        self.event = Event()
        self.event.channel = self
        self.queue = Queue(maxsize=1)

    def put(self, e):
        self.queue.put(e)
        self.event.set()


def channel_wait(channels, timeout=None):
    assert all(isinstance(channel, Channel) for channel in channels), "Can only wait on channels"
    event = wait([channel.event for channel in channels], timeout, 1)
    if event:
        val = event[0].channel.queue.get_nowait()
        event[0].clear()
        return val, event[0].channel


if __name__ == "__main__":
    from gevent import sleep, spawn, joinall

    hey, hola = Channel(), Channel()


    def g():
        for i in range(100):
            msg, channel = channel_wait([hey, hola])
            if channel == hey:
                print 'hey %s' % msg
            else:
                print 'hola %s' % msg
            sleep(5)


    def f():
        for i in range(100):
            if i % 3 == 1:
                hey.put(i)
                print 'put %s in hey' % i
            else:
                hola.put(i)
                print 'put %s in hola' % i


    g_f = spawn(f)
    g_g = spawn(g)
    joinall([g_f, g_g])
