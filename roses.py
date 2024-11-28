import streamlit as st
import base64
from pathlib import Path
import tempfile

# Streamlit Page Configuration
st.set_page_config(page_title="3D Model Viewer", layout="wide")

# File Upload Widget for GLB file
uploaded_file = st.file_uploader("iron_spider_suit_mcu.glb", type=["glb"])

# Streamlit Slider to control the rotation speed of the model
rotation_speed = st.slider("Model Rotation Speed", min_value=0.01, max_value=0.1, value=0.05)

# Function to convert file to base64
def convert_to_base64(file):
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
    # Read the file back as base64
    with open(temp_file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Display the 3D Model if a file is uploaded
if uploaded_file is not None:
    # Convert the uploaded GLB file to base64
    glb_base64 = convert_to_base64(uploaded_file)

    # HTML code to embed a 3D model viewer with three.js
    html_code = f"""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@gltfloader.js"></script>
    </head>
    <body style="margin: 0; overflow: hidden;">
        <script>
            var scene = new THREE.Scene();
            var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            var renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);
            
            // Add lights
            var ambientLight = new THREE.AmbientLight(0x404040); // Soft white light
            scene.add(ambientLight);
            var directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(5, 10, 7.5).normalize();
            scene.add(directionalLight);
            
            // Load GLTF model from base64
            var loader = new THREE.GLTFLoader();
            var modelData = atob("{glb_base64}");
            var blob = new Blob([new Uint8Array(modelData)], {{ type: 'application/octet-stream' }});
            var url = URL.createObjectURL(blob);
            
            loader.load(url, function(gltf) {{
                scene.add(gltf.scene);
                gltf.scene.rotation.y = {rotation_speed};
            }});
            
            camera.position.z = 5;

            // Animation loop
            function animate() {{
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    </body>
    </html>
    """

    # Embed the 3D model viewer in the Streamlit app
    st.components.v1.html(html_code, height=600)
