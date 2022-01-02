import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition

from api import ApiConnection
from screens import ScreenMaker
from sensors import TempDict, PhDict
from equipment import EquipmentDict
from usage import AtoDict, DoserDict
from macros import MacroDict
from mqtt import MqttConnection

class MyScreenManager(ScreenManager):

    screen_list = [
        'Home', 'Sensors', 'Equipment', 'Lights', 'Usage', 'Macros', 'System'
    ]

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.transition = NoTransition()
        self.addScreens()

    def addScreens(self):
        for screen in self.screen_list:
            new_screen = ScreenMaker(str(screen),str(screen))
            self.add_widget(new_screen)

class TopBar(GridLayout):
    pass

class StatusBar(BoxLayout):
    pass

class MainWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        
        self.top_bar = TopBar()
        self.add_widget(self.top_bar)
        
        self.sm = MyScreenManager()
        self.add_widget(self.sm)

        self.status_bar = StatusBar()
        self.add_widget(self.status_bar)

        App.get_running_app().displayed_screen = self.sm.current

    def goScreen(self, instance, screen):
        self.sm.current = screen
        App.get_running_app().displayed_screen = self.sm.current
    
    def nextScreen(self, instance):
        self.sm.current = str(self.sm.next())
        App.get_running_app().displayed_screen = self.sm.current
    
    def prevScreen(self, instance):
        self.sm.current = str(self.sm.previous())
        App.get_running_app().displayed_screen = self.sm.current

class KivyReefApp(App):
    connection = ObjectProperty(None)
    mqtt_connection = ObjectProperty(None)
    reconnect_timer = ObjectProperty(None)
    connected = BooleanProperty(False)
    status = StringProperty('')
    displayed_screen = StringProperty('')
    
    reefpi_version = StringProperty('')
    cpu_temp = StringProperty('')
    
    tc_dict = ObjectProperty(None)
    equipment_dict = ObjectProperty(None)
    ph_dict = ObjectProperty(None)
    ato_dict = ObjectProperty(None)
    inlet_dict = ObjectProperty(None)
    macro_dict = ObjectProperty(None)
    doser_dict = ObjectProperty(None)

    use_kivy_settings = True

    def build_config(self, config):
        config.setdefaults('display', {
            'orientation': 'vertical'
        })
        config.setdefaults('server', {
            'host': 'http://127.0.0.1',
            'user_name': 'reef-pi',
            'password': 'reef-pi',
            'timeout': 5,
            'reconnect_interval': 30
        })
        config.setdefaults('admin', {
            'allow_reload' : 'true',
            'allow_restart' : 'true',
            'allow_poweroff' : 'true'
        })
        config.setdefaults('home', {
            'show_cpu_temp' : 'true',
            'show_version' : 'true'
        })
        config.setdefaults('sensors', {
            'flowmeter_name' : 'flow',
            'flowmeter_unit' : 'm/s'
        })
        config.setdefaults('usage', {
            'ato_ignore' : '',
            'doser_ignore' : ''
        })
        config.setdefaults('mqtt', {
            'enable' : 'false',
            'broker' : '127.0.0.1',
            'port' : '1883',
            'keepalive' : 60,
            'topic1' : '',
            'topic1_name' : ''
        })
    
    def build_settings(self, settings):
        settings.add_json_panel('Kivy Reef', self.config, filename='settings.json')
    
    def build_widgets(self):
        """ Build widgets and populate the dictionaries """
        self.tc_dict = TempDict(self.connection)
        self.equipment_dict = EquipmentDict(self.connection)
        self.ph_dict = PhDict(self.connection)
        self.ato_dict = AtoDict(self.connection)
        self.doser_dict = DoserDict(self.connection)
        self.macro_dict = MacroDict(self.connection)
    
    def connect(self, dt=None):
        """ Creates an ApiConnection object and tries to authenticate against the reef-pi server"""
        self.connection = ApiConnection(self.config.get('server', 'host'), self.config.get('server', 'user_name'), self.config.get('server', 'password'), int(self.config.get('server', 'timeout')))

        # If successfully connected, create the widgets
        if self.connection.authenticate():
            self.connected = True
            self.status = "Connected"
            self.build_widgets()
            if self.reconnect_timer:
                # If the reconnect timer was been created, cancel it now that the connection is established
                self.reconnect_timer.cancel()
    
    def build(self):
        """ Build the application """
        config = self.config
        
        if not self.connect():
            # If an initial connection cannot be established, retry at set intervals
            self.reconnect_timer = Clock.schedule_interval(self.connect, int(config.get('server', 'reconnect_interval')))
        
        # If MQTT support is enabled, create a connection to the MQTT broker
        if self.config.get('mqtt', 'enable') == '1':
            self.mqtt_connection = MqttConnection(self.config.get('mqtt', 'broker'), self.config.get('mqtt', 'port'), self.config.get('mqtt', 'keepalive'))

        return MainWindow()

if __name__ == '__main__':
    KivyReefApp().run()

