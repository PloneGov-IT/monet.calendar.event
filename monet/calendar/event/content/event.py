"""Definition of the Event content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from monet.calendar.event import eventMessageFactory as _
from monet.calendar.event.interfaces import IEvent
from monet.calendar.event.config import PROJECTNAME

EventSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

EventSchema['title'].storage = atapi.AnnotationStorage()
EventSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(EventSchema, moveDiscussion=False)

class Event(base.ATCTContent):
    """Description of the Example Type"""
    implements(IEvent)

    meta_type = "Event"
    schema = EventSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Event, PROJECTNAME)
