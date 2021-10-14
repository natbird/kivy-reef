from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

Builder.load_file("equipment.kv")

from entity import Entity, EntityDict

class EquipmentWidget(Entity):
    """ Equipment object """
    value = BooleanProperty(False)
    entity_type = 'equipment'
    update_interval = 10

    def __init__(self, id, name, state, c):
        super(EquipmentWidget, self).__init__(id, name, c)
        self.value = state
        self.update_timer.cancel()
    
    def postState(self, state):
        # Check whether the value has changed and if so post the new state to Reef-pi
        if self.value != state:
            self.connection.api_post(category='equipment', command='control', post_data=state, id=self.id)
            self.value = state

class EquipmentDict(EntityDict):
    """ A dictionary of equipment objects. Requires a reef-pi connection. """
    update_interval = 10 # Update the EquipmentDict every 10 seconds
    dict_type = "equipment"

    def __init__(self, c, **kwargs):
        super(EquipmentDict, self).__init__(c, **kwargs)
    
    def createItem(self, attributes, c):
        new_item = EquipmentWidget(attributes.get('id'), attributes.get('name'), attributes.get('state'), c)
        return new_item
