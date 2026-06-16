const socket = io();

// ============================================================
// GLOBO 3D (Three.js)
// ============================================================
const canvas = document.getElementById('globe');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050505);

const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
camera.position.set(0, 1, 4);

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

const geometry = new THREE.SphereGeometry(1.5, 48, 32);
const material = new THREE.MeshBasicMaterial({
    color: 0x00FF66,
    wireframe: true,
    transparent: true,
    opacity: 0.3
});
const globe = new THREE.Mesh(geometry, material);
scene.add(globe);

function animate() {
    requestAnimationFrame(animate);
    globe.rotation.y += 0.001;
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
});

// ============================================================
// LOGS E COMANDOS (WebSocket)
// ============================================================
const logs = document.getElementById('logs');
const cmd = document.getElementById('cmd');

socket.on('log', (data) => {
    logs.innerHTML += `<div class="log-line">${data.mensagem}</div>`;
    logs.scrollTop = logs.scrollHeight;
});

cmd.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const comando = cmd.value.trim();
        if (!comando) return;
        socket.emit('comando', { comando });
        logs.innerHTML += `<div class="log-line">SHIRA@C2:~$ ${comando}</div>`;
        cmd.value = '';
    }
});
