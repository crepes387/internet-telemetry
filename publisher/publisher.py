import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import psutil
import time
import json # Tambahkan library JSON

# Callback
def on_connect(client, userdata, flags, rc, prop):
    if rc == 0:
        print("✅ Berhasil terhubung ke Broker EMQX!")
    else:
        print(f"❌ Gagal terhubung dengan kode: {rc}")

class UavTelemetry:
    def __init__(self):
        self.baterai = 100
        self.speed = -10
        self.acuan_waktu = time.time()
        self.topic = "uav/telemetry/crepes387" # Topik tunggal yang rapi
        
    def update_baterai(self):
        now = time.time()
        if now - self.acuan_waktu >= 5:
            # Logika naik turun bateraimu
            if (self.baterai <= 0 and self.speed < 0) or (self.baterai >= 100 and self.speed > 0):
                self.speed *= -1
            self.baterai += self.speed
            self.acuan_waktu = now

    def publish_data(self, mqtt_client):
        self.update_baterai()
        
        # BUNGKUS SEMUA DATA KE DALAM SATU JSON (DICTIONARY PYTHON)
        payload = {
            "timestamp": time.strftime("%H:%M:%S", time.localtime()),
            "battery": self.baterai,
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent
            }
        }
        
        # Ubah Dictionary menjadi format String JSON
        json_string = json.dumps(payload)
        
        # Kirim 1 paket ini saja ke broker
        mqtt_client.publish(self.topic, json_string, qos=0)
        print(f"🚀 Mengirim data: {json_string}")

# Setup Koneksi
broker_address = "ef6ff411.ala.asia-southeast1.emqxsl.com"
port = 8883
username = "user1"
password = "public1"

client = mqtt.Client(client_id="crepes387", callback_api_version=CallbackAPIVersion.VERSION2)
client.tls_set()
client.tls_insecure_set(True)
client.username_pw_set(username, password)

# PASTIKAN CALLBACK DIDAFTARKAN SEBELUM CONNECT
client.on_connect = on_connect 
client.connect(broker_address, port, keepalive=60)
client.loop_start()

uav = UavTelemetry()

# Loop Utama
try:
    while True:
        uav.publish_data(client)
        time.sleep(1) # Ubah jadi 1 detik. 0.2 detik terlalu cepat untuk pengujian awal.
except KeyboardInterrupt:
    print("\nMenghentikan pengiriman data...")
    client.loop_stop()
    client.disconnect()