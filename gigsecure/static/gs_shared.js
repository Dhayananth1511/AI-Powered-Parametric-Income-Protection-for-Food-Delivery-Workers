// ─────────────────────────────────────────────────────────────────────────────
// GigSecure Shared JS — Phase 2
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
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
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
    if (!s) { window.location.href = "gigsecure_login.html"; return null; }
    return s;
  },
  logout() {
    this.clear();
    window.location.href = "gigsecure_login.html";
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
function formatDate(d)       { return d ? new Date(d).toLocaleDateString("en-IN", { day:"numeric", month:"short", year:"numeric" }) : "—"; }
function formatTime(d)       { return d ? new Date(d).toLocaleTimeString("en-IN", { hour:"2-digit", minute:"2-digit" }) : "—"; }
function formatDateTime(d)   { return d ? `${formatDate(d)}, ${formatTime(d)}` : "—"; }
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
                <div style="color:#64748b;font-size:11px;margin-top:4px">${n.time_ago}</div>
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