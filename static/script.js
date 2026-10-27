const donutCtx = document.getElementById('donutChart').getContext('2d');
const lineCtx = document.getElementById('lineChart').getContext('2d');

let donutChart = new Chart(donutCtx, {
  type: 'doughnut',
  data: {
    labels: ['Blocked', 'Allowed'],
    datasets: [{
      data: [0, 0],
      backgroundColor: ['#ff6b6b', '#36e0b1'],
      borderColor: '#0d1222',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#e6eef8' } }
    }
  }
});

let lineChart = new Chart(lineCtx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Requests',
      data: [],
      borderColor: '#36e0b1',
      backgroundColor: 'rgba(54,224,177,0.15)',
      tension: 0.35,
      fill: true,
      pointBackgroundColor: '#36e0b1',
      pointBorderColor: '#060b16'
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#e6eef8' } }
    },
    scales: {
      y: { ticks: { color: '#8896ab' }, grid: { color: '#1b2847' } },
      x: { ticks: { color: '#8896ab' }, grid: { color: '#1b2847' } }
    }
  }
});

function addLog(message, blocked) {
  const feed = document.getElementById('logFeed');
  const entry = document.createElement('div');
  entry.className = 'entry';
  const time = new Date().toLocaleTimeString();
  const cls = blocked ? 'blocked' : 'allowed';
  entry.innerHTML = `<span class="time">[${time}]</span> <span class="${cls}">${message}</span>`;
  feed.prepend(entry);
}

async function refreshStats() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) throw new Error('Stats fetch failed');
    const data = await res.json();

    document.getElementById('statTotal').textContent = data.total_requests || 0;
    document.getElementById('statBlocked').textContent = data.blocked || 0;
    document.getElementById('statAllowed').textContent = data.allowed || 0;

    donutChart.data.datasets[0].data = [
      data.blocked || 0,
      data.allowed || 0
    ];
    donutChart.update();

    // Build time-series from recent attacks (simulate line chart)
    const recent = data.recent_attacks || [];
    const labels = recent.map(r => {
      const d = new Date(r.timestamp);
      return d.toLocaleTimeString();
    }).reverse();
    const values = recent.map(r => r.ml_prediction === 'Blocked' ? 1 : 0).reverse();

    // Aggregate as counts per timestamp bucket for line chart
    const counts = {};
    recent.forEach(r => {
      const ts = new Date(r.timestamp).toLocaleTimeString();
      counts[ts] = (counts[ts] || 0) + 1;
    });
    const lineLabels = Object.keys(counts);
    const lineData = Object.values(counts);

    lineChart.data.labels = lineLabels;
    lineChart.data.datasets[0].data = lineData;
    lineChart.update();
  } catch (e) {
    console.error('Refresh error:', e);
  }
}

async function simulate(type) {
  const output = document.getElementById('simOutput');
  output.textContent = 'Sending simulation...';

  try {
    const res = await fetch('/api/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'User-Agent': type === 'attack' ? 'BotAgent/1.0 RandomX-' + Math.random() : 'NormalBrowser/1.0' },
      body: JSON.stringify({ target: 'sim-' + Date.now() })
    });

    if (res.status === 403) {
      const data = await res.json();
      output.textContent = 'BLOCKED: ' + (data.description || data.message || 'Firewall blocked');
      addLog('⚠️ BLOCKED IP 192.168.x.x — High frequency / bot pattern', true);
    } else {
      const data = await res.json();
      output.textContent = 'ALLOWED: ' + (data.message || JSON.stringify(data));
      addLog('✅ ALLOWED request — Normal traffic pattern', false);
    }
  } catch (e) {
    output.textContent = 'Error: ' + e.message;
    addLog('❌ Request error — ' + e.message, false);
  }

  refreshStats();
}

setInterval(refreshStats, 3000);
refreshStats();
