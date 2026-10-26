:root {
  color-scheme: dark;
  --bg: #080d18;
  --surface: #101a2b;
  --surface-2: #0b1322;
  --border: #263650;
  --text: #e7edf8;
  --muted: #91a0b8;
  --accent: #36e0b1;
  --warning: #ffc66d;
  --danger: #ff7c8a;
}
* { box-sizing: border-box; }
body { margin: 0; background: radial-gradient(ellipse at top right, #14233a 0, var(--bg) 48%); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; min-height: 100vh; }
.topbar { min-height: 76px; padding: 18px max(5%, calc((100% - 1160px)/2)); border-bottom: 1px solid #243047; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; background: rgba(8,13,24,.82); }
.brand { color: var(--text); text-decoration: none; font-size: 22px; font-weight: 800; letter-spacing: -.5px; }
.brand-icon { margin-right: 7px; }
.accent { color: var(--accent); }
.connection { display: flex; align-items: center; gap: 9px; color: var(--muted); font-size: 13px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--warning); box-shadow: 0 0 12px currentColor; }
.connection.online { color: var(--accent); }
.connection.online .status-dot { background: var(--accent); }
.connection.offline { color: var(--danger); }
.connection.offline .status-dot { background: var(--danger); }
.container { max-width: 1160px; padding: 38px 22px 54px; margin: auto; }
.hero { display: flex; justify-content: space-between; align-items: end; gap: 24px; margin-bottom: 24px; }
.eyebrow { font-size: 11px; letter-spacing: 2px; font-weight: 800; color: var(--accent); margin: 0 0 12px; }
h1 { font-size: clamp(29px, 4vw, 40px); line-height: 1.15; letter-spacing: -1.3px; margin: 0 0 12px; }
.subtitle, .muted { color: var(--muted); line-height: 1.65; }
.subtitle { max-width: 690px; margin: 0; }
.notice { border: 1px solid #5d4b2b; background: rgba(255,198,109,.07); color: #d9c7a5; padding: 14px 16px; border-radius: 12px; font-size: 13px; line-height: 1.6; margin: 22px 0; }
.notice strong { color: var(--warning); }
.metrics { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 15px; margin: 22px 0; }
.metric-card, .panel { background: linear-gradient(145deg, rgba(16,26,43,.97), rgba(12,20,34,.97)); border: 1px solid var(--border); border-radius: 16px; }
.metric-card { padding: 20px; min-width: 0; }
.metric-label { color: var(--muted); font-size: 13px; }
.metric-value { font-size: 29px; font-weight: 800; margin: 12px 0 8px; overflow-wrap: anywhere; }
.metric-foot { color: #72839d; font-size: 11px; }
.good { color: var(--accent); }
.warning { color: var(--warning); }
.content-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 18px; }
.panel { padding: 22px; min-width: 0; }
.panel-heading { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 22px; }
.panel-icon { display: grid; place-items: center; flex: 0 0 40px; height: 40px; border-radius: 11px; background: rgba(54,224,177,.1); color: var(--accent); font-size: 24px; }
h2 { margin: 1px 0 6px; font-size: 18px; letter-spacing: -.3px; }
.panel-heading p { margin: 0; color: var(--muted); font-size: 13px; line-height: 1.5; }
label { display: block; font-size: 13px; font-weight: 650; margin: 16px 0 8px; }
input, select { width: 100%; padding: 13px 14px; border-radius: 9px; border: 1px solid #34445e; background: var(--surface-2); color: var(--text); font-size: 14px; outline: none; }
input:focus, select:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(54,224,177,.1); }
.button { border: 0; border-radius: 9px; padding: 12px 15px; font-size: 13px; font-weight: 750; cursor: pointer; transition: transform .15s ease, opacity .15s ease, border-color .15s ease; }
.button:hover { transform: translateY(-1px); }
.button:disabled { opacity: .55; cursor: wait; transform: none; }
.button-primary { width: 100%; display: flex; align-items: center; justify-content: space-between; margin-top: 18px; background: var(--accent); color: #06130f; padding: 14px 16px; }
.button-secondary { background: #1a2940; color: var(--text); border: 1px solid #34445e; }
.refresh-button { white-space: nowrap; }
.small-note { color: #8595ad; font-size: 11px; line-height: 1.6; }
.panel > .small-note { margin: 15px 0 0; }
pre { min-height: 150px; max-height: 330px; overflow: auto; white-space: pre-wrap; overflow-wrap: anywhere; background: #080d18; border: 1px solid #202e44; border-radius: 10px; padding: 15px; color: #b7c8df; font-size: 12px; line-height: 1.65; }
.response-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.activity-panel { margin-top: 18px; }
.activity-heading { justify-content: space-between; align-items: center; }
.activity-heading p { margin-top: 5px; }
.compact { padding: 9px 12px; font-size: 12px; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; text-align: left; font-size: 12px; }
th { color: #8495ae; font-weight: 650; text-transform: uppercase; letter-spacing: .7px; font-size: 10px; }
th, td { padding: 13px 12px; border-bottom: 1px solid #243047; white-space: nowrap; }
tbody tr:last-child td { border-bottom: 0; }
.decision { font-weight: 800; }
.decision.allow { color: var(--accent); }
.decision.flag { color: var(--warning); }
.decision.block { color: var(--danger); }
.empty-row td { color: #8190a7; text-align: center; padding: 25px 10px; }
footer { text-align: center; color: #71819a; font-size: 11px; border-top: 1px solid #243047; padding: 24px 16px; }
@media (max-width: 800px) { .metrics { grid-template-columns: repeat(2, minmax(0,1fr)); } .content-grid { grid-template-columns: 1fr; } .hero { align-items: flex-start; flex-direction: column; } }
@media (max-width: 460px) { .container { padding: 27px 14px 38px; } .topbar { padding: 16px; } .metric-card { padding: 15px; } .metric-value { font-size: 25px; } .panel { padding: 17px; } .activity-heading { align-items: flex-start; flex-direction: column; } }
