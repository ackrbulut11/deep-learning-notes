import os
import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from model import IrisClassifier

# ──────────────────────────────────────────────
# App setup
# ──────────────────────────────────────────────
app = FastAPI(title="Iris Classifier API", version="1.0.0")

CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]

# ──────────────────────────────────────────────
# Load model at startup
# ──────────────────────────────────────────────
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "04-Pytorch",
    "models",
    "iris_classification_model.pth",
)

model = IrisClassifier()
model_loaded = False

try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    model_loaded = True
    print(f"[OK] Model loaded from: {os.path.abspath(MODEL_PATH)}")
except Exception as e:
    print(f"[ERROR] Could not load model: {e}")

# ──────────────────────────────────────────────
# Static files
# ──────────────────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ──────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionResponse(BaseModel):
    prediction: str
    class_id: int
    probabilities: dict
    confidence: float


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model_loaded}


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: IrisInput):
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")

    features = torch.tensor(
        [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]],
        dtype=torch.float32,
    )

    with torch.inference_mode():
        logits = model(features)
        probs = F.softmax(logits, dim=1).squeeze().tolist()

    class_id = int(probs.index(max(probs)))
    probabilities = {
        name: round(p * 100, 2) for name, p in zip(CLASS_NAMES, probs)
    }

    return PredictionResponse(
        prediction=CLASS_NAMES[class_id],
        class_id=class_id,
        probabilities=probabilities,
        confidence=round(max(probs) * 100, 2),
    )


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
