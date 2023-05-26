from typing import Dict
import paho.mqtt.client as mqtt

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

Builder.load_file("mqtt.kv")

class MqttConnection():

    def __init__(self, broker, port, keepalive=60) -> None:
        self.client = mqtt.Client()
        self.client.loop_start()
        try:
            self.client.connect(broker, int(port), int(keepalive))
        except TimeoutError:
            pass
    
    def publish(self, topic, payload):
        try:
            self.client.publish(topic, payload)
        except TimeoutError:
            return False
    
    def subscribe(self, topic):
        try:
            self.client.subscribe(topic)
        except TimeoutError:
            return False

class MqttWidget(Widget):
    connection = ObjectProperty(None)
    name = StringProperty('')
    topic = StringProperty('')
    on = BooleanProperty(False)

    def __init__(self, mqtt_connection, topic, name, **kwargs):
        super(MqttWidget, self).__init__(**kwargs)
        self.connection = mqtt_connection
        self.topic = topic
        self.name = name

    def pressed(self):
        if self.on:
            if self.connection.publish(self.topic, '{"state": "OFF"}'):
                self.on = False
        else:
            if self.connection.publish(self.topic, '{"state": "ON"}'):
                self.on = True
