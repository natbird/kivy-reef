from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

Builder.load_file("usage.kv")

from entity import Entity, EntityDict

class AtoWidget(Entity):
    """ ATO sensor widget """
    entity_type = 'ato'
    update_interval = 60
    usage_per_day = 24 # Number of usage entries which represent last 24 hours
    value = NumericProperty(0)

    def __init__(self, widget_id, widget_name, c):
        super(AtoWidget, self).__init__(widget_id, widget_name, c)
        self.update()

class AtoDict(EntityDict):
    """ A dictionary of ATO widgets """
    update_interval = 60
    dict_type = 'ato'

    def __init__(self, c):
        super(AtoDict, self).__init__(c)
    
    def createItem(self, attributes, c):
        new_item = AtoWidget(attributes.get('id'), attributes.get('name'), c)
        
        # Check whether ATO name is in the ignore list, if so do not create an ATO widget
        if new_item.name in App.get_running_app().config.get('usage', 'ato_ignore'):
            return False
        else:
            return new_item

class DoserWidget(Entity):
    """ Doser widget object """
    entity_type = 'doser'
    update_interval = 60
    usage_per_day = 1 # Number of usage entries which represent last 24 hours
    value = NumericProperty(0)

    def __init__(self, widget_id, widget_name, c):
        super(DoserWidget, self).__init__(widget_id, widget_name, c)
        self.update()

class DoserDict(EntityDict):
    """ A dictionary of doser objects """
    update_interval = 60
    dict_type = 'doser'

    def __init__(self, c):
        super(DoserDict, self).__init__(c)
        
    def createItem(self, attributes, c):
        new_item = DoserWidget(attributes.get('id'), attributes.get('name'), c)
        
        # Check whether Doser name is in the ignore list, if so do not create a Doser widget
        if new_item.name in App.get_running_app().config.get('usage', 'doser_ignore'):
            return False
        else:
            return new_item