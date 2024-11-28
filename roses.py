import streamlit as st
import base64
import tempfile

# Streamlit Page Configuration
st.set_page_config(page_title="3D Model Viewer", layout="wide")

# Set the path to the GLB model (assuming it's in the root directory of the repo)
default_model_path = "iron_spider_suit_mcu.glb"

# Read the GLB file as binary
try:
    with open(default_model_path, "rb") as file:
        glb_file = file.read()
except Exception as e:
    st.error(f"Error reading the model file: {str(e)}")
    st.stop()  # Stop the app if the file is missing or cannot be read

# Convert the GLB file to base64
glb_base64 = base64.b64encode(glb_file).decode("utf-8")

# Streamlit Slider to control the rotation speed of the model
rotation_speed = st.slider("Model Rotation Speed", min_value=0.01, max_value=0.1, value=0.05)

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
