#------------------------------------------
#--- Author: Shitakha Oboo
#--- Version: 1.0
#--- Python Ver:3.6
#------------------------------------------


import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

#====================================================
# MQTT Settings 
MQTT_Broker = "raspberrypi"
MQTT_Port = 1883
Keep_Alive_Interval = 45
mqtt_house = "Jkuat-grid/house1/consumption_data"
#====================================================

def on_connect(client, userdata, rc):
	if rc != 0:
		pass
		print ("Unable to connect to MQTT Broker...")
	else:
		print ("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass


mqttc = mqtt.Client()
mqttc.username_pw_set(username="oboo", password="root100")
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		

		
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ("")


#====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0

def publish_Fake_Sensor_Values_to_MQTT():
	threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()
	global toggle
	if toggle == 0:
		fake_consumption =random.randint(1,101)

		data = {}
		data['Sensor_ID'] = 1
		data['Date'] = (datetime.today()).strftime("%d-%b-%Y")
		data['amount'] = fake_consumption
		fake_data = json.dumps(data)

		print ("Publishing fake Consumption Value: " + str(fake_consumption) + "...")
		publish_To_Topic (mqtt_house, fake_data)


publish_Fake_Sensor_Values_to_MQTT()

#====================================================
