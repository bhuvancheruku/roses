import streamlit as st
from pythreejs import Scene, PerspectiveCamera, WebGLRenderer, AmbientLight, DirectionalLight, Mesh, MeshBasicMaterial, AxesHelper
from pythreejs import OrbitControls
import numpy as np

# Streamlit Page Configuration
st.set_page_config(page_title="3D Model Viewer", layout="wide")

# File Upload Widget for GLB file
uploaded_file = st.file_uploader("Upload GLB Model", type=["glb"])

# Streamlit Slider to control the rotation speed of the model
rotation_speed = st.slider("Model Rotation Speed", min_value=0.01, max_value=0.1, value=0.05)

# Display the 3D Model if a file is uploaded
if uploaded_file is not None:
    # Create a 3D scene using pythreejs
    scene = Scene()

    # Camera setup
    camera = PerspectiveCamera(fov=75, aspect=1, near=0.1, far=1000, position=[0, 1, 5])

    # Lighting
    ambient_light = AmbientLight(intensity=0.7)
    scene.add(ambient_light)
    
    directional_light = DirectionalLight(intensity=0.5, position=[5, 10, 7.5])
    scene.add(directional_light)

    # WebGL renderer
    renderer = WebGLRenderer(width=800, height=600)

    # OrbitControls for user interaction
    controls = OrbitControls(controlling=camera)

    # Load the GLB model using GLTFLoader
    loader = GLTFLoader()

    try:
        model = loader.load(uploaded_file)
        scene.add(model)
    except Exception as e:
        st.error(f"Error loading GLB model: {e}")
        model = None

    # Add Axes Helper to the scene for better orientation visualization
    axes = AxesHelper(size=5)
    scene.add(axes)

    # Render loop function
    def render_loop():
        if model:
            # Rotation animation
            model.rotation.y += rotation_speed
            
            # Render the scene
            renderer.render(scene, camera)
        return renderer

    # Display the 3D scene in Streamlit
    st.components.v1.html(
        render_loop(),
        height=800,
    )
