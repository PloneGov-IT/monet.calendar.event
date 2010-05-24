"""Definition of the Event content type
"""

from zope.interface import implements #, directlyProvides

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.atapi import *

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from monet.calendar.event import eventMessageFactory as _
from monet.calendar.event.interfaces import IEvent
from monet.calendar.event.config import PROJECTNAME

from monet.recurring_event.content.event import EventSchema as RecurringEventSchema
from monet.recurring_event.content.event import RecurringEvent

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DisplayList
from Products.ATContentTypes.content.image import ATImageSchema
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform

EventSchema = RecurringEventSchema.copy() + Schema((

    LinesField('eventType',
               required=False,
               searchable=True,
               languageIndependent=True,
               vocabulary='getEventTypeVocab',
               widget = MultiSelectionWidget(
                        format = 'checkbox',
                        description='',
                        label = _(u'label_event_type', default=u'Event Type(s)')
                        )),
    
    StringField('slots',
                required=False,
                searchable=False,
                languageIndependent=True,
                vocabulary='getSlotsVocab',
                widget=SelectionWidget(
                        format = 'select',
                        label = _(u'label_slots', default=u'Time slots')
                        )),
                        
    StringField('cost',
                required=False,
                searchable=False,
                widget=StringWidget(
                        label = _(u'label_cost', default=u'Cost')
                        )),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

EventSchema['title'].storage = AnnotationStorage()
EventSchema['description'].storage = AnnotationStorage()

schemata.finalizeATCTSchema(EventSchema, moveDiscussion=False)

EventSchema.moveField('eventType', after='description')

imageField = ATImageSchema['image'].copy()
imageField.required = False
imageField.primary = False
imageField.validators = None
EventSchema.addField(imageField)
EventSchema.moveField('image', after='eventType')

EventSchema.moveField('startDate', after='image')
EventSchema.moveField('endDate', after='startDate')

EventSchema.moveField('slots', before='text')
EventSchema['text'].widget.label = _(u'label_time', default=u'Time')
EventSchema.moveField('cost', after='text')

class MonetEvent(RecurringEvent,ATCTImageTransform):
    """Description of the Example Type"""
    implements(IEvent)

    meta_type = "ATEvent"
    schema = EventSchema

    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    
    def getEventTypeVocab(self):
        mp = getToolByName(self,'portal_properties')
        items = mp.monet_calendar_event_properties.event_types
        vocab = DisplayList()
        for item in items:
            vocab.add(item,item)
        return vocab
    
    def getSlotsVocab(self):
        vocab = DisplayList()
        vocab.add('morning',_(u'Morning'))
        vocab.add('afternoon',_(u'Afternoon'))
        vocab.add('night',_(u'Night'))
        vocab.add('allday',_(u'All day'))
        return vocab

registerType(MonetEvent, PROJECTNAME)
