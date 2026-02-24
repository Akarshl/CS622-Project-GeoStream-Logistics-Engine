import streamlit as st
import json
import os
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
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'engine' not in st.session_state:
    engine = LogisticsEngine()
    
    # Load mock data if it exists
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

# --- SIDEBAR: CONTROLS & INPUT ---
st.sidebar.header("Control Center")
user_id = st.sidebar.text_input("Customer ID", "User_77")
dest_query = st.sidebar.text_input("Destination Search", "North Street")

st.sidebar.subheader("User Coordinates")
ux = st.sidebar.slider("Latitude (X)", 0.0, 100.0, 50.0)
uy = st.sidebar.slider("Longitude (Y)", 0.0, 100.0, 50.0)

if st.sidebar.button("Blacklist User (Bloom Filter)"):
    st.session_state.engine.blacklist_user(user_id)
    st.sidebar.warning(f"{user_id} added to bit array.")

# --- MAIN DASHBOARD ---
st.title("GeoStream Logistics Engine")
st.write("Real-time optimization using R-Trees, Radix Trees, Fibonacci Heaps, and Bloom Filters.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Spatial Driver Dispatch")
    
    # Initialize Folium Map (Representing our 100x100 grid)
    m = folium.Map(location=[ux, uy], zoom_start=6, tiles="CartoDB positron")
    
    # Mark User Location
    folium.Marker([ux, uy], popup="You", icon=folium.Icon(color='red', icon='user')).add_to(m)
    
    # Draw Search Radius (Visualizing R-Tree query range)
    folium.Circle([ux, uy], radius=10000, color='blue', fill=True, opacity=0.2).add_to(m)

    if st.button("🔍 Find Optimal Driver"):
        # Execution of the engine logic
        with st.spinner("Processing through algorithmic layers..."):
            result = st.session_state.engine.find_best_driver(user_id, dest_query, (ux, uy))
            st.session_state.logs.insert(0, result)
            
            if "Success" in result:
                st.success(result)
            else:
                st.error(result)

    st_folium(m, width=800, height=500)

with col2:
    st.subheader("System Status")
    
    # Metrics
    st.metric(label="Bloom Filter Size", value=f"{st.session_state.engine.security_filter.m} bits")
    st.metric(label="Radix Tree Nodes", value="Compressed")
    
    st.subheader("Event Log")
    for log in st.session_state.logs[:5]:
        st.write(f"> {log}")

# --- DATA STRUCTURE EXPLAINER ---
st.divider()
st.subheader("Behind the Scenes: Data Structure Pipeline")
exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)

with exp_col1:
    st.markdown("**1. Bloom Filter**")
    st.caption("Checks for blacklisted IDs in $O(k)$ time. High efficiency, zero false negatives.")


with exp_col2:
    st.markdown("**2. Radix Tree**")
    st.caption("Validates destination names using edge compression. Faster than standard Tries.")


with exp_col3:
    st.markdown("**3. R-Tree**")
    st.caption("Filters thousands of drivers by spatial bounding boxes in $O(\log n)$ time.")


with exp_col4:
    st.markdown("**4. Fibonacci Heap**")
    st.caption("Ranks drivers by distance with $O(1)$ amortized insertion.")