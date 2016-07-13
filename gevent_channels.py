# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from gevent import wait
from gevent.event import Event
from gevent.queue import Queue


class Channel:

    def __init__(self):
        self.event = Event
        self.event.channel = self
        self.queue = Queue(maxsize=1)

    def put(self, e):
        self.queue.put(e)
        self.event.set()


def channel_wait(channels, timeout=None):
    assert all(isinstance(channel, Channel) for channel in channels), "Can only wait on channels"
    event = wait([channel.queue for channel in channels], timeout, 1)
    if event:
        return event.channel.queue.get_no_wait()
