/* ────────────────────────────────────────────
   Starfield
──────────────────────────────────────────── */
const canvas = document.getElementById('starfield');
const ctx    = canvas.getContext('2d');

let stars = [];

function initStars() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
  stars = Array.from({ length: 180 }, () => ({
    x:     Math.random() * canvas.width,
    y:     Math.random() * canvas.height,
    r:     Math.random() * 1.2 + 0.2,
    alpha: Math.random(),
    speed: Math.random() * 0.003 + 0.001,
  }));
}

function drawStars() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  stars.forEach(s => {
    s.alpha += s.speed;
    if (s.alpha > 1 || s.alpha < 0) s.speed *= -1;
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(180,220,255,${s.alpha.toFixed(2)})`;
    ctx.fill();
  });
  requestAnimationFrame(drawStars);
}

initStars();
drawStars();
window.addEventListener('resize', initStars);

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

const PRESETS = {
  'preset-brown': { temperature: 3068,  luminosity: 0.0024,   radius: 0.17,   magnitude: 16.12,  color: 'Red',          spectralClass: 'M' },
  'preset-red':   { temperature: 3500,  luminosity: 0.0035,   radius: 0.3,    magnitude: 13.1,   color: 'Red',          spectralClass: 'M' },
  'preset-main':  { temperature: 5778,  luminosity: 1.0,      radius: 1.0,    magnitude: 4.83,   color: 'Yellow-white', spectralClass: 'G' },
  'preset-hyper': { temperature: 30000, luminosity: 850000,   radius: 1600,   magnitude: -9.5,   color: 'Blue',         spectralClass: 'B' },
};

/* ────────────────────────────────────────────
   Refs
──────────────────────────────────────────── */
const statusDot  = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const predictBtn = document.getElementById('predictBtn');
const btnText    = document.getElementById('btnText');
const btnSpinner = document.getElementById('btnSpinner');
const idleState  = document.getElementById('idleState');
const resultState= document.getElementById('resultState');
const errorToast = document.getElementById('errorToast');
const errorMsg   = document.getElementById('errorMsg');

/* ────────────────────────────────────────────
   Presets
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
   Health check
──────────────────────────────────────────── */
async function checkHealth() {
  try {
    const res  = await fetch('/health');
    const data = await res.json();
    if (data.status === 'healthy' && data.model_loaded) {
      statusDot.classList.add('online');
      statusText.textContent = 'SYSTEM ONLINE';
    } else {
      statusDot.classList.add('offline');
      statusText.textContent = 'MODEL LOAD FAILED';
    }
  } catch {
    statusDot.classList.add('offline');
    statusText.textContent = 'SERVER UNREACHABLE';
  }
}
checkHealth();

/* ────────────────────────────────────────────
   Form submit → Predict
──────────────────────────────────────────── */
document.getElementById('starForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  await predict();
});

async function predict() {
  const temperature   = parseInt(document.getElementById('temperature').value, 10);
  const luminosity    = parseFloat(document.getElementById('luminosity').value);
  const radius        = parseFloat(document.getElementById('radius').value);
  const magnitude     = parseFloat(document.getElementById('magnitude').value);
  const color         = document.getElementById('color').value;
  const spectralClass = document.getElementById('spectralClass').value;

  if ([temperature, luminosity, radius, magnitude].some(isNaN)) {
    showError('Invalid input — please check all numeric fields.');
    return;
  }

  setLoading(true);
  hideError();
  idleState.classList.add('hidden');
  resultState.classList.add('hidden');

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ temperature, luminosity, radius, magnitude, color, spectralClass }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Server error');
    }

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    showError(err.message || 'Unknown error');
    idleState.classList.remove('hidden');
  } finally {
    setLoading(false);
  }
}

/* ────────────────────────────────────────────
   Render result
──────────────────────────────────────────── */
function renderResult(data) {
  document.getElementById('resultIcon').textContent    = STAR_ICONS[data.prediction] ?? '⭐';
  document.getElementById('resultClass').textContent   = data.prediction.toUpperCase();
  document.getElementById('confidenceValue').textContent = `${data.confidence}%`;

  const container = document.getElementById('probBars');
  container.innerHTML = '';

  CLASS_ORDER.forEach(cls => {
    const pct    = data.probabilities[cls] ?? 0;
    const isTop  = cls === data.prediction;

    const row = document.createElement('div');
    row.className = `prob-row${isTop ? ' is-top' : ''}`;
    row.innerHTML = `
      <div class="prob-meta">
        <span class="prob-name">${STAR_ICONS[cls]} ${cls}</span>
        <span class="prob-pct">${pct}%</span>
      </div>
      <div class="prob-track">
        <div class="prob-fill" data-pct="${pct}"></div>
      </div>
    `;
    container.appendChild(row);
  });

  resultState.classList.remove('hidden');

  // Animate bars
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      container.querySelectorAll('.prob-fill').forEach(fill => {
        fill.style.width = `${fill.dataset.pct}%`;
      });
    });
  });
}

/* ────────────────────────────────────────────
   UI helpers
──────────────────────────────────────────── */
function setLoading(on) {
  predictBtn.disabled     = on;
  btnText.textContent     = on ? '◌ PROCESSING…' : '▶ RUN ANALYSIS';
  btnSpinner.classList.toggle('hidden', !on);
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorToast.classList.remove('hidden');
}

function hideError() {
  errorToast.classList.add('hidden');
}
