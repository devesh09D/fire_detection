const socket = io();

document.getElementById('start-detection').addEventListener('click', () => {
    fetch('/api/start_detection', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data));
});

document.getElementById('stop-detection').addEventListener('click', () => {
    fetch('/api/stop_detection', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data));
});

socket.on('frame_update', (data) => {
    document.getElementById('video-feed').src = `data:image/jpeg;base64,${data.image}`;
    const fireAlert = document.getElementById('fire-alert');
    fireAlert.style.display = data.fire_detected ? 'block' : 'none';
});
