from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, OptionProperty

from requests import ConnectionError, HTTPError

Builder.load_file("system.kv")

class SystemWidget(GridLayout, Widget):
    """ Reefpi system object """
    server_name = StringProperty('')
    server_ip = StringProperty('')
    version = StringProperty('')
    uptime = StringProperty('')
    cpu_temp = StringProperty('')
    entity_type = 'reefpi'
    update_interval = 10

    screen_orientation = OptionProperty("horizontal", options=["vertical", "horizontal"])

    def __init__(self, c):
        super(SystemWidget, self).__init__()
        self.connection = c
        self.update_timer = Clock.schedule_interval(self.update, self.update_interval)
        self.update()
        Window.bind(on_resize=self.getOrientation)

    def update(self, dt=None):
        if App.get_running_app().connected:
            new_reading = self.connection.system_query()
            if new_reading:
                self.server_name = new_reading.get('name')
                self.server_ip = new_reading.get('ip')
                self.version = new_reading.get('version')
                self.uptime = new_reading.get('uptime')
                self.cpu_temp = new_reading.get('cpu_temperature').strip() # Remove trailing newline
                App.get_running_app().cpu_temp = self.cpu_temp
                App.get_running_app().reefpi_version = self.version
    
    def reload(self):
        self.connection.api_post(category='system', command='reload')

    def getOrientation(self, *args):
        if Window.height < Window.width:
            self.screen_orientation = 'horizontal'
        else:
            self.screen_orientation = 'vertical'
