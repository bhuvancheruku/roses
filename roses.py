import streamlit as st

# Streamlit Page Configuration
st.set_page_config(page_title="3D Model Viewer", layout="wide")

# File Upload Widget for GLB file
uploaded_file = st.file_uploader("Upload your GLB Model", type=["glb"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("uploaded_model.glb", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # HTML/JavaScript for three.js Viewer
    viewer_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three/examples/js/loaders/GLTFLoader.js"></script>
    </head>
    <body>
        <div id="container" style="width: 100%; height: 100%;"></div>
        <script>
            // Scene setup
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.getElementById('container').appendChild(renderer.domElement);

            // Lighting
            const light = new THREE.AmbientLight(0x404040, 2); // Soft white light
            scene.add(light);

            // Load GLB model
            const loader = new THREE.GLTFLoader();
            loader.load(
                "uploaded_model.glb", 
                function (gltf) {{
                    scene.add(gltf.scene);
                }},
                undefined,
                function (error) {{
                    console.error(error);
                }}
            );

            // Set camera position
            camera.position.z = 5;

            // Render loop
            function animate() {{
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }}
            animate();
        </script>
    </body>
    </html>
    """

    # Display the viewer
    st.components.v1.html(viewer_html, height=600, width=800)
