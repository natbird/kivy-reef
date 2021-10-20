from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

class Entity(Widget):
    """ Base entity for reef-pi entities to inherit """
    id = NumericProperty(0)
    name = StringProperty('')
    update_interval = 0

    def __init__(self, widget_id, widget_name, c):
        super(Entity, self).__init__()
        self.id = widget_id
        self.name = widget_name
        self.connection = c
        self.update_timer = Clock.schedule_interval(self.update, self.update_interval)
    
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def update(self, dt=None):
        new_value = False

        if self.entity_type == 'temperature':
            new_value = self.___update_reading()
        elif self.entity_type == 'ph':
            new_value = self.___update_reading()
        elif self.entity_type == 'equipment':
            new_value = self.___update_state()
        elif self.entity_type == 'ato':
            new_value = self.___update_usage()
        elif self.entity_type == 'doser':
            new_value = self.___update_usage()
        else:
            print("Entity type does not support update method.")
        
        if new_value:
            self.value = new_value

    def ___update_reading(self):
        new_reading = self.connection.read_query(category=self.entity_type, id=self.id)
        
        if new_reading:
            return new_reading
    
    def ___update_state(self):
        new_reading = self.connection.state_query(category=self.entity_type, id=self.id)
        
        if new_reading:
            return new_reading
    
    def ___update_usage(self):
        """ Return usage in the last 24 hours """
        new_reading = self.connection.usage_query(category=self.entity_type, id=self.id)
        
        if new_reading:
            usage = 0
            slice = int(self.usage_per_day * -1)
            data = list(new_reading.get('historical'))[slice:]
            for entry in data:
                usage += entry.get('pump')
            return usage

class EntityDict(EventDispatcher):
    """ A dictionary of objects """
    changed = BooleanProperty(False)
    dict_type='' # To be overridden by inherited classes
    update_interval=60 # Default update interval

    def __init__(self, c, **kwargs):
        super(EntityDict, self).__init__(**kwargs)
        self.connection = c
        self.items = {} # The dictionary of entity objects

        self.populateDict() # Populate the dictionary by creating entity objects

        self.update_timer = Clock.schedule_interval(self.updateDict, self.update_interval)

    def ___buildAttributes(self, item):
        """ Takes the result of an API query and returns a dictionary of relevant attributes """
        
        attributes = {
            'id' : int(item['id']),
            'name' : item['name']
        }

        if self.dict_type == 'temperature':
            attributes.update({'fahrenheit' : item['fahrenheit']})
        elif self.dict_type == 'equipment':
            attributes.update({'state' : item['state']})
        elif self.dict_type == 'ato':
            attributes.update({'enabled' : item['enabled'], 'period' : item['period']})
        elif self.dict_type == 'macro':
            attributes.update({'reversible' : item['reversible']})
        
        return attributes
    
    def __len__(self):
        """ Return the number of key:value pairs in the list """
        return len(self.items)

    def __iter__(self):
        """ Iterate through the values of the dictionary """
        for item in self.items.values():
            yield item

    def addItem(self, id, item):
        """ Add a new entity object to the dictionary """
        self.items.update({id : item})
    
    def changedBind(self, callback):
        """ Bind the dictionary changed property to a given function"""
        self.bind(changed=callback)
    
    def createItem(self, *args):
        """ Creates a widget entity for adding to the dictionary. To be implemented by child classes. """
        pass

    def delItem(self, id):
        """ Delete an object from the dictionary """
        self.items.pop(id)
        print(f"Item: {id} removed.")
    
    def getItem(self, id):
        """ Return an entity object by its Reef-pi id number """
        return self.items.get(id)
    
    def populateDict(self):
        """ Creates initial entities and populates the EntityDict """
        query_list = self.connection.list_query(self.dict_type)
        
        if query_list:
            for item in query_list:
                attributes = self.___buildAttributes(item)
                new_item = self.createItem(attributes, self.connection)
                if new_item:
                    self.addItem(attributes.get('id'), new_item)
    
    def updateDict(self, dt):
        """ Refresh the list of items from Reef-pi and update the dictionary """
        query_list = self.connection.list_query(self.dict_type)
        ids = []

        if query_list:
            for item in query_list:
                attributes = self.___buildAttributes(item)

                # Check if the item is new and, if so, create a new widget and set changed to True.
                if attributes.get('id') not in self.items.keys():
                    new_item = self.createItem(attributes, self.connection)
                    if new_item:
                        self.addItem(attributes.get('id'), new_item)
                        self.changed = True
                else:
                    # For equipment items, update the current state of all existing items
                    if self.dict_type == 'equipment':
                        self.getItem(attributes.get('id')).value = attributes.get('state')
                    
                    # For Ato items, update the current state of all existing items
                    if self.dict_type == 'ato':
                        self.getItem(attributes.get('id')).enabled = attributes.get('enabled')
                    
                    # For macro items, update the current state of all existing items
                    if self.dict_type == 'macro':
                        self.getItem(attributes.get('id')).reversible = attributes.get('reversible')
                
                ids.append(attributes.get('id'))
        
        # Check whether any items removed on Reef-pi side and, if so, delete from the EntityDict
        removed = set(self.items.keys()) - set(ids)
        if removed:
            for id in removed:
                self.delItem(id)
            self.changed = True
