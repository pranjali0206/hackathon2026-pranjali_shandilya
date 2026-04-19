import streamlit as st
import requests
import json
import os
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=3000, limit=200, key="live_refresh")

st.set_page_config(
    page_title="ShopWave AI Support",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #0d1117;
}

[data-testid="stSidebar"] {
    background: #0a0e16;
    border-right: 1px solid #1e2433;
}

/* ── Hero ── */
.hero {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    text-align: center;
}
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: #8892a4;
    font-size: 0.88rem;
    margin-top: 8px;
}
.hero-tags {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 16px;
}
.hero-tag {
    background: #1a2235;
    border: 1px solid #2a3650;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 0.72rem;
    color: #8892a4;
}

/* ── Metric cards ── */
.metric-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
}
.metric-number {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
    margin-top: 8px;
}
.metric-label {
    font-size: 0.7rem;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #8892a4;
}
.metric-accent {
    height: 3px;
    border-radius: 3px;
    margin-top: 14px;
}

/* ── Live banner ── */
.live-banner {
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ── Ticket cards ── */
.ticket-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}
.ticket-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 12px 0 0 12px;
}
.tc-resolved::before  { background: #22c55e; }
.tc-escalated::before { background: #ef4444; }
.tc-refunded::before  { background: #f59e0b; }
.tc-pending::before   { background: #3b82f6; }

.ticket-id    { font-size: 0.75rem; color: #3b82f6; font-weight: 600; letter-spacing: 0.5px; }
.ticket-email { font-size: 0.8rem;  color: #8892a4; margin-top: 2px; }
.ticket-subject { font-size: 0.95rem; font-weight: 600; color: #ffffff; margin-top: 6px; }
.ticket-resolution {
    font-size: 0.82rem;
    color: #8892a4;
    margin-top: 10px;
    line-height: 1.6;
    padding-left: 12px;
    border-left: 2px solid #1e2d45;
}

/* ── Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.badge-resolved  { background: #052e16; color: #22c55e; border: 1px solid #166534; }
.badge-escalated { background: #2d0a0a; color: #ef4444; border: 1px solid #7f1d1d; }
.badge-refunded  { background: #2d1f0a; color: #f59e0b; border: 1px solid #78350f; }
.badge-pending   { background: #0a1628; color: #3b82f6; border: 1px solid #1e3a5f; }
.badge-vip       { background: #2d1f0a; color: #f59e0b; border: 1px solid #78350f; }
.badge-premium   { background: #0a1628; color: #3b82f6; border: 1px solid #1e3a5f; }
.badge-standard  { background: #1a2235; color: #8892a4; border: 1px solid #2a3650; }

/* ── Live dot ── */
.live-dot {
    display: inline-block;
    width: 6px; height: 6px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 5px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.4; }
}

/* ── Sidebar ── */
.status-row { display:flex; align-items:center; gap:8px; margin:5px 0; font-size:0.83rem; color:#8892a4; }
.sdot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.sdot-green { background:#22c55e; }

.progress-bg   { background: #1e2d45; border-radius:6px; height:5px; margin-top:8px; overflow:hidden; }
.progress-fill { height:100%; border-radius:6px; background: #3b82f6; transition: width 0.8s ease; }

/* ── Section title ── */
.section-title {
    font-size: 0.68rem;
    font-weight: 600;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d45;
}

/* ── Tool chip ── */
.tool-chip {
    display: inline-block;
    background: #1a2235;
    color: #3b82f6;
    border: 1px solid #2a3650;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.68rem;
    margin: 2px;
}

/* ── Response box ── */
.response-box {
    background: #0d1f12;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: 16px 18px;
    color: #d1fae5;
    line-height: 1.7;
    font-size: 0.85rem;
    margin-top: 12px;
}

/* ── Summary card ── */
.summary-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
    font-size: 0.78rem;
    color: #8892a4;
}

/* ── Streamlit overrides ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }

.stTabs [data-baseweb="tab-list"] {
    background: #131929;
    border-radius: 10px;
    padding: 4px;
    gap: 3px;
    border: 1px solid #1e2d45;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #8892a4 !important;
    font-weight: 500;
    font-size: 0.82rem !important;
}
.stTabs [aria-selected="true"] {
    background: #1e2d45 !important;
    color: #ffffff !important;
}
.stTextInput input, .stTextArea textarea {
    background: #131929 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}
.stButton button {
    background: #3b82f6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    width: 100% !important;
    padding: 10px !important;
}
.stButton button:hover {
    background: #2563eb !important;
}
details summary { color: #8892a4 !important; font-size: 0.82rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────
audit_path = "logs/audit_log.json"
results = []
st.cache_data.clear()
if os.path.exists(audit_path):
    with open(audit_path) as f:
        try:
            results = json.load(f)
        except:
            results = []

total     = len(results)
resolved  = sum(1 for r in results if r.get("status") == "resolved")
escalated = sum(1 for r in results if r.get("status") == "escalated")
refunds   = sum(1 for r in results if r.get("status") == "refunded")
pct       = int((resolved / total * 100) if total > 0 else 0)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 14px'>
        <div style='font-size:2.2rem'>🛍️</div>
        <div style='font-size:1.1rem;font-weight:700;color:#ffffff;margin-top:6px'>ShopWave</div>
        <div style='font-size:0.68rem;color:#8892a4;margin-top:2px;letter-spacing:1px'>AI SUPPORT AGENT</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-title' style='margin-top:6px'>System Status</div>", unsafe_allow_html=True)
    for label in ["FastAPI — Online", "Groq LLM — Connected", "16 Tools — Ready"]:
        st.markdown(f"<div class='status-row'><div class='sdot sdot-green'></div>{label}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title' style='margin-top:18px'>Tech Stack</div>", unsafe_allow_html=True)
    for icon, text in [("🧠","llama-3.1-8b-instant"),("⚡","ReAct Agent Loop"),("🔧","FastAPI + Uvicorn"),("🐳","Docker Ready")]:
        st.markdown(f"<div class='status-row'><span>{icon}</span><span>{text}</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title' style='margin-top:18px'>Resolution Progress</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color:#ffffff;font-size:0.83rem;font-weight:600'>{resolved} <span style='color:#8892a4;font-weight:400'>of {total} resolved</span></div>
    <div class='progress-bg'><div class='progress-fill' style='width:{pct}%'></div></div>
    <div style='color:#8892a4;font-size:0.7rem;margin-top:5px'>{pct}% complete</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#8892a4;font-size:0.7rem;text-align:center'><span class='live-dot'></span>auto-refresh every 3s</div>", unsafe_allow_html=True)
    if st.button("⟳ Refresh Now"):
        st.rerun()

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'>🛍️ ShopWave AI Customer Support</div>
    <div class='hero-sub'>Autonomous AI agent · Groq llama-3.1-8b-instant · ReAct Loop · 16 specialized tools</div>
    <div style='margin-top:10px;color:#8892a4;font-size:0.8rem'><span class='live-dot'></span>Live dashboard — updates every 3 seconds</div>
    <div class='hero-tags'>
        <span class='hero-tag'>llama-3.1-8b-instant</span>
        <span class='hero-tag'>16 tools</span>
        <span class='hero-tag'>FastAPI</span>
        <span class='hero-tag'>Streamlit</span>
        <span class='hero-tag'>Docker</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
metrics = [
    (c1, total,     "Total Tickets",  "📋", "#3b82f6"),
    (c2, resolved,  "Resolved",       "✅", "#22c55e"),
    (c3, escalated, "Escalated",      "🚨", "#ef4444"),
    (c4, refunds,   "Refunds",        "💰", "#f59e0b"),
]
for col, val, label, icon, color in metrics:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size:1.2rem'>{icon}</div>
            <div class='metric-number'>{val}</div>
            <div class='metric-label'>{label}</div>
            <div class='metric-accent' style='background:{color}'></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Live Status Banner ────────────────────────────────────────
live_path = "logs/live_status.json"
if os.path.exists(live_path):
    with open(live_path) as f:
        try:
            live = json.load(f)
        except:
            live = {}
    if live:
        prog     = live.get("progress", 0)
        total_t  = live.get("total", 20)
        t_id     = live.get("current_ticket", "")
        t_email  = live.get("current_email", "")
        t_subj   = live.get("current_subject", "")
        l_status = live.get("status", "")
        pct_live = int(prog / total_t * 100) if total_t > 0 else 0

        if l_status == "processing":
            bg, border, icon, label, dot = "#0a1628", "#1e3a5f", "⚙️", "PROCESSING", "<span class='live-dot'></span>"
        elif l_status == "done":
            bg, border, icon, label, dot = "#0d1f12", "#166534", "✅", "COMPLETED", ""
        elif l_status == "complete":
            bg, border, icon, label, dot = "#0d1f12", "#166534", "🏁", "ALL DONE", ""
        else:
            bg, border, icon, label, dot = "#131929", "#1e2d45", "⏳", "WAITING", ""

        st.markdown(f"""
        <div style='background:{bg};border:1px solid {border};border-radius:12px;padding:16px 20px;margin-bottom:18px'>
            <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px'>
                <div>
                    <div style='font-size:0.68rem;color:#8892a4;letter-spacing:1.5px;margin-bottom:4px'>{dot}{label}</div>
                    <div style='font-size:0.95rem;font-weight:600;color:#ffffff'>{icon} {t_id}
                        <span style='color:#8892a4;font-size:0.8rem;font-weight:400;margin-left:6px'>{t_email}</span>
                    </div>
                    <div style='font-size:0.82rem;color:#8892a4;margin-top:3px'>{t_subj}</div>
                </div>
                <div style='text-align:right'>
                    <div style='font-size:1.4rem;font-weight:700;color:#ffffff'>{prog}<span style='font-size:0.9rem;color:#8892a4'>/{total_t}</span></div>
                    <div style='font-size:0.68rem;color:#8892a4'>{pct_live}% complete</div>
                </div>
            </div>
            <div style='background:#1e2d45;border-radius:6px;height:4px;margin-top:12px;overflow:hidden'>
                <div style='height:100%;border-radius:6px;background:#3b82f6;width:{pct_live}%;transition:width 0.8s ease'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🎫  Submit New Ticket", "📊  Ticket Dashboard"])

# ── Tab 1 ─────────────────────────────────────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("<div class='section-title'>New Support Ticket</div>", unsafe_allow_html=True)
        email    = st.text_input("Customer Email", placeholder="customer@email.com")
        subject  = st.text_input("Subject", placeholder="e.g. Refund request for headphones")
        body     = st.text_area("Message", placeholder="Describe your issue in detail...", height=150)
        submitted = st.button("🚀 Submit to AI Agent")
    with right:
        st.markdown("<div class='section-title'>How it works</div>", unsafe_allow_html=True)
        for icon, text in [
            ("🧠", "Agent reads your ticket"),
            ("🔍", "Looks up your order & account"),
            ("⚖️", "Checks ShopWave policies"),
            ("🛠️", "Calls the right tools"),
            ("✅", "Returns resolution instantly"),
        ]:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;padding:9px 12px;margin-bottom:5px;
                background:#131929;border-radius:8px;border:1px solid #1e2d45'>
                <span style='font-size:1.1rem'>{icon}</span>
                <span style='color:#8892a4;font-size:0.83rem'>{text}</span>
            </div>""", unsafe_allow_html=True)

    if submitted:
        if not email or not subject or not body:
            st.warning("⚠️ Please fill in all fields.")
        else:
            with st.spinner("🤖 Agent is thinking..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/process-ticket",
                        json={"customer_email": email, "subject": subject, "body": body},
                        timeout=120
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Ticket processed successfully!")
                        st.markdown(f"<div class='response-box'>{data.get('resolution','No response')}</div>", unsafe_allow_html=True)
                        steps = data.get("steps", [])
                        if steps:
                            with st.expander("🔍 View agent reasoning steps"):
                                for i, step in enumerate(steps, 1):
                                    st.markdown(f"""
                                    <div style='display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #1e2d45;
                                        color:#8892a4;font-size:0.8rem'>
                                        <div style='background:#1a2235;color:#3b82f6;border-radius:50%;
                                            width:20px;height:20px;display:flex;align-items:center;justify-content:center;
                                            font-size:0.65rem;font-weight:700;flex-shrink:0'>{i}</div>
                                        <div>{step}</div>
                                    </div>""", unsafe_allow_html=True)
                    else:
                        st.error(f"API error {response.status_code}")
                except Exception as e:
                    st.error(f"Could not connect to API: {e}")

# ── Tab 2 ─────────────────────────────────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div style='text-align:center;padding:60px;color:#8892a4'>
            <div style='font-size:3rem'>📭</div>
            <div style='margin-top:12px;font-size:0.95rem;font-weight:600;color:#ffffff'>No tickets yet</div>
            <div style='margin-top:5px;font-size:0.8rem'>Run main.py or submit a ticket above</div>
        </div>""", unsafe_allow_html=True)
    else:
        fa, fb, fc = st.columns([1, 1, 1])
        status_filter = fa.selectbox("Filter by status", ["All", "resolved", "escalated", "refunded", "pending"])
        tier_filter   = fb.selectbox("Filter by tier",   ["All", "vip", "premium", "standard"])
        search        = fc.text_input("🔍 Search", placeholder="ticket ID or email...")

        filtered = results
        if status_filter != "All":
            filtered = [r for r in filtered if r.get("status") == status_filter]
        if tier_filter != "All":
            filtered = [r for r in filtered if r.get("customer_tier","").lower() == tier_filter]
        if search:
            filtered = [r for r in filtered if
                        search.lower() in str(r.get("ticket_id","")).lower() or
                        search.lower() in str(r.get("customer_email","")).lower()]

        sa, sb, sc, sd = st.columns(4)
        sa.markdown(f"<div class='summary-card'>🔎 Showing<br><b style='font-size:1.3rem;color:#ffffff'>{len(filtered)}</b></div>", unsafe_allow_html=True)
        sb.markdown(f"<div class='summary-card'>✅ Resolved<br><b style='font-size:1.3rem;color:#22c55e'>{resolved}</b></div>", unsafe_allow_html=True)
        sc.markdown(f"<div class='summary-card'>🚨 Escalated<br><b style='font-size:1.3rem;color:#ef4444'>{escalated}</b></div>", unsafe_allow_html=True)
        sd.markdown(f"<div class='summary-card'>💰 Refunded<br><b style='font-size:1.3rem;color:#f59e0b'>{refunds}</b></div>", unsafe_allow_html=True)

        st.markdown(f"<div style='color:#8892a4;font-size:0.73rem;margin:14px 0 4px'><span class='live-dot'></span>Showing {len(filtered)} of {total} tickets — auto-refreshing every 3s</div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#1e2d45;margin-bottom:16px'>", unsafe_allow_html=True)

        for r in filtered:
            status    = r.get("status", "pending")
            tier      = r.get("customer_tier", "standard").lower()
            t_id      = r.get("ticket_id", "N/A")
            email_r   = r.get("customer_email", "N/A")
            subject_r = r.get("subject", "No subject")
            resolution= r.get("resolution", "Pending...")
            steps     = r.get("steps", [])
            confidence= r.get("confidence", 0)

            status_icons  = {"resolved":"✅","escalated":"🚨","refunded":"💰","pending":"⏳"}
            status_labels = {"resolved":"Resolved","escalated":"Escalated","refunded":"Refunded","pending":"Pending"}
            tier_icons    = {"vip":"👑","premium":"🔵","standard":"⚪"}

            s_icon  = status_icons.get(status, "⏳")
            s_label = status_labels.get(status, status.title())
            t_icon  = tier_icons.get(tier, "⚪")
            conf_color = "#22c55e" if confidence >= 80 else "#f59e0b" if confidence >= 60 else "#ef4444"

            st.markdown(f"""
            <div class='ticket-card tc-{status}'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px'>
                    <div>
                        <div class='ticket-id'>{t_id}</div>
                        <div class='ticket-email'>📧 {email_r}</div>
                        <div class='ticket-subject'>{subject_r}</div>
                    </div>
                    <div style='display:flex;gap:6px;flex-wrap:wrap;align-items:center'>
                        <span class='badge badge-{status}'>{s_icon} {s_label}</span>
                        <span class='badge badge-{tier}'>{t_icon} {tier.upper()}</span>
                        <span style='font-size:0.68rem;color:{conf_color};background:#1a2235;border:1px solid #2a3650;border-radius:6px;padding:2px 8px'>{confidence}% conf</span>
                        <span style='font-size:0.68rem;color:#8892a4'>🔧 {len(steps)} steps</span>
                    </div>
                </div>
                <div class='ticket-resolution'>{str(resolution)[:220]}{'...' if len(str(resolution)) > 220 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

            if steps:
                with st.expander(f"🔍 {len(steps)} agent steps — {t_id}"):
                    tools_used = []
                    for i, step in enumerate(steps, 1):
                        tool_name = step.get("tool", "") if isinstance(step, dict) else str(step)
                        args      = step.get("args", {}) if isinstance(step, dict) else {}
                        if tool_name:
                            tools_used.append(tool_name)
                        st.markdown(f"""
                        <div style='display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #1e2d45;font-size:0.78rem'>
                            <div style='background:#1a2235;color:#3b82f6;border-radius:50%;
                                width:20px;height:20px;display:flex;align-items:center;justify-content:center;
                                font-size:0.65rem;font-weight:700;flex-shrink:0'>{i}</div>
                            <div style='color:#22c55e'>{tool_name}</div>
                            <div style='color:#8892a4'>{str(args)[:80]}</div>
                        </div>""", unsafe_allow_html=True)
                    if tools_used:
                        st.markdown("<div style='margin-top:8px'>" +
                            "".join([f"<span class='tool-chip'>{t}</span>" for t in tools_used]) +
                            "</div>", unsafe_allow_html=True)