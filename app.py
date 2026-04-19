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
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-4px); }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .hero {
        background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(79,70,229,0.2));
        border: 1px solid rgba(124,58,237,0.3);
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 28px;
        text-align: center;
    }
    .hero h1 {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #c4b5fd, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero p { color: rgba(255,255,255,0.5); margin-top: 8px; font-size: 0.95rem; }
    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: rgba(255,255,255,0.5) !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(124,58,237,0.4) !important;
        color: white !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    .ticket-row {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 12px;
    }
    .ticket-row:hover {
        background: rgba(255,255,255,0.07);
        border-color: rgba(167,139,250,0.3);
        transition: all 0.2s;
    }
    .ticket-id {
        font-size: 0.8rem;
        color: #a78bfa;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .ticket-email {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        margin-top: 2px;
    }
    .ticket-subject {
        font-size: 0.95rem;
        color: white;
        font-weight: 500;
        margin-top: 6px;
    }
    .ticket-resolution {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.55);
        margin-top: 8px;
        line-height: 1.6;
        border-left: 3px solid rgba(167,139,250,0.4);
        padding-left: 12px;
    }
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-resolved  { background: rgba(52,211,153,0.15);  color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
    .badge-escalated { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
    .badge-pending   { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
    .badge-vip       { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
    .badge-premium   { background: rgba(96,165,250,0.15);  color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
    .badge-standard  { background: rgba(156,163,175,0.15); color: #9ca3af; border: 1px solid rgba(156,163,175,0.3); }
    .tool-chip {
        display: inline-block;
        background: rgba(167,139,250,0.1);
        color: #c4b5fd;
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.72rem;
        margin: 2px;
    }
    .live-dot {
        display: inline-block;
        width: 7px; height: 7px;
        background: #34d399;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%,100% { opacity:1; transform:scale(1); }
        50%      { opacity:0.4; transform:scale(0.8); }
    }
    .progress-bar-bg {
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        height: 8px;
        margin-top: 6px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #7c3aed, #34d399);
        transition: width 0.5s ease;
    }
    .response-box {
        background: rgba(52,211,153,0.06);
        border: 1px solid rgba(52,211,153,0.2);
        border-radius: 10px;
        padding: 16px;
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
        font-size: 0.9rem;
        margin-top: 12px;
    }
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 7px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.6);
        font-size: 0.85rem;
    }
    .step-num {
        background: rgba(167,139,250,0.2);
        color: #a78bfa;
        border-radius: 50%;
        width: 20px; height: 20px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700;
        flex-shrink: 0;
    }
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255,255,255,0.9);
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; }
    /* Force expander text visible */
    .streamlit-expanderHeader p { color: white !important; }
    details summary { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ───────────────────────────────────────────────
audit_path = "logs/audit_log.json"
results = []
if os.path.exists(audit_path):
    with open(audit_path) as f:
        try:
            results = json.load(f)
        except:
            results = []

total     = len(results)
resolved  = sum(1 for r in results if r.get("status") == "resolved")
escalated = sum(1 for r in results if r.get("status") == "escalated")
refunds   = sum(1 for r in results if "refund" in str(r.get("resolution","")).lower())
pct       = int((resolved / total * 100) if total > 0 else 0)

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
        <div style='font-size:3rem'>🛍️</div>
        <div style='font-size:1.1rem;font-weight:700;color:white'>ShopWave</div>
        <div style='font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:2px'>AI Support Agent</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:rgba(255,255,255,0.4);font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>System Status</div>", unsafe_allow_html=True)
    st.markdown("🟢 &nbsp; **FastAPI** — Online", unsafe_allow_html=True)
    st.markdown("🟢 &nbsp; **Groq LLM** — Connected", unsafe_allow_html=True)
    st.markdown("🟢 &nbsp; **16 Tools** — Ready", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:rgba(255,255,255,0.4);font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>Tech Stack</div>", unsafe_allow_html=True)
    st.markdown("🧠 &nbsp; llama-3.1-8b-instant", unsafe_allow_html=True)
    st.markdown("⚡ &nbsp; ReAct Agent Loop", unsafe_allow_html=True)
    st.markdown("🔧 &nbsp; FastAPI + Uvicorn", unsafe_allow_html=True)
    st.markdown("🐳 &nbsp; Docker Ready", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:rgba(255,255,255,0.4);font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>Resolution Progress</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color:white;font-size:0.85rem'>{resolved} of {total} tickets resolved</div>
    <div class='progress-bar-bg'>
        <div class='progress-bar-fill' style='width:{pct}%'></div>
    </div>
    <div style='color:rgba(255,255,255,0.4);font-size:0.75rem;margin-top:4px'>{pct}% complete</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='color:rgba(255,255,255,0.35);font-size:0.75rem;text-align:center'><span class='live-dot'></span>Auto-refreshing every 3s</div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Now"):
        st.rerun()

# ── Hero ────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <h1>🛍️ ShopWave AI Customer Support</h1>
    <p>Autonomous AI agent · Groq llama-3.1-8b-instant · ReAct Loop · 16 specialized tools</p>
    <p style='margin-top:4px;font-size:0.8rem'>
        <span class='live-dot'></span>
        <span style='color:rgba(255,255,255,0.3)'>Live dashboard — updates every 3 seconds</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ── Metrics ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-number'>{total}</div><div class='metric-label'>📋 Total Tickets</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-number' style='background:linear-gradient(90deg,#34d399,#6ee7b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>{resolved}</div><div class='metric-label'>✅ Resolved</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-number' style='background:linear-gradient(90deg,#f87171,#fca5a5);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>{escalated}</div><div class='metric-label'>🚨 Escalated</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='metric-number' style='background:linear-gradient(90deg,#fbbf24,#fde68a);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>{refunds}</div><div class='metric-label'>💰 Refunds</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🎫  Submit New Ticket", "📊  Ticket Dashboard"])

# ── Tab 1 ───────────────────────────────────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("<div class='section-title'>✍️ New Support Ticket</div>", unsafe_allow_html=True)
        email   = st.text_input("Customer Email", placeholder="customer@email.com")
        subject = st.text_input("Subject", placeholder="e.g. Refund request for headphones")
        body    = st.text_area("Message", placeholder="Describe your issue in detail...", height=160)
        submitted = st.button("🚀 Submit to AI Agent")
    with right:
        st.markdown("<div class='section-title'>💡 How it works</div>", unsafe_allow_html=True)
        for icon, text in [("🧠","Agent reads your ticket"),("🔍","Looks up your order & account"),("⚖️","Checks ShopWave policies"),("🛠️","Calls the right tools"),("✅","Returns resolution instantly")]:
            st.markdown(f"<div class='step-item'><div style='font-size:1.1rem'>{icon}</div><div style='color:rgba(255,255,255,0.7)'>{text}</div></div>", unsafe_allow_html=True)

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
                                    st.markdown(f"<div class='step-item'><div class='step-num'>{i}</div><div>{step}</div></div>", unsafe_allow_html=True)
                    else:
                        st.error(f"API error {response.status_code}")
                except Exception as e:
                    st.error(f"Could not connect: {e}")

# ── Tab 2 ───────────────────────────────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div style='text-align:center;padding:60px;color:rgba(255,255,255,0.3)'>
            <div style='font-size:3rem'>📭</div>
            <div style='margin-top:12px;font-size:1rem'>No tickets processed yet.</div>
            <div style='margin-top:6px;font-size:0.85rem'>Run main.py or submit a ticket above.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Filter bar ───────────────────────────────────────
        fa, fb, fc = st.columns([1, 1, 1])
        status_filter = fa.selectbox("Filter by status", ["All", "resolved", "escalated", "pending"])
        tier_filter   = fb.selectbox("Filter by tier",   ["All", "vip", "premium", "standard"])
        search        = fc.text_input("🔍 Search ticket ID or email")

        filtered = results
        if status_filter != "All":
            filtered = [r for r in filtered if r.get("status") == status_filter]
        if tier_filter != "All":
            filtered = [r for r in filtered if r.get("customer_tier","").lower() == tier_filter]
        if search:
            filtered = [r for r in filtered if
                        search.lower() in str(r.get("ticket_id","")).lower() or
                        search.lower() in str(r.get("customer_email","")).lower()]

        # ── Summary strip ────────────────────────────────────
        sa, sb, sc, sd = st.columns(4)
        sa.markdown(f"<div style='background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;text-align:center;color:white;font-size:0.85rem'>🔎 Showing<br><b style='font-size:1.3rem'>{len(filtered)}</b></div>", unsafe_allow_html=True)
        sb.markdown(f"<div style='background:rgba(52,211,153,0.08);border-radius:10px;padding:12px;text-align:center;color:#34d399;font-size:0.85rem'>✅ Resolved<br><b style='font-size:1.3rem'>{resolved}</b></div>", unsafe_allow_html=True)
        sc.markdown(f"<div style='background:rgba(248,113,113,0.08);border-radius:10px;padding:12px;text-align:center;color:#f87171;font-size:0.85rem'>🚨 Escalated<br><b style='font-size:1.3rem'>{escalated}</b></div>", unsafe_allow_html=True)
        sd.markdown(f"<div style='background:rgba(251,191,36,0.08);border-radius:10px;padding:12px;text-align:center;color:#fbbf24;font-size:0.85rem'>💰 Refunds<br><b style='font-size:1.3rem'>{refunds}</b></div>", unsafe_allow_html=True)

        st.markdown(f"<div style='color:rgba(255,255,255,0.35);font-size:0.8rem;margin:14px 0 4px'><span class='live-dot'></span>Showing {len(filtered)} of {total} tickets — auto-refreshing every 3s</div>", unsafe_allow_html=True)
        st.markdown("---")

        # ── Ticket cards ─────────────────────────────────────
        for r in filtered:
            status   = r.get("status", "pending")
            tier     = r.get("customer_tier", "standard").lower()
            t_id     = r.get("ticket_id", "N/A")
            email_r  = r.get("customer_email", "N/A")
            subject_r= r.get("subject", "No subject")
            resolution = r.get("resolution", "Pending...")
            steps    = r.get("steps", [])

            status_icon  = {"resolved":"✅","escalated":"🚨","pending":"⏳"}.get(status,"⏳")
            status_label = {"resolved":"Resolved","escalated":"Escalated","pending":"Pending"}.get(status, status.title())
            tier_icon    = "👑" if tier=="vip" else "🔵" if tier=="premium" else "⚪"
            tier_label   = tier.upper()
            left_color   = {"resolved":"#34d399","escalated":"#f87171","pending":"#fbbf24"}.get(status,"#a78bfa")

            st.markdown(f"""
            <div class='ticket-row' style='border-left: 4px solid {left_color}'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px'>
                    <div>
                        <div class='ticket-id'>{t_id}</div>
                        <div class='ticket-email'>📧 {email_r}</div>
                        <div class='ticket-subject'>{subject_r}</div>
                    </div>
                    <div style='display:flex;gap:8px;flex-wrap:wrap;align-items:center'>
                        <span class='badge badge-{status}'>{status_icon} {status_label}</span>
                        <span class='badge badge-{tier}'>{tier_icon} {tier_label}</span>
                        <span style='color:rgba(255,255,255,0.3);font-size:0.75rem'>🔧 {len(steps)} steps</span>
                    </div>
                </div>
                <div class='ticket-resolution'>{resolution[:200]}{'...' if len(str(resolution)) > 200 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

            if steps:
                with st.expander(f"🔍 View {len(steps)} agent steps for {t_id}"):
                    tools_used = []
                    for i, step in enumerate(steps, 1):
                        st.markdown(f"<div class='step-item'><div class='step-num'>{i}</div><div style='color:rgba(255,255,255,0.7)'>{step}</div></div>", unsafe_allow_html=True)
                        if "tool" in str(step).lower() or ":" in str(step):
                            tools_used.append(str(step).split(":")[0].strip())
                    if tools_used:
                        st.markdown("<div style='margin-top:8px'>" + "".join([f"<span class='tool-chip'>{t}</span>" for t in tools_used[:6]]) + "</div>", unsafe_allow_html=True)