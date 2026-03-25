import streamlit as st
import json
import os
from datetime import datetime
from streamlit_folium import st_folium
import folium
from src.engine import LogisticsEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GeoStream | Logistics Engine",
    layout="wide"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    div[data-testid="stSidebar"] .stMarkdown h1,
    div[data-testid="stSidebar"] .stMarkdown h2,
    div[data-testid="stSidebar"] .stMarkdown h3,
    div[data-testid="stSidebar"] .stMarkdown p,
    div[data-testid="stSidebar"] .stMarkdown label {
        color: #e0e0e0;
    }
    .log-entry {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        font-size: 0.85em;
        border-left: 3px solid;
    }
    .log-success {
        background-color: #f0fdf4;
        border-left-color: #22c55e;
        color: #166534;
    }
    .log-error {
        background-color: #fef2f2;
        border-left-color: #ef4444;
        color: #991b1b;
    }
    .pipeline-card {
        background: white;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        height: 100%;
        border-top: 3px solid;
    }
    .pipeline-1 { border-top-color: #ef4444; }
    .pipeline-2 { border-top-color: #f59e0b; }
    .pipeline-3 { border-top-color: #3b82f6; }
    .pipeline-4 { border-top-color: #10b981; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'engine' not in st.session_state:
    engine = LogisticsEngine()

    data_path = "data/mock_data.json"
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            data = json.load(f)
            for loc in data["locations"]:
                engine.add_location(loc)
            for d in data["drivers"]:
                engine.add_driver(d["id"], tuple(d["coords"]))

    st.session_state.engine = engine
    st.session_state.logs = []
    st.session_state.dispatch_count = 0

# --- SIDEBAR: CONTROL CENTER ---
st.sidebar.markdown("## 🎛️ Control Center")
st.sidebar.divider()

user_id = st.sidebar.text_input("👤 Customer ID", "User_77")
dest_query = st.sidebar.text_input("📍 Destination Search", "North Street")

st.sidebar.markdown("##### Coordinates")
ux = st.sidebar.slider("Latitude (X)", 0.0, 100.0, 50.0)
uy = st.sidebar.slider("Longitude (Y)", 0.0, 100.0, 50.0)

st.sidebar.divider()

if st.sidebar.button("🔍 Find Optimal Driver", use_container_width=True, type="primary"):
    with st.spinner("Processing through algorithmic layers..."):
        result = st.session_state.engine.find_best_driver(user_id, dest_query, (ux, uy))
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.logs.insert(0, {"msg": result, "time": timestamp})
        if "Success" in result:
            st.session_state.dispatch_count += 1

st.sidebar.caption(f"🚗 Active Drivers: {len(st.session_state.engine.driver_index.root.entries) if st.session_state.engine.driver_index.root else 0}+")

# --- MAIN DASHBOARD ---
st.markdown("# 🌐 GeoStream Logistics Engine")
st.caption("Real-time driver dispatch powered by R-Trees, Radix Trees, Fibonacci Heaps, and Bloom Filters.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Spatial Driver Dispatch")

    m = folium.Map(location=[ux, uy], zoom_start=6, tiles="CartoDB positron")

    folium.Marker(
        [ux, uy],
        popup=f"📌 You ({ux:.1f}, {uy:.1f})",
        icon=folium.Icon(color='red', icon='user', prefix='fa'),
    ).add_to(m)

    folium.Circle(
        [ux, uy],
        radius=10000,
        color='#3b82f6',
        fill=True,
        fill_opacity=0.08,
        weight=2,
        dash_array='6',
    ).add_to(m)

    if st.session_state.logs:
        latest = st.session_state.logs[0]
        if "Success" in latest["msg"]:
            st.success(latest["msg"])
        else:
            st.error(latest["msg"])

    st_folium(m, width=800, height=500)

with col2:
    st.subheader("📊 System Status")

    m1, m2 = st.columns(2)
    m1.metric(label="Bloom Filter", value=f"{st.session_state.engine.security_filter.m} bits")
    m2.metric(label="Dispatches", value=st.session_state.dispatch_count)

    st.metric(label="Radix Tree", value="Compressed", help="Edge-compressed trie for location lookup")

    st.divider()

    if st.button("🚫 Blacklist User (Bloom Filter)", use_container_width=True):
        st.session_state.engine.blacklist_user(user_id)
        st.warning(f"⚠️ {user_id} added to the bit array.")

    st.subheader("📜 Event Log")
    if not st.session_state.logs:
        st.caption("No events yet — dispatch a driver to get started.")
    for entry in st.session_state.logs[:5]:
        is_success = "Success" in entry["msg"]
        css_class = "log-success" if is_success else "log-error"
        icon = "✅" if is_success else "❌"
        st.markdown(
            f'<div class="log-entry {css_class}">'
            f'<strong>{icon} {entry["time"]}</strong><br>{entry["msg"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

# --- DATA STRUCTURE EXPLAINER ---
st.divider()
st.subheader("⚙️ Behind the Scenes: Data Structure Pipeline")
exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)

with exp_col1:
    st.markdown(
        '<div class="pipeline-card pipeline-1">'
        '<strong>1. Bloom Filter</strong><br>'
        '<span style="font-size:0.85em;color:#555;">Checks for blacklisted IDs in <em>O(k)</em> time. High efficiency, zero false negatives.</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with exp_col2:
    st.markdown(
        '<div class="pipeline-card pipeline-2">'
        '<strong>2. Radix Tree</strong><br>'
        '<span style="font-size:0.85em;color:#555;">Validates destinations using edge compression. Faster than standard Tries.</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with exp_col3:
    st.markdown(
        '<div class="pipeline-card pipeline-3">'
        '<strong>3. R-Tree</strong><br>'
        '<span style="font-size:0.85em;color:#555;">Filters drivers by spatial bounding boxes in <em>O(log n)</em> time.</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with exp_col4:
    st.markdown(
        '<div class="pipeline-card pipeline-4">'
        '<strong>4. Fibonacci Heap</strong><br>'
        '<span style="font-size:0.85em;color:#555;">Ranks drivers by distance with <em>O(1)</em> amortized insertion.</span>'
        '</div>',
        unsafe_allow_html=True,
    )