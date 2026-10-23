
import random
import time
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="ViTrack Sensor Simulator", page_icon="💓")

st.title("💓 ViTrack Sensor Simulator")
st.write("หน้าเว็บจำลองค่าเซนเซอร์ PPG, FSR และ NTC")

if "running" not in st.session_state:
    st.session_state.running = False

if st.button("สร้างค่าจำลองใหม่"):
    st.session_state.ppg = random.randint(65, 100)
    st.session_state.fsr = random.randint(100, 900)
    st.session_state.ntc = round(random.uniform(35.5, 37.5), 1)
    st.session_state.timestamp = datetime.now().isoformat(timespec="seconds")

if "ppg" not in st.session_state:
    st.session_state.ppg = 78
    st.session_state.fsr = 450
    st.session_state.ntc = 36.5
    st.session_state.timestamp = datetime.now().isoformat(timespec="seconds")

col1, col2, col3 = st.columns(3)
col1.metric("PPG (BPM)", st.session_state.ppg)
col2.metric("FSR (raw)", st.session_state.fsr)
col3.metric("NTC (°C)", st.session_state.ntc)

st.caption(f"เวลาจำลองล่าสุด: {st.session_state.timestamp}")
st.info("ตอนนี้เป็นเพียงค่าจำลอง ยังไม่ได้ส่งข้อมูลไป Firebase")
