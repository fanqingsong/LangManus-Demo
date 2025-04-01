import streamlit as st
from agent import LangManusAgent
import os
from PIL import Image

st.set_page_config(page_title="LangManus GitHub Analyzer", layout="wide")
st.title("🧠 LangManus GitHub Repo Analyzer")

if st.button("🔍 Run Analysis on Trending Repo"):
    with st.spinner("Running LangManus agents..."):
        agent = LangManusAgent(task="Find a popular open-source project updated recently and summarize its new features with examples and charts.")
        report, chart_paths = agent.run_and_return()

        st.markdown(report)

        st.subheader("📊 Charts")
        for path in chart_paths:
            if os.path.exists(path):
                st.image(Image.open(path), caption=os.path.basename(path).replace('_', ' ').replace('.png', '').title(), use_container_width=True)
else:
    st.info("Click the button to run analysis on a trending GitHub Python repo.")
