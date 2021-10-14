from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

Builder.load_file("sensors.kv")

from entity import Entity, EntityDict

class TempWidget(Entity):
    """ Temperature controller object """
    value = NumericProperty(0)
    fahrenheit = BooleanProperty(False)
    update_interval = 30
    entity_type = 'temperature'

    def __init__(self, widget_id, widget_name, fahrenheit, c):
        super(TempWidget, self).__init__(widget_id, widget_name, c)
        self.farenheit = fahrenheit
        self.update()

class TempDict(EntityDict):
    """ A dictionary of temperature controller objects """
    update_interval = 60
    dict_type = 'temperature'

    def __init__(self, c):
        super(TempDict, self).__init__(c)
    
    def createItem(self, attributes, c):
        new_item = TempWidget(attributes.get('id'), attributes.get('name'), attributes.get('fahrenheit'), c)
        return new_item

class PhWidget(Entity):
    """ pH probe object """
    value = NumericProperty(0)
    update_interval = 60
    entity_type = 'ph'
    flow_meter = BooleanProperty(False)

    def __init__(self, widget_id, widget_name, c):
        super(PhWidget, self).__init__(widget_id, widget_name, c)
        # Check whether the pH entity is actually a flow meter
        if App.get_running_app().config.get('sensors', 'flowmeter_name') in self.name:
            self.flow_meter = True
        self.update()
    
class PhDict(EntityDict):
    """ A dictionary of pH probe objects """
    update_interval = 60
    dict_type = 'ph'

    def __init__(self, c):
        super(PhDict, self).__init__(c)
    
    def createItem(self, attributes, c):
        new_item = PhWidget(attributes.get('id'), attributes.get('name'), c)
        return new_item
