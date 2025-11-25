from paho.mqtt import client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import psutil
import time

def on_connect(client, userdata, flags, rc, prop):
    global connected  
    if rc == 0:
        print("broker connected")
    else:
        print("broker not connected")

class baterai:
    def __init__(self):
        self.baterai = 100
        self.speed = -20
        self.now = 0
        self.acuan = 0
        self.topic = "drive/topic/battery"
    def proses(self):
        now = time.time()
        if self.acuan == 0:
            self.acuan = now
        elif (self.baterai <= 0 and self.speed < 0) or (self.baterai >= 100 and self.speed > 0):
            self.acuan = 0
            self.speed *= -1
        elif now - self.acuan >= 2:
            self.move()
            self.acuan = 0
    def move(self):
        self.baterai += self.speed
    def publish(self):
        self.now = time.strftime("%H:%M:%S", time.localtime())
        print(f"mengirim {self.topic}: {self.baterai} pada {self.now}")
        client.publish(self.topic, self.baterai)

#define broker (menggunakan cloud terlebih dahulu)
broker_address = "chameleon.lmq.cloudamqp.com"
port = 8883
username = "axsmlklf:axsmlklf"
password = "FXadEHF_swcOjLxyaHJ8pxAa6lniPpTI"

#message
topic = "drive/topic/#"
#data = {"drive/topic/memory":f"{psutil.virtual_memory().percent}", "drive/topic/cpu":f"{psutil.cpu_percent(1)}"}

client = mqtt.Client(client_id="crepes387", callback_api_version=CallbackAPIVersion.VERSION2) #unique clientID 
client.tls_set()
client.tls_insecure_set(True)
client.username_pw_set(username, password) #set pw
client.connect(broker_address, port, keepalive=60)
client.on_connect = on_connect
client.loop_start()
baterai1 = baterai()
while True:
    baterai1.proses()
    baterai1.publish()
    time.sleep(1)