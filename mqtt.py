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
        self.client.connect(broker, int(port), int(keepalive))
    
    def publish(self, topic, payload):
        self.client.publish(topic, payload)
    
    def subscribe(self, topic):
        self.client.subscribe(topic)

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
            self.connection.publish(self.topic, '{"state": "OFF"}')
            self.on = False
        else:
            self.connection.publish(self.topic, '{"state": "ON"}')
            self.on = True
