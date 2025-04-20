# Roominate - Home/Landing Page
# Accessible via /
import streamlit as st
from PIL import Image
import os

# ---------- LAYOUT SETTINGS ----------
st.set_page_config(
    page_title="Roominate Survey", 
    layout="wide", 
    page_icon="🏠")

if "responses" not in st.session_state:
    st.session_state.responses = {}

# ---------- START OF HOME PAGE ----------
image_path = "assets/roominate_banner.jpg"
# image_path = "assets/roominate_banner_no_text.png"
# image_path = "assets/roominate_full_room_banner.jpg"
image_path = "assets/roominate_shorter.png"

if os.path.exists(image_path):
    # Parameters: image.crop
    # box – a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    # Return type: Image (Returns a rectangular region as (left, upper, right, lower)-tuple).
    # Return: An Image object. 
    image = Image.open(image_path)
    cropped_image = image.crop((0, 200, image.width, image.height - 300))  # Crop 50px from top and bottom
    st.image(cropped_image, use_container_width=True)
else:
    st.info(
        "no image called roominate_banner.jpg"
    )

# TODO: ADD SOME BRANDING HERE PROBABLY...

st.title("First time with us?")
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
    "<h3>Let us <em>ruminate</em> for you and find your perfect roommate matches — thoughtfully. </h3>"
    "<p>Roominate is a student-led initiative designed to help Cornell students find compatible roommates through intentional survey-based matching.</p>"
    "<p>It's inspired by <em>and</em> built on the roommate finding experiences of 4 Cornell students.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# if we want the two sections to be next to one another
col1, col2 = st.columns(2)  # Create two equal-width columns

with col1:
    st.markdown(
        '<div class="highlight-box">'
        "<h4>✨ Why Roominate?</h4>"
        "<ul>"
        "<li>Skip the awkward Instagram cold DMs</li>"
        "<li>Match on <b>YOUR</b> own preferences for a roommate</li>"
        "<li>Answer the questions that matter — based on research and feedback</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        '<div class="highlight-box">'
        "<h4>📝 How It Works</h4>"
        "<ol>"
        "<li>Take the 2-part survey located on the <b>left</b> sidebar</li>"
        "<li>We use these preferences to determine the most compatible pairs</li>"
        "<li>You hear back from us with your best matches!</li>"
        "</ol>"
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    "<br><p style='text-align: center;'><b>←</br>Use the sidebar to begin your survey!</p>",
    unsafe_allow_html=True,
)

st.markdown(
    "<br><p style='text-align: center; font-size: 14px; color: gray;'>Questions? Contact us at <a href='mailto:admin@roominate.me' style='color: gray;'>admin@roominate.me</a>, or find us on Instagram <a href='https://www.instagram.com/roominatematching' target='_blank' style='color: pink;'>@roominatematching</a>.</p>",
    unsafe_allow_html=True,
)