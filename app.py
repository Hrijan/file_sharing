from flask import Flask, request, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import threading
from file_transfer import listenOnPort, sendFile
from network_scanner import scanNetwork, discoveredDevices

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    targetIp = request.form['targetIp']
    file = request.files['file']
    filePath = os.path.join(os.getcwd(), file.filename)
    file.save(filePath)
    sendFile(targetIp, filePath)
    return 'File sent successfully', 200

@socketio.on('scan_network')
def handle_scan_network(data):
    discoveredDevices.clear()
    network = data['network']
    threading.Thread(target=scanNetwork, args=(network,)).start()
    socketio.sleep(5)  # Give some time for scanning
    emit('scan_complete', {'devices': discoveredDevices})

if __name__ == '__main__':
    threading.Thread(target=listenOnPort, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
