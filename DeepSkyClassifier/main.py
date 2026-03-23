import joblib
from contextlib import asynccontextmanager
from pathlib import Path

import numpy as np
import numpy as np
import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from model import DeepSkyClassifier

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"

STAR_CLASS_MAP = {
    0: "Brown Dwarf",
    1: "Red Dwarf",
    2: "White Dwarf",
    3: "Main Sequence",
    4: "Supergiant",
    5: "Hypergiant",
}

# ──────────────────────────────────────────────
# Global state
# ──────────────────────────────────────────────
state: dict = {}


# ──────────────────────────────────────────────
# Lifespan – load artefacts once on startup
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    errors = []

    # Model
    model_path = MODELS_DIR / "star_model.pth"
    try:
        net = DeepSkyClassifier()
        net.load_state_dict(torch.load(model_path, map_location="cpu"))
        net.eval()
        state["model"] = net
        print(f"[OK] Model yüklendi: {model_path}")
    except Exception as exc:
        errors.append(f"Model yüklenemedi: {exc}")
        print(f"[ERROR] {errors[-1]}")

    # Scaler
    scaler_path = MODELS_DIR / "scaler.pkl"
    try:
        state["scaler"] = joblib.load(scaler_path)
        print(f"[OK] Scaler yüklendi: {scaler_path}")
    except Exception as exc:
        errors.append(f"Scaler yüklenemedi: {exc}")
        print(f"[ERROR] {errors[-1]}")

    # LabelEncoder – color
    le_color_path = MODELS_DIR / "le_color.pkl"
    try:
        state["le_color"] = joblib.load(le_color_path)
        print(f"[OK] LabelEncoder (color) yüklendi: {le_color_path}")
    except Exception as exc:
        errors.append(f"le_color yüklenemedi: {exc}")
        print(f"[ERROR] {errors[-1]}")

    # LabelEncoder – spectral class
    le_spectral_path = MODELS_DIR / "le_spectral.pkl"
    try:
        state["le_spectral"] = joblib.load(le_spectral_path)
        print(f"[OK] LabelEncoder (spectral) yüklendi: {le_spectral_path}")
    except Exception as exc:
        errors.append(f"le_spectral yüklenemedi: {exc}")
        print(f"[ERROR] {errors[-1]}")

    state["errors"] = errors
    state["ready"]  = len(errors) == 0

    yield  # app runs here

    state.clear()
    print("[INFO] Uygulama kapandı, kaynaklar serbest bırakıldı.")


# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────
app = FastAPI(
    title="DeepSky Classifier API",
    version="1.0.0",
    description="Yıldız türü sınıflandırıcı – PyTorch + FastAPI",
    lifespan=lifespan,
)

STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ──────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────
class StarInput(BaseModel):
    temperature:   int
    luminosity:    float
    radius:        float
    magnitude:     float
    color:         str
    spectralClass: str


class PredictionResponse(BaseModel):
    prediction:    str
    class_id:      int
    probabilities: dict[str, float]
    confidence:    float


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
async def health():
    return {
        "status":       "healthy" if state.get("ready") else "degraded",
        "model_loaded": state.get("ready", False),
        "errors":       state.get("errors", []),
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: StarInput):
    if not state.get("ready"):
        raise HTTPException(
            status_code=503,
            detail="Servis henüz hazır değil. Yükleme hataları: " + str(state.get("errors", [])),
        )

    # ── 1. Encode categorical fields ──
    le_color    = state["le_color"]
    le_spectral = state["le_spectral"]

    try:
        color_enc = int(le_color.transform([data.color])[0])
    except ValueError:
        valid_colors = list(le_color.classes_)
        raise HTTPException(
            status_code=422,
            detail=f"Bilinmeyen renk: '{data.color}'. Geçerli değerler: {valid_colors}",
        )

    try:
        spectral_enc = int(le_spectral.transform([data.spectralClass])[0])
    except ValueError:
        valid_spectral = list(le_spectral.classes_)
        raise HTTPException(
            status_code=422,
            detail=f"Bilinmeyen spektral sınıf: '{data.spectralClass}'. Geçerli değerler: {valid_spectral}",
        )

    # ── 2. Scale numeric features ──

    raw = np.array([[data.temperature, data.luminosity, data.radius,
                     data.magnitude, color_enc, spectral_enc]], dtype=float)
    scaled = state["scaler"].transform(raw)

    # ── 3. Inference ──
    tensor = torch.tensor(scaled, dtype=torch.float32)
    with torch.inference_mode():
        logits = state["model"](tensor)
        probs  = F.softmax(logits, dim=1).squeeze().tolist()

    class_id    = int(probs.index(max(probs)))
    prediction  = STAR_CLASS_MAP[class_id]
    confidence  = round(max(probs) * 100, 2)
    probability_map = {
        STAR_CLASS_MAP[i]: round(p * 100, 2) for i, p in enumerate(probs)
    }

    return PredictionResponse(
        prediction=prediction,
        class_id=class_id,
        probabilities=probability_map,
        confidence=confidence,
    )


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
