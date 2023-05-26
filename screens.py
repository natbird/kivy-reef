from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import OptionProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget

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

class HomeScreen(Screen, EventDispatcher):
    screen_orientation = OptionProperty("horizontal", options=["vertical", "horizontal"])

    def __init__(self, **kwargs) -> None:
        super(HomeScreen, self).__init__(**kwargs)
        Window.bind(on_resize=self.getOrientation)
    
    def getOrientation(self, *wargs):
        if Window.height < Window.width:
            self.screen_orientation = 'horizontal'
        else:
            self.screen_orientation = 'vertical'

class SystemScreen(Screen, EventDispatcher):
    def __init__(self, **kwargs) -> None:
        super(SystemScreen, self).__init__(**kwargs)
        self.add_widget(SystemWidget(App.get_running_app().connection))

class LightsScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super(LightsScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=2, padding=10, spacing=10)
        self.add_widget(layout)
        if App.get_running_app().mqtt_connection:
            layout.add_widget(MqttWidget(App.get_running_app().mqtt_connection, App.get_running_app().config.get('mqtt', 'topic1'), App.get_running_app().config.get('mqtt', 'topic1_name')))

class WidgetScreen(Screen, EventDispatcher):
    layout = None
    screen_orientation = OptionProperty("None", options=["vertical", "horizontal", "None"])

    def __init__(self, **kwargs) -> None:
        super(WidgetScreen, self).__init__(**kwargs)
        
        Window.bind(on_resize=self.getOrientation)
        self.bind(screen_orientation=self.redo_layout)
        
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
    
    def getOrientation(self, *wargs):
        if Window.height < Window.width:
            self.screen_orientation = 'horizontal'
        else:
            self.screen_orientation = 'vertical'

    def redo_layout(self, *args):
        pass

class SensorsScreen(WidgetScreen):
    entities = None

    def __init__(self, **kwargs) -> None:
        self.getOrientation()
        if self.screen_orientation == 'horizontal':
            self.layout = GridLayout(cols=2, padding=10, spacing=10)
        else:
            self.layout = GridLayout(cols=1, padding=10, spacing=10)

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
    
    def redo_layout(self, *args):
        if self.screen_orientation == 'vertical':
            self.layout.cols=1
        else:
            self.layout.cols=2

class EquipmentScreen(WidgetScreen):
    layout = BoxLayout(orientation='vertical', padding=10)

    def __init__(self, **kwargs) -> None:
        self.entities = App.get_running_app().equipment_dict

        if self.entities:
            self.entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        super(EquipmentScreen, self).__init__(**kwargs)

class UsageScreen(WidgetScreen):
    entities = None

    def __init__(self, **kwargs) -> None:
        self.getOrientation()
        if self.screen_orientation == 'horizontal':
            self.layout = GridLayout(cols=3, padding=10, spacing=15)
        else:
            self.layout = GridLayout(cols=2, padding=10, spacing=15)

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
    
    def redo_layout(self, *args):
        if self.screen_orientation == 'vertical':
            self.layout.cols=2
        else:
            self.layout.cols=3

class MacrosScreen(WidgetScreen):
    layout = BoxLayout(orientation='vertical', padding=10)

    def __init__(self, **kwargs) -> None:
        self.entities = App.get_running_app().macro_dict
        if self.entities:
            self.entities.changedBind(self.recreateWidgets) # Bind the changed property to the recreateWidgets function
        super(MacrosScreen, self).__init__(**kwargs)
