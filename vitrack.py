import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# ViTrack — software prototype
# Simulated data only; no hardware.
# -----------------------------
st.set_page_config(
    page_title="ViTrack | Health Monitor",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for a polished health dashboard.
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Prompt:wght@400;500;600;700&display=swap');
      html, body, [class*="css"] { font-family: Inter, Prompt, sans-serif; }
      .stApp { background: #f5f7fb; }
      [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e8edf4; }
      .hero {
        background: linear-gradient(120deg, #142d4e 0%, #244f78 58%, #337b91 100%);
        padding: 26px 30px; border-radius: 22px; color: white; margin-bottom: 20px;
        box-shadow: 0 12px 30px rgba(25, 55, 85, .12);
      }
      .hero h1 { margin: 0; font-size: 30px; font-weight: 700; color: white; }
      .hero p { margin: 8px 0 0 0; color: #dcebf5; font-size: 14px; }
      .eyebrow { color: #b9dbe9; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
      .section-title { font-size: 18px; font-weight: 700; color: #172b45; margin: 8px 0 3px 0; }
      .muted { color: #718096; font-size: 12px; }
      div[data-testid="stMetric"] {
        background: white; padding: 18px 20px; border: 1px solid #e7edf5;
        border-radius: 17px; box-shadow: 0 4px 14px rgba(31, 55, 80, .035);
      }
      div[data-testid="stMetricLabel"] { color: #62748a; font-weight: 600; }
      div[data-testid="stMetricValue"] { color: #172b45; }
      .status-card {
        background: white; padding: 16px 18px; border-radius: 16px;
        border: 1px solid #e7edf5; margin-bottom: 8px;
      }
      .status-ok { border-left: 4px solid #16a085; }
      .status-warn { border-left: 4px solid #e9a23b; }
      .status-label { font-size: 12px; color: #718096; }
      .status-value { font-size: 17px; font-weight: 700; color: #172b45; margin-top: 4px; }
      .footer-note { color: #7b8797; font-size: 11px; margin-top: 22px; }
      div.stButton > button { border-radius: 10px; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar controls
with st.sidebar:
    st.markdown("## 💗 ViTrack")
    st.caption("VITAL SIGN MONITORING")
    st.divider()
    st.markdown("### Simulation settings")
    profile = st.selectbox("Demo scenario", ["Typical readings", "Elevated heart rate", "Temperature alert"])
    history_hours = st.slider("Chart history (hours)", min_value=1, max_value=24, value=8)
    refresh = st.selectbox("Data refresh", ["Manual demo", "Auto-refresh every 5 seconds"])
    st.info("This prototype uses generated sample data. It is not connected to sensors.")
    generate = st.button("🔄 Generate new readings", use_container_width=True)

# Stable history stored for the current session
if "vitrack_history" not in st.session_state:
    random.seed(7)
    now = datetime.now()
    rows = []
    for i in range(48):
        ts = now - timedelta(minutes=(47 - i) * 10)
        rows.append({
            "Time": ts,
            "Heart Rate": max(55, min(125, int(random.gauss(76, 7)))),
            "Temperature": round(random.gauss(36.6, 0.25), 1),
            "Pressure Sensor": random.randint(180, 560),
        })
    st.session_state.vitrack_history = pd.DataFrame(rows)

if generate:
    df = st.session_state.vitrack_history.copy()
    now = datetime.now()
    if profile == "Elevated heart rate":
        hr = random.randint(101, 118)
        temp = round(random.uniform(36.2, 37.2), 1)
    elif profile == "Temperature alert":
        hr = random.randint(72, 94)
        temp = round(random.uniform(37.8, 38.5), 1)
    else:
        hr = random.randint(65, 91)
        temp = round(random.uniform(36.1, 37.2), 1)
    pressure = random.randint(180, 800)
    new_row = pd.DataFrame([{
        "Time": now,
        "Heart Rate": hr,
        "Temperature": temp,
        "Pressure Sensor": pressure,
    }])
    st.session_state.vitrack_history = pd.concat([df, new_row], ignore_index=True).tail(200)

df = st.session_state.vitrack_history.copy()
cutoff = datetime.now() - timedelta(hours=history_hours)
visible = df[df["Time"] >= cutoff]
if visible.empty:
    visible = df.tail(10)

latest = df.iloc[-1]
hr = int(latest["Heart Rate"])
temp = float(latest["Temperature"])
pressure = int(latest["Pressure Sensor"])

# Header
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">PERSONAL HEALTH TECHNOLOGY · SOFTWARE PROTOTYPE</div>
      <h1>ViTrack Health Dashboard</h1>
      <p>Vital sign overview, trend monitoring, and event notifications — powered by simulated data.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status banner
alerts = []
if hr > 100:
    alerts.append(f"Heart-rate demo threshold exceeded ({hr} bpm)")
if temp >= 37.8:
    alerts.append(f"Temperature demo threshold exceeded ({temp:.1f} °C)")

if alerts:
    st.warning("⚠️ **Demo alert:** " + " · ".join(alerts))
else:
    st.success("● Demo status: no configured alert in the latest simulated reading")

st.markdown('<div class="section-title">Live overview</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Latest generated values · updated when you generate a new reading</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("♥ Heart Rate", f"{hr} bpm", help="Simulated beats per minute")
m2.metric("🌡 Temperature", f"{temp:.1f} °C", help="Simulated temperature")
m3.metric("◉ Pressure signal", f"{pressure}", help="Raw simulated sensor value; not a pressure unit")
m4.metric("● Device status", "Simulation", help="No physical device connected")

st.markdown('<div class="section-title">Trend analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Sample history for demonstration only</div>', unsafe_allow_html=True)

left, right = st.columns([1.55, 1])
with left:
    hr_fig = px.line(
        visible, x="Time", y="Heart Rate", markers=True,
        labels={"Time": "Time", "Heart Rate": "Heart rate (bpm)"},
        title="Heart rate trend",
    )
    hr_fig.update_traces(line=dict(width=3), marker=dict(size=5))
    hr_fig.update_layout(
        height=330, margin=dict(l=12, r=12, t=55, b=12),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter, Prompt, sans-serif", color="#516276"),
        title_font=dict(size=15, color="#172b45"),
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#edf1f6"),
    )
    st.plotly_chart(hr_fig, use_container_width=True)

with right:
    temp_fig = px.area(
        visible, x="Time", y="Temperature",
        labels={"Time": "Time", "Temperature": "Temperature (°C)"},
        title="Temperature trend",
    )
    temp_fig.update_traces(line=dict(width=2))
    temp_fig.update_layout(
        height=330, margin=dict(l=12, r=12, t=55, b=12),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter, Prompt, sans-serif", color="#516276"),
        title_font=dict(size=15, color="#172b45"),
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#edf1f6"),
    )
    st.plotly_chart(temp_fig, use_container_width=True)

# Events and data table
st.markdown('<div class="section-title">Alert rules & latest events</div>', unsafe_allow_html=True)
event_col, table_col = st.columns([1, 1.6])
with event_col:
    st.markdown(
        """
        <div class="status-card status-warn">
          <div class="status-label">DEMO RULE 01</div>
          <div class="status-value">Heart rate &gt; 100 bpm</div>
          <div class="muted">Shows an alert for the selected demo condition.</div>
        </div>
        <div class="status-card status-warn">
          <div class="status-label">DEMO RULE 02</div>
          <div class="status-value">Temperature ≥ 37.8 °C</div>
          <div class="muted">Illustrative threshold for presentation only.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with table_col:
    display_df = df.tail(8).sort_values("Time", ascending=False).copy()
    display_df["Time"] = display_df["Time"].dt.strftime("%H:%M:%S")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown(
    """
    <div class="footer-note">
      DEMONSTRATION ONLY · All readings are simulated and are not measured from a person.
      Thresholds are illustrative, not medical advice. This prototype is not a diagnostic or emergency-monitoring device.
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional timed rerun for demo mode. Install streamlit-autorefresh to enable:
if refresh == "Auto-refresh every 5 seconds":
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=5000, key="vitrack_autorefresh")
    except ImportError:
        st.caption("For timed auto-refresh, install: pip install streamlit-autorefresh")
