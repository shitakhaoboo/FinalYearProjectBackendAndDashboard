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
dbFile1 = 'db.sqlite3'


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
    if msg.topic == "Jkuat-grid/house1/consumption":
        # my_data = json.loads(msg.payload)
        print(msg.payload)
        a = 1
        #KPLC format YYYY/MM/DD
        b = datetime.now()
        # safaricom format DD/MM/YY
        f=b.strftime("%d/%m/%y")
        c = float(msg.payload)
        print(a,b, c,f)
        print("Writing to db...")
        dbobj = DatabaseManager(dbFile1)
        dbobj.add_del_update_db_record("INSERT INTO store_daily_consumption(meter_id,day,usage) VALUES (?,?,?)", [a,f,c])
        #write function to update balance for the current user(manipulate database vs publish to token_balance topic
        del dbobj
        # data_fetch(-c,a)

    if msg.topic == "Jkuat-grid/load_data":
        #from the mobile app, we get load data
        print(msg.payload)
        #convert received message to string
        m1 = str(msg.payload)
        #divide the string using split method
        step_1 = m1.split(" ")

        a = int(step_1[10])
        #a is meter id, b is money, c is units,d is time
        print(a)
        #to remain with the amount and convert it to float
        step_2 = str(step_1[2]).lstrip("Ksh")
        b = float(step_2)
        #passing amount through tarrif to generate token
        c= b*0.1
        d = datetime.now().strftime("%d/%m/%y")
        e = datetime.now().strftime("%H:%M:%S")
        print(b)
        # saver = load_meter(meter=a,ksh=b,units=c)
        # saver.save()
        dbobj = DatabaseManager(dbFile1)
        dbobj.add_del_update_db_record("INSERT INTO store_load_meter(meter_id,ksh,units,day,time) VALUES (?,?,?,?,?)", [a,b,c,d,e])
        del dbobj
        # data_fetch(c, a)
        #write code to update the meter

    if msg.topic == "Jkuat-grid/house1/status":
        print(msg.payload)

    return

# #function to update the balance table
# def data_fetch(adjustment,mtr):
#     try:
#         sqliteConnection = sqlite3.connect(dbFile1)
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")
#         #to select current balance
#         sqlite_select_query = """SELECT balance from store_meter WHERE id = 1 """
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         records1 = str(records).strip("[],()")
#         #to add purcgased tokens
#         adjustment +=float(records1)
#         print(adjustment)
#         cursor.close()
#         #to save purchased tokens
#
#         sqliteConnection = sqlite3.connect(dbFile1)
#         cursor = sqliteConnection.cursor()
#         sql_update_query = """Update store_meter set balance = ? where id =?"""
#         data= (adjustment,mtr)
#         cursor.execute(sql_update_query, data)
#         sqliteConnection.commit()
#         cursor.close()
#
#
#     except sqlite3.Error as error:
#         print("Failed to read data from sqlite table", error)
#     finally:
#         if (sqliteConnection):
#             sqliteConnection.close()
#             print("The SQLite connection is closed")


client = mqtt.Client()
# client.username_pw_set(username="oboo", password="root100")
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
