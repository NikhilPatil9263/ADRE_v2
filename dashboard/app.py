import sys
import os

# ================= ADD PROJECT ROOT TO PYTHON PATH =================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from run_phase3 import run_adre_for_dashboard

# ================= STREAMLIT CONFIG =================
st.set_page_config(
    page_title="ADRE Route Optimization Dashboard",
    layout="wide"
)

st.title("🚚 ADRE – Intelligent Route Optimization Dashboard")
st.markdown(
    """
This dashboard visualizes **ETA, fuel cost, emissions, and loss-based route optimization**
using **traffic + weather aware digital twin logic**.
"""
)

# ================= RUN BUTTON =================
if st.button("▶️ Run Route Optimization"):
    with st.spinner("Running ADRE engine..."):
        results = run_adre_for_dashboard()

    df = pd.DataFrame(results["routes"])

    st.subheader("📊 Route Comparison")
    st.dataframe(df, use_container_width=True)

    best = results["best_route"]

    st.success(
        f"✅ Best Route Selected: **{best['route_id']}**  \n"
        f"💰 Total Loss: ₹{round(best['total_loss'], 2)}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏱️ ETA Comparison (minutes)")
        st.bar_chart(df.set_index("route_id")["eta_min"])

    with col2:
        st.subheader("💸 Total Loss Comparison (₹)")
        st.bar_chart(df.set_index("route_id")["total_loss"])

    st.subheader("🌱 CO₂ Emissions (kg)")
    st.bar_chart(df.set_index("route_id")["co2_kg"])

    st.subheader("🧠 AI Explanation")
    st.write(results["explanation"])

    st.subheader("🤖 LLM Reasoning")
    st.write(results["llm_reasoning"])

else:
    st.info("Click **Run Route Optimization** to start.")
