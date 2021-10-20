from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from system import SystemWidget
from mqtt import MqttWidget

Builder.load_file("screens.kv")

def ScreenMaker(widget_screen_type, name):
    if widget_screen_type == 'Home':
        new_screen = HomeScreen(name=name)
    if widget_screen_type == 'Sensors':
        new_screen = SensorsScreen(name=name)
    elif widget_screen_type == 'Equipment':
        new_screen = EquipmentScreen(name=name)
    elif widget_screen_type == 'Lights':
        new_screen = LightsScreen(name=name)
    elif widget_screen_type == 'Usage':
        new_screen = UsageScreen(name=name)
    elif widget_screen_type == 'Macros':
        new_screen = MacrosScreen(name=name)
    elif widget_screen_type == 'System':
        new_screen = SystemScreen(name=name)
    
    return new_screen

class HomeScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super(HomeScreen, self).__init__(**kwargs)

class SystemScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super(SystemScreen, self).__init__(**kwargs)
        self.add_widget(SystemWidget(App.get_running_app().connection))

class LightsScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super(LightsScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=3, padding=20, spacing=30)
        self.add_widget(layout)
        if App.get_running_app().mqtt_connection:
            layout.add_widget(MqttWidget(App.get_running_app().mqtt_connection, App.get_running_app().config.get('mqtt', 'topic1'), App.get_running_app().config.get('mqtt', 'topic1_name')))

class WidgetScreen(Screen):
    layout = None

    def __init__(self, **kwargs) -> None:
        super(WidgetScreen, self).__init__(**kwargs)
        self.add_widget(self.layout)
        
        if self.entities:
            self.createWidgets()

    def createWidgets(self):
        for item in self.entities:
            self.layout.add_widget(item)
    
    def recreateWidgets(self, instance=None):
        self.layout.clear_widgets()
        self.createWidgets()
        self.entities.changed = False

class SensorsScreen(WidgetScreen):
    layout = GridLayout(cols=2, padding=20, spacing=30)
    entities = None

    def __init__(self, **kwargs) -> None:
        self.temp_entities = App.get_running_app().tc_dict
        if self.temp_entities:
            self.temp_entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        
        self.ph_entities = App.get_running_app().ph_dict
        if self.ph_entities:
            self.ph_entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function

        if self.temp_entities or self.ph_entities:
            self.entities = 1
        super(SensorsScreen, self).__init__(**kwargs)
        
    def createWidgets(self):
        if self.temp_entities:
            for item in self.temp_entities:
                self.layout.add_widget(item)
        
        if self.ph_entities:
            for item in self.ph_entities:
                self.layout.add_widget(item)
    
    def recreateWidgets(self):
        self.layout.clear_widgets()
        self.createWidgets()
        self.temp_entities.changed = False
        self.ph_entities.changed = False

class EquipmentScreen(WidgetScreen):
    layout = BoxLayout(orientation='vertical')

    def __init__(self, **kwargs) -> None:
        self.entities = App.get_running_app().equipment_dict

        if self.entities:
            self.entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        super(EquipmentScreen, self).__init__(**kwargs)

class UsageScreen(WidgetScreen):
    layout = GridLayout(cols=4)
    entities = None

    def __init__(self, **kwargs) -> None:
        self.ato_entities = App.get_running_app().ato_dict
        if self.ato_entities:
            self.ato_entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        
        self.doser_entities = App.get_running_app().doser_dict
        if self.doser_entities:
            self.doser_entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        
        if self.ato_entities or self.doser_entities:
            self.entities = 1
        super(UsageScreen, self).__init__(**kwargs)
        
    def createWidgets(self):
        if self.ato_entities:
            for item in self.ato_entities:
                self.layout.add_widget(item)

        if self.doser_entities:
            for item in self.doser_entities:
                self.layout.add_widget(item)
    
    def recreateWidgets(self):
        self.layout.clear_widgets()
        self.createWidgets()
        self.ato_entities.changed = False
        self.doser_entities.changed = False

class MacrosScreen(WidgetScreen):
    layout = BoxLayout(orientation='vertical')

    def __init__(self, **kwargs) -> None:
        self.entities = App.get_running_app().macro_dict
        if self.entities:
            self.entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        super(MacrosScreen, self).__init__(**kwargs)
