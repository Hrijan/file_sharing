document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const scanBtn = document.getElementById('scanBtn');
    const devicesList = document.getElementById('devicesList');
    const fileInput = document.getElementById('fileInput');
    const sendBtn = document.getElementById('sendBtn');

    scanBtn.addEventListener('click', () => {
        socket.emit('scan_network');
    });

    socket.on('devices', (devices) => {
        devicesList.innerHTML = '';
        devices.forEach((device, index) => {
            const li = document.createElement('li');
            li.textContent = `${index + 1}. ${device}`;
            li.dataset.ip = device;
            devicesList.appendChild(li);
        });
    });

    sendBtn.addEventListener('click', () => {
        const selectedDevice = devicesList.querySelector('li.selected');
        if (!selectedDevice) {
            alert('Please select a device to send the file to.');
            return;
        }

        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a file to send.');
            return;
        }

        const targetIp = selectedDevice.dataset.ip;
        const filePath = file.name;

        socket.emit('send_file', { targetIp, filePath });
    });

    devicesList.addEventListener('click', (e) => {
        const items = devicesList.querySelectorAll('li');
        items.forEach(item => item.classList.remove('selected'));
        e.target.classList.add('selected');
    });

    socket.on('progress', (data) => {
        console.log(`Progress: ${data.bytesSent}/${data.fileSize} (${data.type})`);
    });
});
