/* ────────────────────────────────────────────
   Constants
──────────────────────────────────────────── */
const CLASS_FLOWERS = { Setosa: '🌼', Versicolor: '🌺', Virginica: '🌸' };
const CLASS_KEYS    = ['Setosa', 'Versicolor', 'Virginica'];
const CLASS_DISPLAY = { Setosa: 'Iris-setosa', Versicolor: 'Iris-versicolor', Virginica: 'Iris-virginica' };

/* ────────────────────────────────────────────
   Element refs
──────────────────────────────────────────── */
const statusDot  = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const predictBtn = document.getElementById('predictBtn');
const btnText    = document.getElementById('btnText');
const btnSpinner = document.getElementById('btnSpinner');
const resultCard = document.getElementById('resultCard');
const errorToast = document.getElementById('errorToast');
const errorMsg   = document.getElementById('errorMsg');

/* ────────────────────────────────────────────
   Slider ↔ Number sync
──────────────────────────────────────────── */
const syncPairs = [
  ['sepalLengthSlider', 'sepalLength'],
  ['sepalWidthSlider',  'sepalWidth'],
  ['petalLengthSlider', 'petalLength'],
  ['petalWidthSlider',  'petalWidth'],
];

syncPairs.forEach(([sliderId, numberId]) => {
  const slider = document.getElementById(sliderId);
  const number = document.getElementById(numberId);

  const updateGradient = (s) => {
    const pct = ((parseFloat(s.value) - parseFloat(s.min)) / (parseFloat(s.max) - parseFloat(s.min))) * 100;
    s.style.background = `linear-gradient(to right, var(--accent) ${pct}%, var(--border) ${pct}%)`;
  };

  slider.addEventListener('input', () => { number.value = slider.value; updateGradient(slider); });
  number.addEventListener('input', () => { slider.value = number.value; updateGradient(slider); });
  updateGradient(slider); // init
});

/* ────────────────────────────────────────────
   Preset buttons
──────────────────────────────────────────── */
document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const vals = [
      parseFloat(btn.dataset.sl),
      parseFloat(btn.dataset.sw),
      parseFloat(btn.dataset.pl),
      parseFloat(btn.dataset.pw),
    ];
    syncPairs.forEach(([sliderId, numberId], i) => {
      const slider = document.getElementById(sliderId);
      const number = document.getElementById(numberId);
      slider.value = vals[i];
      number.value = vals[i];
      slider.dispatchEvent(new Event('input'));
    });
  });
});

/* ────────────────────────────────────────────
   Health check on load
──────────────────────────────────────────── */
async function checkHealth() {
  try {
    const res  = await fetch('/health');
    const data = await res.json();
    if (data.status === 'healthy' && data.model_loaded) {
      statusDot.classList.add('online');
      statusText.textContent = 'Model hazır';
    } else {
      statusDot.classList.add('offline');
      statusText.textContent = 'Model yüklenemedi';
    }
  } catch {
    statusDot.classList.add('offline');
    statusText.textContent = 'Sunucuya ulaşılamıyor';
  }
}
checkHealth();

/* ────────────────────────────────────────────
   Predict
──────────────────────────────────────────── */
predictBtn.addEventListener('click', predict);

async function predict() {
  const sepal_length = parseFloat(document.getElementById('sepalLength').value);
  const sepal_width  = parseFloat(document.getElementById('sepalWidth').value);
  const petal_length = parseFloat(document.getElementById('petalLength').value);
  const petal_width  = parseFloat(document.getElementById('petalWidth').value);

  if ([sepal_length, sepal_width, petal_length, petal_width].some(isNaN)) {
    showError('Lutfen tum degerleri dogru girin.');
    return;
  }

  setLoading(true);
  hideError();
  resultCard.classList.add('hidden');

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sepal_length, sepal_width, petal_length, petal_width }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Sunucu hatasi');
    }

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    showError(err.message || 'Bilinmeyen hata');
  } finally {
    setLoading(false);
  }
}

/* ────────────────────────────────────────────
   Render result
──────────────────────────────────────────── */
function renderResult(data) {
  document.getElementById('resultFlower').textContent  = CLASS_FLOWERS[data.prediction] ?? '🌸';
  document.getElementById('resultSpecies').textContent = CLASS_DISPLAY[data.prediction] ?? data.prediction;
  document.getElementById('confidenceValue').textContent = `${data.confidence}%`;

  const container = document.getElementById('probBars');
  container.innerHTML = '';

  CLASS_KEYS.forEach(cls => {
    const pct = data.probabilities[cls] ?? 0;
    const key = cls.toLowerCase();

    const row = document.createElement('div');
    row.className = 'prob-row';
    row.innerHTML = `
      <div class="prob-meta">
        <span class="prob-name">${CLASS_FLOWERS[cls]} ${CLASS_DISPLAY[cls]}</span>
        <span class="prob-pct ${key}">${pct}%</span>
      </div>
      <div class="prob-track">
        <div class="prob-fill ${key}" data-pct="${pct}"></div>
      </div>
    `;
    container.appendChild(row);
  });

  resultCard.classList.remove('hidden');

  // Animate bars + smooth scroll to result
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      container.querySelectorAll('.prob-fill').forEach(fill => {
        fill.style.width = `${fill.dataset.pct}%`;
      });
      resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

/* ────────────────────────────────────────────
   UI helpers
──────────────────────────────────────────── */
function setLoading(on) {
  predictBtn.disabled      = on;
  btnText.textContent      = on ? 'Hesaplaniyor...' : 'Tahmin Et';
  btnSpinner.classList.toggle('hidden', !on);
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorToast.classList.remove('hidden');
}

function hideError() {
  errorToast.classList.add('hidden');
}
