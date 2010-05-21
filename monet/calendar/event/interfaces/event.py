from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from monet.calendar.event import eventMessageFactory as _

class IEvent(Interface):
    """Description of the Example Type"""
    
    # -*- schema definition goes here -*-
