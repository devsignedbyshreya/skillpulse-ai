import streamlit as st

def metric_card(title, value):
    st.markdown(
        f"""
        <div style="
            padding:20px;
            border-radius:12px;
            background:#111827;
            border:1px solid #1f2937;
            text-align:center;
        ">
            <h4 style="margin:0;color:#9ca3af">{title}</h4>
            <h2 style="margin:0;color:white">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )