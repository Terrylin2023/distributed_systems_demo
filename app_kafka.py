import influxdb_client, os, time, threading
from flask import Flask, jsonify
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaProducer
app = Flask(__name__)

#kafka設置
kafka_server = 'localhost:9092'
kafka_topic = 'CPU_Usage'
kafka_topic = 'Health'
kafka_topic = 'Memory_Usage'
kafka_topic = 'throughput'
producer = KafkaProducer(bootstrap_servers=kafka_servers,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Page</title>
        <script>
            async function startDataCollection() {
                const response = await fetch('/start_collect');
                const data = await response.json();
                alert(data.message); // 或者在页面上显示消息
            }

            function updateProgress() {
                fetch('/progress')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('status').innerText = `Status: ${data.status}`;
                        document.getElementById('cpu_usage').innerText = `CPU Usage: ${data.cpu_usage}%`;
                        document.getElementById('health').innerText = `Health: ${data.health}`;
                        document.getElementById('message').innerText = data.message;
                    })
                    .catch(error => console.error('Error fetching data:', error));
            }

            document.addEventListener('DOMContentLoaded', () => {
                setInterval(updateProgress, 1000); // 每秒更新一次
            });
        </script>
    </head>
    <body>
        <h1>This is a Flask InfluxDB Integration Example!</h1>
        <button onclick="startDataCollection()">Start Data Collection</button>
        <p id="status">Status: idle</p>
        <p id="cpu_usage">CPU Usage: 0%</p>
        <p id="health">Health: unknown</p>
        <p id="message">Click start to collect data.</p>
    </body>
    </html>
    '''


# InfluxDB設定
url = 'http://10.8.49.203:8086' # 修改為你的InfluxDB URL
token = "qE1J_1s3kLvjZJpjBKz9FtZSZ_zKqxZMOW6JEdTeDUvo8_nLUxGr7mQutPjtDAIONg68o35Dbe_5sQ2krnoUQg==" # 修改為你的InfluxDB token
org = "cs230" # 修改為你的InfluxDB組織名稱
bucket = "server" # 修改為你的InfluxDB bucket名稱

# 創建InfluxDB客戶端
client = InfluxDBClient(url=url, token=token, org=org)

# 寫入API
write_api = client.write_api(write_options=SYNCHRONOUS)

# 全局变量用于存储进度
progress = {"status": "idle", "cpu_usage": 0, "health": "unknown", "message": ""}




def collect_and_send_data():
    global progress
    # 定時收集和發送數據
    for i in range(10):
        cpu_usage = i * 9
        health = "healthy" if cpu_usage < 80 else "unhealthy"
        producer.send('your_topic', value=data)
        print(f"Sent data to Kafka topic: {data}")
        print(f"Sent CPU usage: {cpu_usage}%",f"Health: {health}")
        progress = {"status": "collecting", "cpu_usage": cpu_usage, "health": health, "message": f"Sent CPU usage: {cpu_usage}%, Health: {health}"}
        time.sleep(1)  # 每1秒運行一次
    progress["status"] = "complete"
    progress["message"] = "Data collection and sending complete!"

@app.route('/start_collect')
def start_collect():
    global progress
    progress = {"status": "starting", "cpu_usage": 0, "health": "unknown", "message": "Starting data collection..."}
    thread = threading.Thread(target=collect_and_send_data)
    thread.start()
    return jsonify({"message": "Data collection started."})

@app.route('/progress')
def get_progress():
    return jsonify(progress)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)