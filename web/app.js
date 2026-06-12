const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// =========================
// STATE
// =========================
let agents = [];
let ws;

// =========================
// UI ELEMENTS
// =========================
const systemSelect = document.getElementById("system");
const aSlider = document.getElementById("a");
const bSlider = document.getElementById("b");
const dampingSlider = document.getElementById("damping");
const speedSlider = document.getElementById("speed");
const growthSlider = document.getElementById("growth");

// =========================
// WEBSOCKET
// =========================
function connect() {
  //  ws = new WebSocket("ws://127.0.0.1:8000/ws");
  //  ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onopen = () => {
        console.log("🟢 WS conectado");
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        agents = data.agents || [];
        console.log(data.agents[0]);
    };

    ws.onclose = () => {
        console.log("🔴 WS cerrado, reconectando...");
        setTimeout(connect, 1000);
    };
}

connect();
// =========================
// BOTON RESET
// =========================
async function reset() {
    await fetch("http://127.0.0.1:8000/reset", {
        method: "POST"
    });
}
// =========================
// SEND CONTROL UPDATES
// =========================
function sendSystem(value) {
    fetch(`http://127.0.0.1:8000/system/${value}`, {
        method: "POST"
    });
}

function sendParams() {
    fetch("http://127.0.0.1:8000/params", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            a: parseFloat(aSlider.value),
            b: parseFloat(bSlider.value),
            damping: parseFloat(dampingSlider.value),
            speed: parseFloat(speedSlider.value),
            growth_rate: parseFloat(growthSlider.value)
        })
    });
}

// =========================
// EVENTS
// =========================
systemSelect.addEventListener("change", (e) => {
    sendSystem(e.target.value);
});

[aSlider, bSlider, dampingSlider, speedSlider].forEach(slider => {
    slider.addEventListener("input", sendParams);
});

// =========================
// RENDER LOOP
// =========================
function draw() {
    ctx.fillStyle = "rgba(0,0,0,0.2)";
ctx.fillRect(0, 0, canvas.width, canvas.height);

const cx = canvas.width / 2;
const cy = canvas.height / 2;
const scale = 200;

// trails
for (let i = 0; i < agents.length; i++) {
    ctx.strokeStyle = "rgba(255,255,255,0.2)";
    ctx.lineWidth = 2;

    const size = scale; // usa mismo scale

    ctx.strokeRect(
        cx - size,
        cy - size,
        size * 2,
        size * 2
    );
    
    const a = agents[i];
    if (!a || !a.trail) continue;

    ctx.beginPath();

    for (let j = 0; j < a.trail.length; j++) {
        const p = a.trail[j];

        const x = cx + p[0] * scale;
        const y = cy + p[1] * scale;

        if (j === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.strokeStyle = "rgba(255,255,255,0.8)";
    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.stroke();
}

    requestAnimationFrame(draw);
}

draw();
window.reset = reset;
