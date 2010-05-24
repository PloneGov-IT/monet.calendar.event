from Products.CMFCore.utils import getToolByName

# Properties are defined here, because if they are defined in propertiestool.xml,
# all properties are re-set the their initial state if you reinstall product
# in the quickinstaller.

_PROPERTIES = [
    dict(name='event_types', type_='lines', value=()),
    ]

def import_various(context):
    if context.readDataFile('monet.calendar.event-various.txt') is None:
        return
    # Define portal properties
    site = context.getSite()
    ptool = getToolByName(site, 'portal_properties')
    props = ptool.monet_calendar_event_properties
    
    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])