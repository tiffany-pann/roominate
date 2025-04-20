# Roominate - Home/Landing Page
# Accessible via /
import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Roominate Survey", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🏠")

if "responses" not in st.session_state:
    st.session_state.responses = {}

# Set up columns for centered layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    image_path = "roominate_banner.jpg"
    if os.path.exists(image_path):
        st.image(Image.open(image_path), use_container_width=True)
    else:
        st.info(
            "[Add a banner image called 'roominate_banner.jpg' to this folder to display it here]"
        )
    st.title("🏠 Welcome to Roominate")

    st.markdown(
        """
    <style>
    .centered-text {
        text-align: center;
        font-size: 18px;
        line-height: 1.6;
    }
    .highlight-box {
        border: 2px solid #f63366;
        border-radius: 10px;
        padding: 1rem;
        background-color: #fff0f5;
        margin-top: 1.5rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="centered-text">'
        "<h3>Find your perfect roommate match — thoughtfully.</h3>"
        "<p>Roominate is a student-led initiative designed to help Cornell students find compatible roommates through intentional survey-based matching.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="highlight-box">'
        "<h4>✨ Why Roominate?</h4>"
        "<ul>"
        "<li>Skip the awkward pairings</li>"
        "<li>Match on lifestyle and values</li>"
        "<li>Created by students, for students</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="highlight-box">'
        "<h4>📝 How It Works</h4>"
        "<ol>"
        "<li>Take the 2-part survey</li>"
        "<li>We analyze your responses</li>"
        "<li>You get matched with compatible peers</li>"
        "</ol>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<br><p style='text-align: center;'>Use the sidebar to begin your survey!</p>",
        unsafe_allow_html=True,
    )
