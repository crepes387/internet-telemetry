from paho.mqtt import client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from prometheus_client import Gauge, start_http_server
import time
data_memory = Gauge("virtual memory", "virtual memory di laptop")
data_cpu = Gauge("cpu percent", "berapa persen cpu yang dipakai")
battery = Gauge("battery random", "turun 3 setiap 3 detik")

def sorting(topic, msg):
    if "memory" in topic:
        data_memory.set(msg)
    elif "cpu" in topic:
        data_cpu.set(msg)
    elif "battery" in topic:
        battery.set(msg)
    else:
        print("error! message tidak diketahui")

def on_message(client, data, msg):
    try:
        topic = msg.topic 
        payload = float(msg.payload.decode())

        now = time.strftime("%H:%M:%S", time.localtime())
        print(f"menerima {topic}: {payload} pada {now}")
        sorting(topic, payload)

    except Exception as e:
        print(f"error karena {e}")

def on_connect(client, userdata, flags, rc, prop):
    global connected  
    if rc == 0:
        print("broker connected")
        client.subscribe(topic)
    else:
        print("broker not connected")

def on_subscribe(client, userdata, mid, rc, properties):
    if rc == 128:
        print("subscribe error")
    else:
        print("subscribe berhasil")
 
connected = False
broker_address = "fuji.lmq.cloudamqp.com"
port = 8883
username = "taqfkmpa:taqfkmpa"
password = "gUhaWkG-m3qA7pmRUSnl3ARqEIY0TPMS"
topic = "drive/topic/#"

client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.tls_set()
client.tls_insecure_set(True)
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.username_pw_set(username, password)
client.connect(host=broker_address, port=port, keepalive=60)
client.loop_start()

start_http_server(8000)
while True:
    time.sleep(0.2)

