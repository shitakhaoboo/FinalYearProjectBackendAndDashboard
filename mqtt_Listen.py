from time import gmtime, strftime
import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime
# import os
# # django project name is adleads, replace adleads with your project name
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pharmacy.settings")
# from pharmacy.store.models import load_meter

# Keep_Alive_Interval = 45
MQTT_Topic1 = "Jkuat-grid/#"
dbFile = 'IoT1.db'
dbFile1 = '/home/pi/pharmacy/db.sqlite3'


class DatabaseManager:
    def __init__(self, jina):
        self.conn = sqlite3.connect(jina)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_Topic1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #from the meter, we get consumption data
    if msg.topic == "Jkuat-grid/house1/consumed":
        # my_data = json.loads(msg.payload)
        print(msg.payload)
        a = 1
        #KPLC format YYYY/MM/DD
        b = datetime.now()
        # safaricom format DD/MM/YY
        f=b.strftime("%y-%m-%d")
        c = float(msg.payload)
        print(a,b, c,f)
        print("Writing to db...")
        dbobj = DatabaseManager(dbFile1)
        dbobj.add_del_update_db_record("INSERT INTO store_daily_consumption(meter_id,day,usage) VALUES (?,?,?)", [a,f,c])
        #write function to update balance for the current user(manipulate database vs publish to token_balance topic
        del dbobj
        # data_fetch(-c,a)
        
    elif msg.topic == "Jkuat-grid/load_data":
        #from the mobile app, we get load data
#         print(msg.payload)
        #convert received message to string
        m1 = str(msg.payload)
        #divide the string using split method
        step_1 = m1.split("\\n")

        a = int((step_1[1].split())[2])
        #a is meter id, b is money, c is units,d is time
        print(a)
        #to remain with the amount and convert it to float
        step_2 = str((step_1[5].split())[1]).lstrip("Ksh").strip("'")
        b = float(step_2)
        #passing amount through tarrif to generate token
        c= b*0.1
        d = datetime.now().strftime("%d/%m/%y")
        e = datetime.now().strftime("%H:%M:%S")
        print(b)
        # saver = load_meter(meter=a,ksh=b,units=c)
        # saver.save()
        token = step_1[2].split()[1]
        dbobj = DatabaseManager(dbFile1)
        dbobj.add_del_update_db_record("INSERT INTO store_load_meter(meter_id,ksh,units,day,time,token) VALUES (?,?,?,?,?,?)", [a,b,c,d,e,token])
        del dbobj
#         in case meter is connected to online broker
        client.publish("Jkuat-grid/house1/load_data_meter",token)

    elif msg.topic == "Jkuat-grid/house1/status":
        print(msg.payload)

    else:
        return

client = mqtt.Client()
# client.username_pw_set(username="oboo", password="root100")
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
