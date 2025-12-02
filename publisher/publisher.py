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
        self.speed = -10
        self.now = 0
        self.acuan = 0
        self.topic = "drive/topic/battery"
    def proses(self):
        now = time.time()
        if self.acuan == 0:
            self.acuan = now
        elif (self.baterai == 0 and self.speed < 0) or (self.baterai == 100 and self.speed > 0): #perubahan naik turun
            self.acuan = 0
            self.speed *= -1
        elif now - self.acuan >= 5:
            self.move()
            self.acuan = 0
    def move(self):
        self.baterai += self.speed
    def publish(self):
        self.now = time.strftime("%H:%M:%S", time.localtime())
        print(f"mengirim {self.topic}: {self.baterai} pada {self.now}")
        client.publish(self.topic, self.baterai)

class data:
    def __init__(self):
        self.cpu = psutil.cpu_percent()
        self.memory = psutil.virtual_memory().percent
        self.topic_memory = "drive/topic/memory"
        self.topic_cpu = "drive/topic/cpu"
    def initialize(self):
        self.cpu = psutil.cpu_percent()
        self.memory = psutil.virtual_memory().percent
    def publish(self):
        self.now = time.strftime("%H:%M:%S", time.localtime())
        client.publish(self.topic_cpu, self.cpu)
        client.publish(self.topic_memory, self.memory)
        print(f"mengirim data: pada {self.now}")

#define broker (menggunakan cloud terlebih dahulu)
broker_address = "fuji.lmq.cloudamqp.com"
port = 8883
username = "taqfkmpa:taqfkmpa"
password = "gUhaWkG-m3qA7pmRUSnl3ARqEIY0TPMS"

#message
topic = "drive/topic/#"

client = mqtt.Client(client_id="crepes387", callback_api_version=CallbackAPIVersion.VERSION2) #unique clientID 
client.tls_set()
client.tls_insecure_set(True)
client.username_pw_set(username, password) #set pw
client.connect(broker_address, port, keepalive=60)
client.on_connect = on_connect
client.loop_start()
baterai1 = baterai()
data1 = data()
while True:

    data1.initialize()
    data1.publish()
        
    baterai1.proses()
    baterai1.publish()
        
    time.sleep(0.2)