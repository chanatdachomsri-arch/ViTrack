import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------------------------------
# ViTrack — Health Alert software prototype
# Simulated data only. No physical sensors connected.
# -------------------------------------------------
st.set_page_config(
    page_title="ViTrack | Health Monitor",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Demo-only thresholds. These are NOT clinical decision limits.
HR_WARNING_LOW = 50
HR_WARNING_HIGH = 100
HR_CRITICAL_HIGH = 120
TEMP_WARNING = 37.8
TEMP_CRITICAL = 38.5
PRESSURE_WARNING_LOW = 200
PRESSURE_WARNING_HIGH = 650
PRESSURE_CRITICAL_HIGH = 750

st.markdown(
    """
    <style>
        /* Main app background */
        .stApp {
            background-color: #F5F7FB;
        }

        /* General text color */
        .stApp, .stMarkdown, p, label {
            color: #1E293B;
        }

        /* Main heading color */
        h1 {
            color: #142D4E;
        }

        /* Subheading colors */
        h2, h3 {
            color: #2563EB;
        }

        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #E8EEF8;
        }
    </style>
    """, 
    unsafe_allow_html=True,
)


def assess_readings(heart_rate: int, temperature: float, pressure_signal: int):
    """Return alert records for demo thresholds; not medical advice."""
    results = []

    # Heart rate: illustrative thresholds for this software demo only.
    if heart_rate >= HR_CRITICAL_HIGH:
        results.append({
            "sensor": "Heart rate", "level": "Critical", "color": "🔴",
            "message": f"Heart rate is very high in this demo ({heart_rate} bpm).",
            "advice": "Pause the demo and recheck the simulated value. In real life, consider activity and symptoms; seek appropriate medical help if unwell.",
        })
    elif heart_rate > HR_WARNING_HIGH:
        results.append({
            "sensor": "Heart rate", "level": "Warning", "color": "🟠",
            "message": f"Heart rate is above the demo reference range ({heart_rate} bpm).",
            "advice": "Recheck the reading and consider whether the person has recently been active. This alert does not diagnose a condition.",
        })
    elif heart_rate < HR_WARNING_LOW:
        results.append({
            "sensor": "Heart rate", "level": "Warning", "color": "🟠",
            "message": f"Heart rate is below the demo reference range ({heart_rate} bpm).",
            "advice": "Recheck the reading and consider context such as rest, fitness, and symptoms. This is a demo alert only.",
        })

    # Temperature thresholds are illustrative, not a diagnostic fever test.
    if temperature >= TEMP_CRITICAL:
        results.append({
            "sensor": "Temperature", "level": "Critical", "color": "🔴",
            "message": f"Temperature is very elevated in this demo ({temperature:.1f} °C).",
            "advice": "Recheck how the temperature would be measured in a real system. If a real person is unwell, seek advice from a qualified adult or health professional.",
        })
    elif temperature >= TEMP_WARNING:
        results.append({
            "sensor": "Temperature", "level": "Warning", "color": "🟠",
            "message": f"Temperature is above the demo reference range ({temperature:.1f} °C).",
            "advice": "Repeat the measurement and consider measurement method and context. The prototype cannot diagnose fever.",
        })

    # This is a raw simulated sensor signal, not a validated force/pressure unit.
    if pressure_signal > PRESSURE_CRITICAL_HIGH:
        results.append({
            "sensor": "Grip pressure signal", "level": "Critical", "color": "🔴",
            "message": f"Grip pressure signal is very high ({pressure_signal} demo units).",
            "advice": "Check the simulated sensor value and calibration. The number is an arbitrary raw signal, not a medical measurement.",
        })
    elif pressure_signal > PRESSURE_WARNING_HIGH:
        results.append({
            "sensor": "Grip pressure signal", "level": "Warning", "color": "🟠",
            "message": f"Grip pressure signal is above the demo range ({pressure_signal} demo units).",
            "advice": "Check sensor placement and repeat the demo reading. These raw units need calibration before real-world interpretation.",
        })
    elif pressure_signal < PRESSURE_WARNING_LOW:
        results.append({
            "sensor": "Grip pressure signal", "level": "Warning", "color": "🟠",
            "message": f"Grip pressure signal is below the demo range ({pressure_signal} demo units).",
            "advice": "Check the simulated sensor connection/value. Low raw signal alone does not indicate a health problem.",
        })

    return results


def make_demo_reading(profile: str):
    """Generate a single simulated reading for the selected presentation scenario."""
    if profile == "Elevated heart rate":
        return random.randint(103, 126), round(random.uniform(36.3, 37.4), 1), random.randint(280, 580)
    if profile == "Temperature alert":
        return random.randint(70, 95), round(random.uniform(37.8, 38.8), 1), random.randint(280, 580)
    if profile == "Grip signal alert":
        return random.randint(65, 92), round(random.uniform(36.2, 37.2), 1), random.choice([random.randint(100, 190), random.randint(660, 820)])
    if profile == "Multiple alerts":
        return random.randint(121, 135), round(random.uniform(38.5, 39.0), 1), random.randint(760, 850)
    return random.randint(65, 92), round(random.uniform(36.2, 37.2), 1), random.randint(280, 580)


# Sidebar controls
with st.sidebar:
    st.markdown("## 🫀 ViTrack")
    st.caption("VITAL SIGN MONITORING")
    st.divider()
    st.markdown("### Simulation settings")
    profile = st.selectbox(
        "Demo scenario",
        ["Typical readings", "Elevated heart rate", "Temperature alert", "Grip signal alert", "Multiple alerts"],
    )
    history_hours = st.slider("Chart history (hours)", min_value=1, max_value=24, value=8)
    refresh = st.selectbox("Data refresh", ["Manual demo", "Auto-refresh every 5 seconds"])
    st.info("Simulated data only. No physical sensors are connected.")
    generate = st.button("🔄 Generate new readings", use_container_width=True)

# Initialize history for this browser session.
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
            "Pressure Sensor": random.randint(280, 580),
        })
    st.session_state.vitrack_history = pd.DataFrame(rows)

if generate:
    new_hr, new_temp, new_pressure = make_demo_reading(profile)
    new_row = pd.DataFrame([{
        "Time": datetime.now(),
        "Heart Rate": new_hr,
        "Temperature": new_temp,
        "Pressure Sensor": new_pressure,
    }])
    st.session_state.vitrack_history = pd.concat(
        [st.session_state.vitrack_history, new_row], ignore_index=True
    ).tail(200)

# Current data and selected history window.
df = st.session_state.vitrack_history.copy()
cutoff = datetime.now() - timedelta(hours=history_hours)
visible = df[df["Time"] >= cutoff]
if visible.empty:
    visible = df.tail(10)

latest = df.iloc[-1]
hr = int(latest["Heart Rate"])
temp = float(latest["Temperature"])
pressure = int(latest["Pressure Sensor"])
alerts = assess_readings(hr, temp, pressure)

# Header
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">PERSONAL HEALTH TECHNOLOGY · SOFTWARE PROTOTYPE</div>
      <h1>ViTrack Health Dashboard</h1>
      <p>Vital sign overview, trend monitoring, and multi-sensor alerts — powered by simulated data.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Summary status and alert cards.
if any(item["level"] == "Critical" for item in alerts):
    st.error("🔴 **CRITICAL DEMO STATUS** — At least one simulated sensor has crossed the demo critical threshold.")
elif alerts:
    st.warning("🟠 **WARNING DEMO STATUS** — At least one simulated sensor is outside the demo reference range.")
else:
    st.success("🟢 **NORMAL DEMO STATUS** — No configured demo alert in the latest simulated reading.")

st.markdown('<div class="section-title">Live overview</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Latest generated values · use “Generate new readings” to test different alert scenarios</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("♥ Heart Rate", f"{hr} bpm", help="Simulated beats per minute")
m2.metric("🌡 Temperature", f"{temp:.1f} °C", help="Simulated temperature")
m3.metric("✊ Grip signal", f"{pressure} units", help="Raw simulated signal; not a calibrated force/pressure unit")
m4.metric("● Device status", "Simulation", help="No physical device connected")

st.markdown('<div class="section-title">Health Alert details</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Each alert includes a severity color, explanation, and suggested next step.</div>', unsafe_allow_html=True)
if not alerts:
    st.markdown(
        '<div class="status-card" style="border-left:5px solid #16a085;">'
        '<div class="status-value">🟢 All demo readings within configured ranges</div>'
        '<div class="muted">No rule was triggered by the latest simulated values. This does not confirm that a real person is healthy.</div></div>',
        unsafe_allow_html=True,
    )
else:
    for item in alerts:
        border_color = "#dc2626" if item["level"] == "Critical" else "#e9a23b"
        st.markdown(
            f'<div class="status-card" style="border-left:5px solid {border_color};">'
            f'<div class="status-label">{item["color"]} {item["level"].upper()} · {item["sensor"]}</div>'
            f'<div class="status-value">{item["message"]}</div>'
            f'<div style="margin-top:8px; color:#516276; font-size:14px;"><b>Suggested action:</b> {item["advice"]}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

# Trend charts
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
    hr_fig.update_layout(height=330, margin=dict(l=12, r=12, t=55, b=12), paper_bgcolor="white", plot_bgcolor="white", font=dict(family="Inter, Prompt, sans-serif", color="#516276"), title_font=dict(size=15, color="#172b45"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#edf1f6"))
    st.plotly_chart(hr_fig, use_container_width=True)
with right:
    temp_fig = px.area(
        visible, x="Time", y="Temperature",
        labels={"Time": "Time", "Temperature": "Temperature (°C)"},
        title="Temperature trend",
    )
    temp_fig.update_traces(line=dict(width=2))
    temp_fig.update_layout(height=330, margin=dict(l=12, r=12, t=55, b=12), paper_bgcolor="white", plot_bgcolor="white", font=dict(family="Inter, Prompt, sans-serif", color="#516276"), title_font=dict(size=15, color="#172b45"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#edf1f6"))
    st.plotly_chart(temp_fig, use_container_width=True)

# Explicit demo rules and recent readings.
st.markdown('<div class="section-title">Demo alert rules & latest readings</div>', unsafe_allow_html=True)
rules_col, table_col = st.columns([1, 1.6])
with rules_col:
    st.markdown(
        f"""
        <div class="status-card"><div class="status-label">HEART RATE · DEMO RULE</div>
        <div class="status-value">Warning: below {HR_WARNING_LOW} or above {HR_WARNING_HIGH} bpm<br>Critical: ≥ {HR_CRITICAL_HIGH} bpm</div></div>
        <div class="status-card"><div class="status-label">TEMPERATURE · DEMO RULE</div>
        <div class="status-value">Warning: ≥ {TEMP_WARNING:.1f} °C<br>Critical: ≥ {TEMP_CRITICAL:.1f} °C</div></div>
        <div class="status-card"><div class="status-label">GRIP SIGNAL · ARBITRARY DEMO UNITS</div>
        <div class="status-value">Warning: below {PRESSURE_WARNING_LOW} or above {PRESSURE_WARNING_HIGH}<br>Critical: above {PRESSURE_CRITICAL_HIGH}</div>
        <div class="muted">Grip-signal limits are arbitrary software-demo values and require sensor calibration.</div></div>
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
      Alert limits are illustrative software rules, not medically validated thresholds. Grip signal is an arbitrary raw value.
      This prototype is not a diagnostic, treatment, or emergency-monitoring device.
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional timed rerun for demo mode. Install streamlit-autorefresh to enable.
if refresh == "Auto-refresh every 5 seconds":
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=5000, key="vitrack_autorefresh")
    except ImportError:
        st.caption("For timed auto-refresh, add streamlit-autorefresh to requirements.txt and redeploy.")
