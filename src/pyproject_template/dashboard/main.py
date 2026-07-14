import time

import numpy as np
import pandas as pd
import requests
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Pyproject Template Dashboard",
    page_icon="🚀",
    layout="wide",
)

# Custom premium header styles
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF4B4B, #7814FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.25rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: #1e1e24;
        border: 1px solid #333;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render main header
st.markdown(
    '<div class="main-title">Pyproject Template Showcase</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Interactive dashboard demonstrating FastAPI backend integration, live streaming, and simulated observability metrics.</div>',
    unsafe_allow_html=True,
)

# Sidebar configurations
st.sidebar.image(
    "https://raw.githubusercontent.com/astral-sh/uv/main/assets/uv-dark-logo.svg",
    width=150,
)
st.sidebar.markdown("### Configurations")
backend_url = st.sidebar.text_input("FastAPI Backend URL", "http://localhost:8000")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### Tech Stack Showcase
    - **FastAPI** (REST Web Services)
    - **Streamlit** (Data App Interface)
    - **OpenTelemetry** (Observability Layer)
    - **uv** (Package & Environment Orchestrator)
    """
)

# Tabs
tab1, tab2, tab3 = st.tabs(
    ["🔌 FastAPI Integration", "📺 Live Event Stream", "📊 Observability Metrics"]
)

with tab1:
    st.header("FastAPI Backend Operations")
    st.write("Directly query endpoint routes configured on your FastAPI backend.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ Numbers Addition Endpoint")
        st.write("Route: `/numbers/addition/{n1}/{n2}`")
        n1 = st.number_input("First Number", value=10, step=1)
        n2 = st.number_input("Second Number", value=32, step=1)

        if st.button("Calculate Addition"):
            try:
                res = requests.get(
                    f"{backend_url}/numbers/addition/{n1}/{n2}", timeout=5
                )
                if res.status_code == 200:
                    st.success(f"Result from API: **{res.json()}**")
                else:
                    st.error(f"Error status code: {res.status_code}")
            except Exception:
                st.error(
                    f"Could not connect to FastAPI server at {backend_url}. Verify that it is running."
                )

    with col2:
        st.subheader("📦 Items Lookup Endpoint")
        st.write("Route: `/items/{item_id}`")
        item_id = st.number_input("Item ID", value=42, step=1)
        query_param = st.text_input(
            "Query Parameter (optional)", value="streamlit-showcase"
        )

        if st.button("Lookup Item"):
            try:
                url = f"{backend_url}/items/{item_id}"
                params = {"q": query_param} if query_param else {}
                res = requests.get(url, params=params, timeout=5)
                if res.status_code == 200:
                    st.json(res.json())
                else:
                    st.error(f"Error status code: {res.status_code}")
            except Exception:
                st.error(
                    f"Could not connect to FastAPI server at {backend_url}. Verify that it is running."
                )

with tab2:
    st.header("Real-Time Event Streaming")
    st.write(
        "Test our optimized streaming endpoint route (`/test`), which uses chunked transfers to stream values real-time over the network."
    )

    col_btn, col_gauge = st.columns([1, 3])

    with col_btn:
        start_stream = st.button("🚀 Start Event Stream", type="primary")
        st.write(
            "Click to initiate requests session and iterate through HTTP chunk payloads."
        )

    if start_stream:
        try:
            # Connect to stream
            response = requests.get(f"{backend_url}/test", stream=True, timeout=10)
            if response.status_code == 200:
                progress_bar = st.progress(0.0)
                status_text = st.empty()
                chart_placeholder = st.empty()

                chart_data = pd.DataFrame(columns=["Value"])

                for idx, line in enumerate(response.iter_lines()):
                    if line:
                        decoded_val = int(line.decode("utf-8").strip())
                        new_row = pd.DataFrame({"Value": [decoded_val]}, index=[idx])
                        chart_data = pd.concat([chart_data, new_row])

                        # Update progress & stats
                        progress_bar.progress((decoded_val + 1) / 10.0)
                        status_text.metric(
                            "Received Value", decoded_val, delta=f"Index {idx}"
                        )

                        # Re-render chart
                        chart_placeholder.line_chart(chart_data)
                        time.sleep(0.15)  # Simulated latency for dashboard animation

                st.success("Successfully completed event streaming session.")
            else:
                st.error(f"Failed connection: Status {response.status_code}")
        except Exception:
            st.error(
                f"Could not reach Backend at {backend_url}/test. Verify your FastAPI server is started."
            )

with tab3:
    st.header("Observability & Metrics Dashboard")
    st.write(
        "Visualizing telemetry logs, trace stats, and performance metrics (mocked telemetry reflecting OpenTelemetry collector targets)."
    )

    # Metrics top row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("API Request Rate", "248 req/sec", "+12%")
    m2.metric("Median Request Latency", "12.4 ms", "-1.2 ms")
    m3.metric("Error Rate", "0.08 %", "Stable")
    m4.metric("Tracing Spans Emitted", "1,842 spans", "+234")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📈 Request Latency Over Time (ms)")
        latency_data = pd.DataFrame(
            np.random.normal(12.5, 2.0, size=(100, 3)),
            columns=["/items/{id}", "/numbers/addition", "/test"],
        )
        st.line_chart(latency_data)

    with col_chart2:
        st.subheader("📊 HTTP Status Code Distribution")
        status_codes = pd.DataFrame(
            {"Requests": [9840, 120, 15, 5]},
            index=[
                "200 OK",
                "304 Not Modified",
                "404 Not Found",
                "500 Internal Server Error",
            ],
        )
        st.bar_chart(status_codes)
