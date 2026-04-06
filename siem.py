import subprocess, sys, os, re, time, threading, socket
from datetime import datetime
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Dashboard simples
HTML = """<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIEM Simples</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8">
    <h1 class="text-4xl font-bold text-red-600 mb-6">SIEM Simples</h1>
    
    <div class="bg-white p-8 rounded-3xl shadow max-w-2xl">
        <h2 class="text-xl font-semibold mb-4">Adicionar Log da Aplicação</h2>
        <input id="logpath" type="text" placeholder="/var/log/nginx/access.log" 
               class="w-full p-4 border rounded-xl mb-4">
        <button onclick="addLog()" 
                class="bg-red-600 text-white px-8 py-3 rounded-xl">Adicionar Log</button>
    </div>

    <div class="mt-10 bg-white p-8 rounded-3xl shadow">
        <h2 class="text-xl font-semibold mb-4">IPs Atacantes</h2>
        <div id="result"></div>
    </div>

    <script>
        async function load() {
            const r = await fetch('/api/attacks');
            const d = await r.json();
            document.getElementById('result').innerHTML = 
                `<pre class="bg-gray-100 p-4 rounded-xl">${JSON.stringify(d, null, 2)}</pre>`;
        }
        setInterval(load, 5000);
        window.onload = load;

        async function addLog() {
            const path = document.getElementById('logpath').value;
            await fetch('/add-log', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path})
            });
            load();
        }
    </script>
</body>
</html>"""

MONITORED_LOGS = ["/var/log/auth.log"]
ATTACKS = {}
LOCK = threading.Lock()

def get_free_port():
    for p in range(8080, 8200):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return 8080

def parse_logs():
    global ATTACKS
    with LOCK:
        for path in MONITORED_LOGS:
            if not os.path.exists(path): continue
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f.readlines()[-3000:]:
                        if any(k in line.lower() for k in ["failed password", "invalid user", "404", "403", "500"]):
                            ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                            if ip_match:
                                ip = ip_match.group(0)
                                if not ip.startswith(("127.", "192.168.", "10.")):
                                    if ip not in ATTACKS:
                                        ATTACKS[ip] = {"count": 0, "last_seen": datetime.now().strftime("%H:%M")}
                                    ATTACKS[ip]["count"] += 1
                                    ATTACKS[ip]["last_seen"] = datetime.now().strftime("%H:%M")
            except:
                pass

def monitor():
    while True:
        parse_logs()
        time.sleep(10)

@app.route('/')
def home():
    return HTML

@app.route('/api/attacks')
def attacks():
    with LOCK:
        return jsonify({"attacks": sorted(ATTACKS.items(), key=lambda x: x[1]["count"], reverse=True)})

@app.route('/add-log', methods=['POST'])
def add_log():
    path = request.get_json().get('path')
    if path and os.path.exists(path) and path not in MONITORED_LOGS:
        MONITORED_LOGS.append(path)
    return jsonify({"success": True})

if __name__ == '__main__':
    print("🚀 Iniciando SIEM Simples...")
    threading.Thread(target=monitor, daemon=True).start()
    port = get_free_port()
    print(f"🌐 Acesse → http://localhost:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
