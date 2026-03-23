# 🌌 DeepSky Classifier Web Servisi

PyTorch ile eğitilmiş bir Yıldız Sınıflandırma modelini FastAPI ile web servisi olarak sunan, interaktif ve bilim kurgu temalı modern bir dashboard projesi.

---

## 📋 Özellikler

- **PyTorch Neural Network:** `6 → 16 → 16 → 6` mimarisi (ReLU aktivasyon)
- **FastAPI Backend:** Modelleri, LabelEncoder ve StandardScaler'ı asenkron startup ile hafızada tutan hızlı framework
- **Sci-Fi Dashboard Frontend:** HTML, CSS, JavaScript ile hazırlanan özel yıldız haritası ve terminal/panel arayüzü
- **Real-time Predictions:** Girilen yıldız verilerinden anlık tür tahmini ve güven skorları

---

## 📁 Proje Yapısı

```
DeepSkyClassifier/
│
├── model.py              # PyTorch DeepSkyClassifier model tanımı
├── train.py              # Modeli, encoder ve scaler'ı eğiten script
├── main.py               # FastAPI uygulaması (Backend)
├── README.md             # Proje dokümantasyonu
│
├── models/               # Eğitilmiş model ve ön işleme nesneleri
│   ├── star_model.pth    # Eğitilmiş model ağırlıkları
│   ├── scaler.pkl        # StandardScaler 
│   ├── le_color.pkl      # Renkler için LabelEncoder 
│   └── le_spectral.pkl   # Spektral sınıf için LabelEncoder 
│
└── static/               # Frontend dosyaları
    ├── index.html        # Ana dashboard arayüzü
    ├── style.css         # Neon sci-fi stil dosyası
    └── script.js         # Etkileşim ve API iletişim kodu
```

> **Not:** FastAPI sunucusu başladığında `models/` klasöründeki tüm gerekli `.pth` ve `.pkl` dosyaları otomatik olarak belleğe alınır.

---

## 🚀 Kurulum

### 1. Web Servisini Başlatın

Uygulamayı geliştirme modunda çalıştırmak için klasör dizininde terminalinizi açın ve şu komutu girin:

```bash
uvicorn main:app --reload
```

Servis şu adreste çalışacaktır: **http://127.0.0.1:8000**

> ⚠️ **Önemli:** Modellerin göreceli yollarının (relative path) doğru çalışması için komutu `DeepSkyClassifier/` klasörü içinden çalıştırın.

---

## 🔧 Model Mimarisi

```python
class DeepSkyClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(6, 16),    # Input layer: 6 özellik
            nn.ReLU(),
            nn.Linear(16, 16),   # Hidden layer
            nn.ReLU(),
            nn.Linear(16, 6)     # Output layer: 6 farklı yıldız sınıfı
        )
```

### Girdi Özellikleri (6 Adet)

| Özellik | Tip | Birim/Açıklama |
|---------|-----|----------------|
| Temperature | Sürekli | Kelvin (K) |
| Luminosity | Sürekli | L/Lo (Güneş baz alınarak) |
| Radius | Sürekli | R/Ro (Güneş baz alınarak) |
| Absolute Magnitude | Sürekli | Mv |
| Color | Kategorik | Yıldızın rengi (örn. Red, Blue) |
| Spectral Class | Kategorik | O, B, A, F, G, K, M |

### Çıktı Sınıfları

| Sınıf Adı | Açıklama |
|-----------|----------|
| Brown Dwarf | Kahverengi Cüce |
| Red Dwarf | Kırmızı Cüce |
| White Dwarf | Beyaz Cüce |
| Main Sequence | Ana Kol Yıldızı |
| Supergiant | Süperdev |
| Hypergiant | Hiperdev |

---

## 📡 API Kullanımı

### Health Check

```bash
curl http://127.0.0.1:8000/health
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
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
         "temperature": 5778,
         "luminosity": 1.0,
         "radius": 1.0,
         "magnitude": 4.83,
         "color": "yellow-white",
         "spectralClass": "G"
     }'
```

**Yanıt:**
```json
{
    "prediction": "Main Sequence",
    "class_id": 3,
    "probabilities": {
        "Brown Dwarf": 0.01,
        "Red Dwarf": 0.05,
        "White Dwarf": 0.01,
        "Main Sequence": 99.85,
        "Supergiant": 0.04,
        "Hypergiant": 0.04
    },
    "confidence": 99.85
}
```

---

## 🎨 Kullanıcı Arayüzü

Web arayüzüne erişmek için tarayıcınızda şu adresi açın:

```
http://127.0.0.1:8000
```

![DeepSky Web App](screenshots/deepsky.png)

**Arayüz Detayları:**

- ✨ **Terminal Aesthetics:** Neon "Cyan" ve "Violet" renk paleti, monospace terminal yazı tipleri (Share Tech Mono)
- 🌌 **Hareketli Arka Plan:** HTML5 Canvas ile hazırlanan kayan yıldız haritası
- 🎛️ **Quick Load Formu:** "Güneş (Main Sequence)", "Kahverengi Cüce", "Hiperdev" gibi hızlı ön ayar butonları
- 📊 **Matrix Görselleştirmesi:** Sınıflandırma sonuçlarının yatay olasılık (prob) çubuklarıyla ve en yüksek tahminli sonucun fosforlu olarak gösterimi
- 🔌 **Dynamic State:** Sistem hazır olana kadar uyku modu (Awaiting Stellar Input) ve bağlantı indikatörü.

---

## 💡 Önemli Notlar

### Veri Ön İşleme (Preprocessing)
Gelen kategorik veriler (`Color`, `Spectral Class`)  `LabelEncoder` ile sayısala dönüştürülür. Tüm 6 özellik, tahmin işleminden hemen önce `StandardScaler` ile ölçeklendirilir. Aksi takdirde farklı birimli sayılar (örn. 30.000 Sıcaklık ve 0.002 Parlaklık) modeli yanlış yönlendirebilir.

### Inference (Tahmin) Modu
```python
with torch.inference_mode():
    logits = model(input_tensor)
    probs = torch.nn.functional.softmax(logits, dim=1)
```

---

## 🐛 Sorun Giderme

### Modül Bulunamadı Veya Joblib Hatası
Model dosyalarınız `.pkl` uzantısıyla paketlenirken hangi araç (pickle vs. joblib) kullanıldıysa okurken de aynı araç kullanılmalıdır. Bu proje `joblib` paketine bağımlıdır.

```bash
pip install joblib fastapi uvicorn scikit-learn torch numpy
```
