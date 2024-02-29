import influxdb_client, os, time, threading, random
from flask import Flask, jsonify
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

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
                        document.getElementById('memory_usage').innerText = `Memory Usage: ${data.memory_usage}%`;
                        document.getElementById('throughput').innerText = `Throughput: ${data.throughput} kbps`;
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
        <p id="memory_usage">Memory Usage: 0%</p>
        <p id="throughput">Throughput: 0 kbps</p>
        <p id="health">Health: unknown</p>
        <p id="message">Click start to collect data.</p>
    </body>
    </html>
    '''


# InfluxDB設定
url = 'http://localhost:8086' # InfluxDB URL
token = "your_token" # 修改為你的InfluxDB token
org = "your_org_name" # InfluxDB組織名稱
bucket = "yore_bucket_name" # InfluxDB bucket名稱

# 創建InfluxDB客戶端
client = InfluxDBClient(url=url, token=token, org=org)

# 寫入API
write_api = client.write_api(write_options=SYNCHRONOUS)

# 全局變量用於儲存進度
progress = {"status": "idle", "cpu_usage": 0, "memory_usage": 0,"throughput": 0,"health": "unknown", "message": ""}




def collect_and_send_data():
    global progress
    # 定時收集和發送數據s
    for i in range(10):
        cpu_usage = i * 9
        memory_usage= i * random.randint(1, 10)
        throughput = i * random.randint(10, 100)
        health = "healthy" if cpu_usage < 80 else "unhealthy"
        point = Point("system").tag("host", "server01").field("cpu_usage", cpu_usage).field("memory_usage", memory_usage).field("throughput", throughput).field("health", health) # 創建數據點
        write_api.write(bucket=bucket, org=org, record=point) # 寫入InfluxDB
        print(f"Sent CPU usage: {cpu_usage}% ,memory_usage: {memory_usage}%,throughput: {throughput} kbps,Health: {health}")
        progress = {"status": "collecting", "cpu_usage": cpu_usage, "memory_usage": memory_usage,"throughput": throughput,"health": health, "message": f"Sent CPU usage: {cpu_usage}%, Memory usage: {memory_usage}%, Throughput: {throughput}kbps,Health: {health}"}
        time.sleep(1)  # 每1秒運行一次
    progress["status"] = "complete"
    progress["message"] = "Data collection and sending complete!"

@app.route('/start_collect')
def start_collect():
    global progress
    progress = {"status": "starting", "cpu_usage": 0, "memory_usage": 0,"throughput": 0,"health": "unknown", "message": "Starting data collection..."}
    thread = threading.Thread(target=collect_and_send_data)
    thread.start()
    return jsonify({"message": "Data collection started."})

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/health', methods=['GET'])
def health_check():
    # loadbalencer check health status
    if progress['health'] == 'healthy':
        return jsonify({'status': 'healthy'}),200
    else:
        return jsonify({'status': 'unhealthy'}),503
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
