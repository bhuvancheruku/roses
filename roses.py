import streamlit as st
import base64
from pythreejs import Scene, PerspectiveCamera, WebGLRenderer, AmbientLight, DirectionalLight, GLTFLoader

# Set file path (ensure this is correct)
model_path = "iron_spider_suit_mcu.glb"

# Streamlit Page Configuration
st.set_page_config(page_title="3D Model Viewer", layout="wide")

try:
    with open(model_path, "rb") as f:
        model_data = f.read()
    base64_model = base64.b64encode(model_data).decode("utf-8")

    # Display base64 model data for testing
    st.write("Base64 Model Data:", base64_model[:200])  # Just show a part of base64 for confirmation
except Exception as e:
    st.error(f"Error loading the model: {e}")
