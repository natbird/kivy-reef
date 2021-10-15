from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

Builder.load_file("macros.kv")

from entity import Entity, EntityDict

class MacroWidget(Entity):
    """ Macro widget object """
    entity_type = 'macro'
    update_interval = 60
    reversible = BooleanProperty(False)

    def __init__(self, widget_id, widget_name, reversible, c):
        super(MacroWidget, self).__init__(widget_id, widget_name, c)
        self.reversible = reversible
        self.update_timer.cancel() # Cancel the update timer since nothing to update
    
    def run(self):
        # Run the macro
        self.connection.api_post(category='macro', command='run', id=self.id)
    
    def revert(self):
        # Revert the macro
        if self.reversible:
            self.connection.api_post(category='macro', command='revert', id=self.id)

class MacroDict(EntityDict):
    """ A dictionary of macro objects """
    update_interval = 60
    dict_type = 'macro'

    def __init__(self, c):
        super(MacroDict, self).__init__(c)
        
    def createItem(self, attributes, c):
        new_item = MacroWidget(attributes.get('id'), attributes.get('name'), attributes.get('reversible'), c)
        return new_item