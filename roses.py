import streamlit as st
import os

# Set page configuration
st.set_page_config(page_title="Rose Bouquet Animation", layout="wide")

# HTML and CSS Integration
def load_local_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

st.title("Interactive Rose Bouquet Animation")
st.write("This project uses HTML, CSS, and JavaScript to display a beautiful animated rose bouquet.")

# Embed HTML and CSS in the Streamlit app
html_code = load_local_file("roses_animation.html")
css_code = load_local_file("style.css")

# Add CSS to Streamlit
st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

# Embed the HTML animation
st.components.v1.html(html_code, height=800)
