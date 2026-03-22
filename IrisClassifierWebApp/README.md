# 🌸 Iris Çiçeği Sınıflandırıcı Web Servisi

PyTorch ile eğitilmiş bir Neural Network modelini FastAPI ile web servisi olarak sunan ve modern bir arayüze sahip proje.

---

## 📋 Özellikler

- **PyTorch Neural Network:** `4 → 12 → 12 → 3` mimarisi (ReLU aktivasyon)
- **FastAPI Backend:** Hızlı ve modern Python web framework'ü
- **Responsive Frontend:** HTML, CSS, JavaScript ile modern dark tema arayüzü
- **Real-time Predictions:** Anlık tahmin yapma ve olasılık görselleştirme

---

## 📁 Proje Yapısı

```
IrisClassifierWebApp/
│
├── model.py              # PyTorch model tanımı
├── main.py               # FastAPI uygulaması
├── requirements.txt      # Python bağımlılıkları
├── README.md             # Proje dokümantasyonu
│
└── static/               # Frontend dosyaları
    ├── index.html        # Ana sayfa
    ├── style.css         # Stil dosyası
    └── script.js         # JavaScript kodu
```

> **Not:** Eğitilmiş model dosyası (`iris_classification_model.pth`) projeyle aynı repodaki `04-Pytorch/models/` klasöründen otomatik olarak yüklenir.

---

## 🚀 Kurulum

### 1. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Web Servisini Başlatın

```bash
python -m uvicorn main:app --port 8000
```

Servis şu adreste çalışacaktır: **http://localhost:8000**

> 💡 8000 portu kullanımdaysa farklı bir port belirtin: `--port 8001`

> ⚠️ **Önemli:** Komutu mutlaka `IrisClassifierWebApp/` klasörü içinden çalıştırın. Sunucu, model dosyasını `../04-Pytorch/models/` yolundan bulur.

---

## 🔧 Model Mimarisi

```python
class IrisClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(4, 12),    # Input layer: 4 özellik
            nn.ReLU(),
            nn.Linear(12, 12),   # Hidden layer
            nn.ReLU(),
            nn.Linear(12, 3)     # Output layer: 3 sınıf
        )
```

### Girdi Özellikleri

| # | Özellik | Birim |
|---|---------|-------|
| 1 | Sepal Uzunluğu | cm |
| 2 | Sepal Genişliği | cm |
| 3 | Petal Uzunluğu | cm |
| 4 | Petal Genişliği | cm |

### Çıktı Sınıfları

| ID | Sınıf |
|----|-------|
| 0 | 🌼 Setosa |
| 1 | 🌺 Versicolor |
| 2 | 🌸 Virginica |

---

## 📡 API Kullanımı

### Health Check

```bash
curl http://localhost:8000/health
```

**Yanıt:**
```json
{
    "status": "healthy",
    "model_loaded": true
}
```

### Tahmin Yapma

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
         "sepal_length": 5.1,
         "sepal_width": 3.5,
         "petal_length": 1.4,
         "petal_width": 0.2
     }'
```

**Yanıt:**
```json
{
    "prediction": "Setosa",
    "class_id": 0,
    "probabilities": {
        "Setosa": 99.87,
        "Versicolor": 0.10,
        "Virginica": 0.03
    },
    "confidence": 99.87
}
```

---

## 🎨 Kullanıcı Arayüzü

Web arayüzüne erişmek için tarayıcınızda şu adresi açın:

```
http://localhost:8000
```

**Arayüz özellikleri:**

- ✨ Modern karanlık tema (glassmorphism)
- 🎚️ Kaydırma çubukları ile kolay değer girişi
- ⚡ Hızlı örnek değer yükleme butonları (Setosa / Versicolor / Virginica)
- 📊 Tahmin sonrası otomatik kaydırma
- 📈 Animasyonlu olasılık dağılımı görselleştirmesi
- 🎯 Güven skoru göstergesi

---

## 💡 Önemli Notlar

### Model Yükleme

```python
from model import IrisClassifier

model = IrisClassifier()
model.load_state_dict(torch.load('iris_classification_model.pth', map_location='cpu'))
model.eval()
```

### Inference (Tahmin) Modu

```python
with torch.inference_mode():
    logits = model(input_tensor)
    probs = torch.nn.functional.softmax(logits, dim=1)
```

---

## 🐛 Sorun Giderme

### Port Zaten Kullanımda

```bash
python -m uvicorn main:app --port 8001
```

### Modül Bulunamadı Hatası

```bash
pip install -r requirements.txt
```

### Model Dosyası Bulunamadı

Sunucuyu `IrisClassifierWebApp/` klasörü **içinden** başlattığınızdan emin olun:

```bash
cd IrisClassifierWebApp
python -m uvicorn main:app --port 8000
```

---

## 📚 Ek Kaynaklar

- [PyTorch Dokümantasyonu](https://pytorch.org/docs/)
- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [Iris Dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html)
