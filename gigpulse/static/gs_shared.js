// ─────────────────────────────────────────────────────────────────────────────
// ZenVyte GigPulse Shared JS — Phase 2
// API base, auth helpers, fetch wrapper, notification polling
// ─────────────────────────────────────────────────────────────────────────────

const API_BASE = ""; // Relative to the same host

// ─── Global Theme Manager ─────────────────────────────────────────────────────
const Theme = {
  apply() {
    const t = localStorage.getItem('gs_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', t);
    const btn = document.getElementById('themeToggle');
    if (btn) { const k = btn.querySelector('.theme-toggle-knob'); if(k) k.textContent = t==='dark'?'🌙':'☀️'; }
  },
  toggle() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const t = isDark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('gs_theme', t);
    const btn = document.getElementById('themeToggle');
    if (btn) { const k = btn.querySelector('.theme-toggle-knob'); if(k) k.textContent = t==='dark'?'🌙':'☀️'; }
  }
};
// Auto-apply on load
(function(){ Theme.apply(); })();

// ─── API Fetch Helper ────────────────────────────────────────────────────────
async function apiCall(path, options = {}) {
  const sess = Session.get();
  const headers = { 
    "Content-Type": "application/json", 
    ...(options.headers || {}) 
  };
  
  if (sess && sess.access_token) {
    headers["Authorization"] = `Bearer ${sess.access_token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "API error");
  }
  return res.json();
}

const GS = {
  get:    (path)         => apiCall(path, { method: "GET" }),
  post:   (path, body)   => apiCall(path, { method: "POST",  body: JSON.stringify(body) }),
  put:    (path, body)   => apiCall(path, { method: "PUT",   body: JSON.stringify(body) }),
  delete: (path)         => apiCall(path, { method: "DELETE" }),
};

// ─── Session Helpers ─────────────────────────────────────────────────────────
const Session = {
  save(data) { localStorage.setItem("gs_session", JSON.stringify(data)); },
  get()      { return JSON.parse(localStorage.getItem("gs_session") || "null"); },
  clear()    { localStorage.removeItem("gs_session"); },
  require()  {
    const s = this.get();
    if (!s) { window.location.href = "/gigpulse_login.html"; return null; }
    return s;
  },
  logout() {
    this.clear();
    window.location.href = "/gigpulse_login.html";
  }
};

// ─── Plan Metadata ────────────────────────────────────────────────────────────
const PLANS = {
  starter:  { label: "🌱 Starter",  premium: 55,  rate: 35, maxHrs: 3, cap: 105,  color: "#4ade80", badge: "starter"  },
  basic:    { label: "🔵 Basic",    premium: 70,  rate: 45, maxHrs: 4, cap: 180,  color: "#60a5fa", badge: "basic"    },
  standard: { label: "🟡 Standard", premium: 90,  rate: 60, maxHrs: 5, cap: 300,  color: "#facc15", badge: "standard" },
  premium:  { label: "🟠 Premium",  premium: 115, rate: 75, maxHrs: 6, cap: 450,  color: "#fb923c", badge: "premium"  },
  elite:    { label: "🔴 Elite",    premium: 135, rate: 90, maxHrs: 7, cap: 630,  color: "#f87171", badge: "elite"    },
};

const TRIGGER_META = {
  rainfall:    { icon: "🌧️", label: "Heavy Rainfall",  color: "#60a5fa", unit: "mm/3hr", threshold: 35 },
  temperature: { icon: "🔥", label: "Extreme Heat",    color: "#f87171", unit: "°C",     threshold: 43 },
  aqi:         { icon: "💨", label: "Severe AQI",      color: "#a78bfa", unit: "AQI",    threshold: 300},
  cyclone:     { icon: "🌀", label: "Cyclone/Flood",   color: "#38bdf8", unit: "alert",  threshold: 1  },
  curfew:      { icon: "🚫", label: "Curfew/Hartal",   color: "#fb923c", unit: "flag",   threshold: 1  },
};

// ─── Toast Notifications ──────────────────────────────────────────────────────
function toast(message, type = "info", duration = 4000) {
  const colors = { info: "#6366f1", success: "#22c55e", error: "#ef4444", warning: "#f59e0b" };
  const icons  = { info: "✨", success: "✅", error: "🚫", warning: "⚠️" };
  
  const container = document.getElementById("gs-toast-container") || (() => {
    const c = document.createElement("div");
    c.id = "gs-toast-container";
    c.style.cssText = "position:fixed; top:24px; right:24px; z-index:9999; display:flex; flex-direction:column; gap:10px; pointer-events:none;";
    document.body.appendChild(c);
    return c;
  })();

  const el = document.createElement("div");
  el.className = "glass fade-in-up";
  el.style.cssText = `
    pointer-events: auto; min-width: 280px; max-width: 380px;
    background: rgba(15, 23, 42, 0.9); border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1); border-left: 4px solid ${colors[type]};
    padding: 16px; display: flex; align-items: center; gap: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4); backdrop-filter: blur(20px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  `;
  
  el.innerHTML = `
    <div style="font-size:20px">${icons[type]}</div>
    <div style="flex:1; font-size:14px; font-weight:500; color:#f1f5f9; line-height:1.4">${message}</div>
    <button onclick="this.parentElement.remove()" style="background:none; border:none; color:#64748b; cursor:pointer; font-size:16px;">✕</button>
  `;

  if (!document.getElementById("gs-global-styles")) {
    const s = document.createElement("style");
    s.id = "gs-global-styles";
    s.textContent = `
      .fade-in-up { animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
      @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
      .glass { background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(12px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; }
      .scale-hover { transition: transform 0.2s ease !important; }
      .scale-hover:hover { transform: scale(1.02) !important; }
      .pulse-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; display: inline-block; position: relative; margin-right: 8px; }
      .pulse-dot::after { content: ""; position: absolute; inset: -4px; border: 2px solid #22c55e; border-radius: 50%; animation: pulse 2s infinite; }
      @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(2.5); opacity: 0; } }
      @media (max-width: 600px) { #gs-toast-container { top: auto; bottom: 20px; left: 20px; right: 20px; width: calc(100% - 40px); } .glass { backdrop-filter: blur(8px) !important; } }
    `;
    document.head.appendChild(s);
  }

  container.appendChild(el);
  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transform = "translateX(20px)";
    setTimeout(() => el.remove(), 400);
  }, duration);
}

// ─── Format Helpers ───────────────────────────────────────────────────────────
function formatINR(n)        { return "₹" + Number(n || 0).toLocaleString("en-IN"); }
function formatDate(d)       { 
  if(!d) return "—";
  const date = new Date(d);
  return date.toLocaleDateString("en-IN", { day:"numeric", month:"short", year:"numeric" }); 
}
function formatTime(d)       { 
  if(!d) return "—";
  const date = new Date(d);
  return date.toLocaleTimeString("en-IN", { hour:"2-digit", minute:"2-digit", second:"2-digit", hour12: true }); 
}
function formatDateTime(d)   { 
  if(!d) return "—";
  // The backend now sends ISO strings with offsets. new Date() handles these perfectly.
  return `${formatDate(d)}, ${formatTime(d)}`; 
}
function formatTimeAgo(d) {
  if(!d) return "—";
  const date = new Date(d);
  const now = new Date();
  const diff = Math.floor((now - date) / 1000);
  if (diff < 60) return "Just now";
  if (diff < 3600) return Math.floor(diff/60) + "m ago";
  if (diff < 86400) return Math.floor(diff/3600) + "h ago";
  return formatDate(d);
}
function capitalize(s)       { return s ? s.charAt(0).toUpperCase() + s.slice(1) : ""; }
function trustColor(score)   {
  if (score >= 75) return "#4ade80";
  if (score >= 50) return "#60a5fa";
  if (score >= 25) return "#facc15";
  return "#f87171";
}
function trustLabel(score) {
  if (score >= 75) return "🟢 Trusted";
  if (score >= 50) return "🔵 Established";
  if (score >= 25) return "🟡 Building";
  return "🔴 Restricted";
}
function statusBadge(status) {
  const map = {
    approved:      "background:#16a34a22;color:#4ade80;border:1px solid #4ade8044",
    manual_review: "background:#ca8a0422;color:#facc15;border:1px solid #facc1544",
    rejected:      "background:#dc262622;color:#f87171;border:1px solid #f8717144",
    active:        "background:#1d4ed822;color:#60a5fa;border:1px solid #60a5fa44",
    cancelled:     "background:#52525222;color:#a1a1aa;border:1px solid #52525244",
    pending:       "background:#7c3aed22;color:#a78bfa;border:1px solid #a78bfa44",
  };
  const st = map[status] || map.pending;
  return `<span style="padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;${st}">${capitalize(status?.replace("_"," "))}</span>`;
}

// ─── Notification Polling ─────────────────────────────────────────────────────
let _notifPollingId = null;
let _lastUnread = 0;

function startNotifPolling(workerId, badgeEl, dropdownEl) {
  if (!workerId) return;
  async function poll() {
    try {
      const data = await GS.get(`/notifications/unread/${workerId}`);
      const count = data.unread_count || 0;
      if (badgeEl) {
        badgeEl.textContent = count;
        badgeEl.style.display = count > 0 ? "flex" : "none";
      }
      // Show new notification toast if count increased
      if (count > _lastUnread && _lastUnread >= 0 && document.visibilityState === "visible") {
        const notifs = await GS.get(`/notifications/${workerId}?limit=1`);
        if (notifs.notifications?.[0] && !notifs.notifications[0].is_read) {
          const n = notifs.notifications[0];
          toast(`${n.icon || ""} ${n.title}: ${n.message}`, "info", 5000);
        }
      }
      _lastUnread = count;
    } catch(e) {}
  }
  poll();
  _notifPollingId = setInterval(poll, 15000); // Poll every 15s
}

function stopNotifPolling() {
  if (_notifPollingId) clearInterval(_notifPollingId);
}

// ─── Hardware Telemetry (GPS + Accelerometer) ─────────────────────────────────
let _telemetry = { lat: null, lon: null, motion_var: 0 };
let _motionSamples = [];
let _telemetryInterval = null;

function enableDeviceTelemetry(workerId) {
  if (!navigator.geolocation) {
    toast("Geolocation is not supported by your browser", "error");
    return;
  }
  
  // Start GPS tracking
  navigator.geolocation.watchPosition((pos) => {
    _telemetry.lat = pos.coords.latitude;
    _telemetry.lon = pos.coords.longitude;
  }, (err) => {
    console.warn("GPS tracking error:", err);
  }, { enableHighAccuracy: true });

  // Start Accelerometer tracking
  if (window.DeviceMotionEvent) {
    window.addEventListener('devicemotion', (event) => {
      if (event.acceleration) {
        const ax = event.acceleration.x || 0;
        const ay = event.acceleration.y || 0;
        const az = event.acceleration.z || 0;
        const magnitude = Math.sqrt(ax*ax + ay*ay + az*az);
        _motionSamples.push(magnitude);
        if (_motionSamples.length > 50) _motionSamples.shift(); // keep last 50
        
        // Calculate variance roughly
        const mean = _motionSamples.reduce((a,b)=>a+b,0) / _motionSamples.length;
        _telemetry.motion_var = _motionSamples.reduce((a,b) => a + Math.pow(b - mean, 2), 0) / _motionSamples.length;
      }
    });
  } else {
    console.warn("DeviceMotionEvent not supported.");
  }

  // Heartbeat to server
  if (_telemetryInterval) clearInterval(_telemetryInterval);
  _telemetryInterval = setInterval(() => {
    if (_telemetry.lat && workerId) {
      _telemetry.timestamp = Date.now();
      GS.post(`/workers/${workerId}/telemetry`, _telemetry).catch(console.warn);
    }
  }, 15000); // 15 seconds
  
  toast("Live Telemetry Active. You are fully protected.", "success");
}

async function loadNotifications(workerId, containerEl, badgeEl) {
  try {
    const data = await GS.get(`/notifications/${workerId}?limit=20`);
    if (badgeEl) {
      badgeEl.textContent = data.unread_count;
      badgeEl.style.display = data.unread_count > 0 ? "flex" : "none";
    }
    if (containerEl) {
      containerEl.innerHTML = data.notifications.length === 0
        ? `<div style="padding:20px;text-align:center;color:#94a3b8">No notifications yet</div>`
        : data.notifications.map(n => `
          <div style="padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.06);background:${n.is_read?"transparent":"rgba(99,102,241,0.08)"}">
            <div style="display:flex;align-items:center;gap:10px">
              <span style="font-size:20px">${n.icon || "ℹ️"}</span>
              <div style="flex:1;min-width:0">
                <div style="color:#f1f5f9;font-size:13px;font-weight:600">${n.title}</div>
                <div style="color:#94a3b8;font-size:12px;margin-top:2px;white-space:normal">${n.message}</div>
                <div style="color:#64748b;font-size:11px;margin-top:4px">${formatTimeAgo(n.logged_at)}</div>

              </div>
              ${n.amount ? `<div style="color:#4ade80;font-weight:700;font-size:14px;white-space:nowrap">${formatINR(n.amount)}</div>` : ""}
            </div>
          </div>`).join("");
    }
    // Mark all as read after viewing
    if (data.unread_count > 0) {
      await GS.post("/notifications/mark-read", { worker_id: workerId });
      if (badgeEl) badgeEl.style.display = "none";
      _lastUnread = 0;
    }
  } catch(e) { console.warn("Notifications error:", e); }
}

// ─── Loading Spinner ──────────────────────────────────────────────────────────
function showLoader(el, msg = "Loading...") {
  if (el) el.innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;gap:12px;padding:40px;color:#94a3b8">
      <div style="width:32px;height:32px;border:3px solid #1e293b;border-top-color:#6366f1;border-radius:50%;animation:spin 0.8s linear infinite"></div>
      <span>${msg}</span>
    </div>`;
  if (!document.getElementById("gs-spin-style")) {
    const s = document.createElement("style");
    s.id = "gs-spin-style";
    s.textContent = "@keyframes spin{to{transform:rotate(360deg)}}";
    document.head.appendChild(s);
  }
}

function showError(el, msg) {
  if (el) el.innerHTML = `<div style="padding:20px;text-align:center;color:#f87171">⚠️ ${msg}</div>`;
}

// ─── AI Assistant Bot UI Phase 2.1 ───────────────────────────────────────────
function initGigPulseBot() {
  if (document.getElementById("gp-bot-widget")) return;

  const botStyles = document.createElement("style");
  botStyles.textContent = `
    .gp-bot-widget { position: fixed; bottom: 24px; right: 24px; z-index: 1000; font-family: 'Inter', sans-serif; }
    .gp-bot-btn { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; box-shadow: 0 10px 25px rgba(99,102,241,0.5); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 28px; color: white; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .gp-bot-btn:hover { transform: scale(1.1); box-shadow: 0 15px 35px rgba(99,102,241,0.6); }
    .gp-bot-btn.pulse { animation: gpBotPulse 2s infinite; }
    @keyframes gpBotPulse { 0% { box-shadow: 0 0 0 0 rgba(99,102,241,0.7); } 70% { box-shadow: 0 0 0 15px rgba(99,102,241,0); } 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); } }
    
    .gp-bot-window { position: absolute; bottom: 80px; right: 0; width: 350px; height: 480px; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); border: 1px solid rgba(99,102,241,0.3); border-radius: 24px; display: none; flex-direction: column; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); transform-origin: bottom right; transform: scale(0.9); opacity: 0; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .gp-bot-window.open { display: flex; transform: scale(1); opacity: 1; }
    
    html[data-theme="light"] .gp-bot-window { background: rgba(255, 255, 255, 0.9); border-color: rgba(99,102,241,0.2); box-shadow: 0 25px 50px -12px rgba(99,102,241,0.2); }
    html[data-theme="light"] .gp-bot-msg.bot { background: #f1f5f9; color: #0f172a; border: 1px solid #e2e8f0; }
    html[data-theme="light"] .gp-bot-msg.user { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; }
    html[data-theme="light"] .gp-bot-input { background: #fff; color: #0f172a; border-top: 1px solid #e2e8f0; }
    
    .gp-bot-header { background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(15,23,42,0.8)); padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(99,102,241,0.2); }
    html[data-theme="light"] .gp-bot-header { background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(255,255,255,0.9)); }
    .gp-bot-title { font-weight: 700; color: var(--text); display: flex; align-items: center; gap: 8px; }
    .gp-bot-close { background: none; border: none; color: var(--muted); cursor: pointer; font-size: 20px; transition: color 0.2s; }
    .gp-bot-close:hover { color: var(--text); }
    
    .gp-bot-body { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
    .gp-bot-body::-webkit-scrollbar { width: 6px; }
    .gp-bot-body::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 10px; }
    
    .gp-bot-msg { max-width: 85%; padding: 12px 16px; font-size: 13.5px; line-height: 1.5; border-radius: 18px; position: relative; animation: msgFadeIn 0.3s ease; }
    @keyframes msgFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .gp-bot-msg.bot { align-self: flex-start; background: rgba(30, 41, 59, 0.8); color: #f8fafc; border-bottom-left-radius: 4px; border: 1px solid rgba(255,255,255,0.05); }
    .gp-bot-msg.user { align-self: flex-end; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border-bottom-right-radius: 4px; box-shadow: 0 4px 12px rgba(99,102,241,0.3); }
    
    .gp-bot-typing { display: flex; gap: 4px; padding: 12px 16px; align-items: center; align-self: flex-start; background: rgba(30, 41, 59, 0.8); border-radius: 18px; border-bottom-left-radius: 4px; display: none; }
    html[data-theme="light"] .gp-bot-typing { background: #f1f5f9; }
    .gp-bot-typing span { width: 6px; height: 6px; background: var(--muted); border-radius: 50%; animation: typingBounce 1.4s infinite ease-in-out both; }
    .gp-bot-typing span:nth-child(1) { animation-delay: -0.32s; }
    .gp-bot-typing span:nth-child(2) { animation-delay: -0.16s; }
    @keyframes typingBounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); background: var(--primary); } }
    
    .gp-bot-footer { padding: 14px 20px; border-top: 1px solid var(--border); background: rgba(2, 8, 23, 0.5); }
    .gp-bot-input-grp { display: flex; gap: 10px; background: rgba(15, 23, 42, 0.6); padding: 4px 4px 4px 16px; border-radius: 30px; border: 1px solid var(--border); transition: border-color 0.3s; }
    .gp-bot-input-grp:focus-within { border-color: var(--primary); }
    html[data-theme="light"] .gp-bot-input-grp { background: #f8fafc; border-color: #cbd5e1; }
    .gp-bot-input { flex: 1; border: none; background: transparent; color: var(--text); font-family: 'Inter', sans-serif; font-size: 14px; outline: none; }
    .gp-bot-send { width: 36px; height: 36px; border-radius: 50%; background: var(--primary); border: none; color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: transform 0.2s; }
    .gp-bot-send:hover { transform: scale(1.05); }
    .gp-bot-send:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
    
    @media (max-width: 600px) {
      .gp-bot-window { width: calc(100vw - 40px); right: -10px; bottom: 70px; height: 450px; }
    }
  `;
  document.head.appendChild(botStyles);

  const container = document.createElement("div");
  container.className = "gp-bot-widget";
  container.id = "gp-bot-widget";
  container.innerHTML = `
    <button class="gp-bot-btn pulse" id="gpBotToggle">🤖</button>
    <div class="gp-bot-window" id="gpBotWindow">
      <div class="gp-bot-header">
        <div class="gp-bot-title"><span style="font-size:24px">🤖</span> GigPulse AI</div>
        <button class="gp-bot-close" id="gpBotClose">✕</button>
      </div>
      <div class="gp-bot-body" id="gpBotBody">
        <div class="gp-bot-msg bot">Hi! I'm your GigPulse AI Assistant. How can I protect your earnings today?</div>
        <div class="gp-bot-typing" id="gpBotTyping"><span></span><span></span><span></span></div>
      </div>
      <div class="gp-bot-footer">
        <form id="gpBotForm" class="gp-bot-input-grp">
          <input type="text" class="gp-bot-input" id="gpBotInput" placeholder="Ask about claims, policies..." autocomplete="off">
          <button type="submit" class="gp-bot-send" id="gpBotSend">↗</button>
        </form>
      </div>
    </div>
  `;
  document.body.appendChild(container);

  const toggle = document.getElementById("gpBotToggle");
  const win = document.getElementById("gpBotWindow");
  const close = document.getElementById("gpBotClose");
  const form = document.getElementById("gpBotForm");
  const input = document.getElementById("gpBotInput");
  const body = document.getElementById("gpBotBody");
  const typing = document.getElementById("gpBotTyping");

  function toggleOpen() {
    win.classList.toggle("open");
    toggle.classList.remove("pulse");
    if(win.classList.contains("open")) { input.focus(); }
  }

  toggle.addEventListener("click", toggleOpen);
  close.addEventListener("click", () => win.classList.remove("open"));

  function addMsg(text, sender) {
    const d = document.createElement("div");
    d.className = `gp-bot-msg ${sender}`;
    d.textContent = text;
    body.insertBefore(d, typing);
    body.scrollTop = body.scrollHeight;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const txt = input.value.trim();
    if (!txt) return;
    
    input.value = "";
    addMsg(txt, "user");
    
    typing.style.display = "flex";
    body.scrollTop = body.scrollHeight;
    
    try {
      const sess = Session.get();
      const wId = sess ? (sess.worker_id || sess.id) : null;
      const res = await GS.post("/bot/chat", { message: txt, worker_id: wId });
      typing.style.display = "none";
      if (res && res.response) {
        // Strip out the prompt text if HD free model returns it by mistake
        let finalTxt = res.response;
        if(finalTxt.includes("<|assistant|>")) {
            finalTxt = finalTxt.split("<|assistant|>").pop().strip();
        }
        addMsg(finalTxt, "bot");
      } else {
        addMsg("Sorry, I had trouble connecting. You can try again.", "bot");
      }
    } catch(err) {
      typing.style.display = "none";
      addMsg("I'm experiencing an error connecting to my servers. Please try again later.", "bot");
    }
  });
}

// Auto-init bot on all pages
function attemptBotInit() {
    setTimeout(() => {
        initGigPulseBot();
    }, 1000);
}

if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', attemptBotInit);
} else {
    attemptBotInit();
}