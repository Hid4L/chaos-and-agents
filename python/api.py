from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from core.engine import ChaosEngine


# =========================
# APP SETUP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ENGINE GLOBAL
# =========================
engine = ChaosEngine(n_agents=300)


# =========================
# STATE LOCK (EVITA CONFLICTOS WS)
# =========================
lock = asyncio.Lock()


# =========================
# HTTP ENDPOINTS (MINIMAL)
# =========================
@app.get("/step")
def step():
    """
    Debug endpoint (puedes eliminarlo después).
    """
    return engine.step()


@app.post("/reset")
def reset():
    engine.reset()
    return {"ok": True}


@app.post("/system/{name}")
def set_system(name: str):
    engine.set_system(name)
    return {"system": name}


@app.post("/params")
def update_params(self, params):
    # parámetros del campo
    if "a" in params:
        self.params["a"] = float(params["a"])

    if "b" in params:
        self.params["b"] = float(params["b"])

    # parámetros de comportamiento global
    if "damping" in params:
        self.damping = float(params["damping"])

    if "speed" in params:
        self.speed = float(params["speed"])

    if "noise" in params:
        self.noise = float(params["noise"])

    if "growth_rate" in params:
        self.growth_rate = float(params["growth_rate"])


# =========================
# WEBSOCKET REALTIME ENGINE
# =========================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🟢 WebSocket conectado")

    try:
        while True:
            async with lock:
                # 1 tick del motor
                state = engine.step()

            # envío seguro
            await websocket.send_json(state)

            # control de velocidad del sistema
            await asyncio.sleep(0.016)  # ~60 FPS

    except WebSocketDisconnect:
        print("🔴 WebSocket desconectado")

    except Exception as e:
        print("⚠️ error WS:", e)

    finally:
        try:
            await websocket.close()
        except:
            pass