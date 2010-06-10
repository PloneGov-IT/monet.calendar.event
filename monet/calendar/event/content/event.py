"""Definition of the Event content type
"""

from zope.interface import implements #, directlyProvides

try:
    # turn off
    from Products.LinguaPloneXXX.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.atapi import *

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from monet.calendar.event import eventMessageFactory as _
from monet.calendar.event.interfaces import IMonetEvent, IMonetCalendar
from monet.calendar.event.config import PROJECTNAME

from monet.recurring_event.content.event import EventSchema as RecurringEventSchema
from monet.recurring_event.content.event import RecurringEvent

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DisplayList
from Products.ATContentTypes.content.image import ATImageSchema
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform
from Products.ATContentTypes.permission import ChangeEvents
from Products.ATContentTypes.configuration import zconf
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View

EventSchema = RecurringEventSchema.copy() + Schema((

    LinesField('eventType',
               required=False,
               searchable=True,
               languageIndependent=True,
               vocabulary='getEventTypeVocab',
               widget = MultiSelectionWidget(
                        format = 'checkbox',
                        label = _(u'label_event_type', default=u'Event Type(s)')
                        )),
    
    StringField('slots',
                required=False,
                searchable=False,
                languageIndependent=True,
                vocabulary='getSlotsVocab',
                widget=SelectionWidget(
                        format = 'select',
                        label = _(u'label_slots', default=u'Time slots'),
                        description = _(u'help_slots', default=u'Select the time slot of the day on which the event takes place.')
                        )),
                        
    TextField('time',
              required=False,
              searchable=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              default_output_type = 'text/x-html-safe',
              widget = RichWidget(
                        label = _(u'label_time', default=u'Hours'),
                        description = _(u'help_time', default=u'Add time details.'),
                        rows = 25,
                        allow_file_upload = zconf.ATDocument.allow_document_upload
                        )),
                        
    TextField('cost',
                required=False,
                searchable=False,
                widget=TextAreaWidget(
                        label = _(u'label_cost', default=u'Entrance free'),
                        description = _(u'help_cost', default=u'Add details about the cost of the event.'),
                        )),
    
    TextField('location',
               required=False,
               searchable=False,
               write_permission = ChangeEvents,
               widget=TextAreaWidget(
                        label = _(u'label_location', default=u'Where'),
                        )),       
    
    StringField('address',
                required=False,
                searchable=False,
                languageIndependent=True,
                widget=StringWidget(
                        label = _(u'label_address', default=u'Address'),
                        size=80
                        )),
                        
    StringField('country',
                required=False,
                searchable=False,
                languageIndependent=True,
                widget=StringWidget(
                        label = _(u'label_country', default=u'Nation'),
                        size=40
                        )),
                        
    StringField('zipcode',
                required=False,
                searchable=False,
                languageIndependent=True,
                validators=("isInt"),
                widget=StringWidget(
                        label = _(u'label_zipcode', default=u'ZIP code'),
                        size=20
                        )),
                        
    StringField('fax',
                required=False,
                searchable=False,
                languageIndependent=True,
                widget=StringWidget(
                        label = _(u'label_fax', default=u'Contact Fax'),
                        size=50
                        )),
  
    LinesField('referenceEntities',
               required=False,
               searchable=False,
               widget=LinesWidget(
                        label = _(u'label_referenceentities', default=u'Reference entities'),
                        description = _(u'help_referenceentities', default=u'In this field you can specify the reference entities, one after another.')
                        )),
                        
    TextField('annotations',
              required=False,
              searchable=False,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              default_output_type = 'text/x-html-safe',
              widget = RichWidget(
                        label = _(u'label_annotations', default=u'Annotations'),
                        description = _(u'help_annotations', default=u'Enter here your notes about the event.'),
                        allow_file_upload = zconf.ATDocument.allow_document_upload
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
imageField.widget.description = _(u'help_event_image',default=u'Insert an image that represents the event.')
EventSchema.addField(imageField)
EventSchema.moveField('image', after='eventType')

EventSchema['startDate'].widget.show_hm = False
EventSchema['startDate'].widget.label= _(u'label_startDate',default=u'From')
EventSchema['endDate'].widget.show_hm = False
EventSchema['endDate'].widget.label= _(u'label_endDate',default=u'To')
EventSchema.moveField('startDate', after='image')
EventSchema.moveField('endDate', after='startDate')

EventSchema.moveField('cadence', after='endDate')
EventSchema.moveField('except', after='cadence')

EventSchema.moveField('slots', after='except')
EventSchema.moveField('time', after='slots')
EventSchema.moveField('cost', after='time')

EventSchema['location'].widget.description = _(u'help_location',default=u'Enter the event location.')
EventSchema.changeSchemataForField('location', 'default')
EventSchema.moveField('location', after='cost')
EventSchema.moveField('address', after='location')
EventSchema.moveField('country', after='address')
EventSchema.moveField('zipcode', after='country')

EventSchema['contactPhone'].widget.size=50
EventSchema['contactPhone'].languageIndependent=True,
EventSchema.moveField('contactPhone', after='zipcode')

EventSchema.moveField('fax', after='contactPhone')

EventSchema['eventUrl'].widget.size=60
EventSchema['eventUrl'].widget.description=''
EventSchema['eventUrl'].languageIndependent=True,
EventSchema.moveField('eventUrl', after='fax')

EventSchema['contactEmail'].widget.size=40
EventSchema['contactEmail'].languageIndependent=True,
EventSchema.moveField('contactEmail', after='eventUrl')

EventSchema.moveField('text', after='contactEmail')

EventSchema.moveField('referenceEntities', after='text')
EventSchema.moveField('annotations', after='referenceEntities')

EventSchema['attendees'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
EventSchema['contactName'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}

class MonetEvent(RecurringEvent, ATCTImageTransform):
    """Description of the Example Type"""
    implements(IMonetEvent,IMonetCalendar)

    meta_type = "ATEvent"
    schema = EventSchema

    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    
    security = ClassSecurityInfo()
    
    def getEventTypeVocab(self):
        mp = getToolByName(self,'portal_properties')
        items = mp.monet_calendar_event_properties.event_types
        vocab = DisplayList()
        for item in items:
            vocab.add(item,_(item))
        return vocab
    
    def getSlotsVocab(self):
        vocab = DisplayList()
        vocab.add('morning',_(u'Morning'))
        vocab.add('afternoon',_(u'Afternoon'))
        vocab.add('night',_(u'Evening'))
        vocab.add('allday',_(u'All day long'))
        return vocab
    
    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                scalename.replace(".jpg", "")
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return base.ATCTContent.__bobo_traverse__(self, REQUEST, name)

registerType(MonetEvent, PROJECTNAME)
