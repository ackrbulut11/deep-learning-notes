/* ────────────────────────────────────────────
   Constants
──────────────────────────────────────────── */
const STAR_ICONS = {
  'Brown Dwarf':   '🟤',
  'Red Dwarf':     '🔴',
  'White Dwarf':   '⚪',
  'Main Sequence': '🌟',
  'Supergiant':    '🌠',
  'Hypergiant':    '💥',
};

const CLASS_ORDER = [
  'Brown Dwarf', 'Red Dwarf', 'White Dwarf',
  'Main Sequence', 'Supergiant', 'Hypergiant',
];

// CSS class key per star type
const CSS_KEY = {
  'Brown Dwarf':   'brown-dwarf',
  'Red Dwarf':     'red-dwarf',
  'White Dwarf':   'white-dwarf',
  'Main Sequence': 'main-sequence',
  'Supergiant':    'supergiant',
  'Hypergiant':    'hypergiant',
};

/* ────────────────────────────────────────────
   Preset values
──────────────────────────────────────────── */
const PRESETS = {
  'preset-brown': { temperature: 3068,  luminosity: 0.0024,  radius: 0.17,   magnitude: 16.12, color: 'Red',        spectralClass: 'M' },
  'preset-red':   { temperature: 3500,  luminosity: 0.0035,  radius: 0.3,    magnitude: 13.1,  color: 'Red',        spectralClass: 'M' },
  'preset-main':  { temperature: 5778,  luminosity: 1.0,     radius: 1.0,    magnitude: 4.83,  color: 'Yellow-white', spectralClass: 'G' },
  'preset-hyper': { temperature: 30000, luminosity: 850000,  radius: 1600,   magnitude: -9.5,  color: 'Blue',       spectralClass: 'B' },
};

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
   Preset buttons
──────────────────────────────────────────── */
Object.entries(PRESETS).forEach(([id, vals]) => {
  const btn = document.getElementById(id);
  if (!btn) return;
  btn.addEventListener('click', () => {
    document.getElementById('temperature').value   = vals.temperature;
    document.getElementById('luminosity').value    = vals.luminosity;
    document.getElementById('radius').value        = vals.radius;
    document.getElementById('magnitude').value     = vals.magnitude;
    document.getElementById('color').value         = vals.color;
    document.getElementById('spectralClass').value = vals.spectralClass;
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
  const temperature   = parseInt(document.getElementById('temperature').value, 10);
  const luminosity    = parseFloat(document.getElementById('luminosity').value);
  const radius        = parseFloat(document.getElementById('radius').value);
  const magnitude     = parseFloat(document.getElementById('magnitude').value);
  const color         = document.getElementById('color').value;
  const spectralClass = document.getElementById('spectralClass').value;

  if ([temperature, luminosity, radius, magnitude].some(isNaN)) {
    showError('Lütfen tüm sayısal değerleri doğru girin.');
    return;
  }

  setLoading(true);
  hideError();
  resultCard.classList.add('hidden');

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ temperature, luminosity, radius, magnitude, color, spectralClass }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Sunucu hatası');
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
  document.getElementById('resultIcon').textContent    = STAR_ICONS[data.prediction] ?? '⭐';
  document.getElementById('resultSpecies').textContent = data.prediction;
  document.getElementById('confidenceValue').textContent = `${data.confidence}%`;

  const container = document.getElementById('probBars');
  container.innerHTML = '';

  CLASS_ORDER.forEach(cls => {
    const pct = data.probabilities[cls] ?? 0;
    const key = CSS_KEY[cls];

    const row = document.createElement('div');
    row.className = 'prob-row';
    row.innerHTML = `
      <div class="prob-meta">
        <span class="prob-name">${STAR_ICONS[cls]} ${cls}</span>
        <span class="prob-pct">${pct}%</span>
      </div>
      <div class="prob-track">
        <div class="prob-fill ${key}" data-pct="${pct}"></div>
      </div>
    `;
    container.appendChild(row);
  });

  resultCard.classList.remove('hidden');

  // Animate bars after DOM paint
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
  predictBtn.disabled     = on;
  btnText.textContent     = on ? 'Hesaplanıyor...' : 'Tahmin Et';
  btnSpinner.classList.toggle('hidden', !on);
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorToast.classList.remove('hidden');
}

function hideError() {
  errorToast.classList.add('hidden');
}
