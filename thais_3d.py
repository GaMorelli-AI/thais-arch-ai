import streamlit as st
import streamlit.components.v1 as components
import replicate
import os
import base64
import io
from PIL import Image


def run_projeto2():

    st.markdown("""
        <style>
        /* Reduz padding do corpo principal */
        .block-container {
            padding-top: 1rem;
        }

        .main {
            padding-top: 0rem;
        }
                            
            button[kind="secondary"] {
                width: 100%;
                height: 50px;
                border-radius: 10px;
                font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Config
    REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

    #st.set_page_config(page_title="ThAIs 3D", layout="centered")
    st.title("🏛️ ThAIs: Tool Hyperrealistic Architectural Image Simulation")

    st.sidebar.markdown("## ⚙️ Configurações")
    # Upload
    uploaded_file = st.sidebar.file_uploader("📸 Envie sua imagem", type=["jpg", "jpeg", "png"])

    # Parâmetros
    texture_size = st.sidebar.selectbox("🎨 Textura", [1024, 2048, 512], index=0)
    mesh_simplify = st.sidebar.slider("🧠 Mesh Simplify (Valores menores preservam mais detalhes.)", 0.90, 0.98, 0.95)
    slat_sampling_steps = st.sidebar.slider("✨ Slat Sampling Steps ((Stage of Local Appearance Transfer) – onde são refinados detalhes locais.)", 1, 50, 12)
    ss_guidance_strength = st.sidebar.slider("⚙️ Guidance Strength (Valores mais altos forçam o modelo a seguir mais fielmente a imagem original, mas podem limitar a criatividade 3D.)", 0.0, 10.0, 7.5)
    slat_guidance_strength = st.sidebar.slider("💄 Slat Guidance Strength (Mesmo princípio do Guidance Strength, mas aplicado ao refinamento.)", 0.0, 10.0, 3.0)
    ss_sampling_steps = st.sidebar.slider("💄 Sampling Steps (Valores maiores geram resultados mais detalhados, mas demoram mais.)", 1, 50, 12)

    if st.button("🚀 Gerar modelo 3D"):
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)
            img_base64 = base64.b64encode(buffered.read()).decode()
            data_uri = f"data:image/png;base64,{img_base64}"

            with st.spinner("🧠 Processando com IA..."):
                output = replicate.run(
                    "firtoz/trellis:e8f6c45206993f297372f5436b90350817bd9b4a0d52d2a76df50c1c8afa2b3c",
                    input={
                        "seed": 0,
                        "images": [data_uri],
                        "texture_size": texture_size,
                        "mesh_simplify": mesh_simplify,
                        "generate_color": False,
                        "generate_model": True,
                        "randomize_seed": True,
                        "generate_normal": False,
                        "save_gaussian_ply": False,
                        "ss_sampling_steps": ss_sampling_steps,
                        "slat_sampling_steps": slat_sampling_steps,
                        "return_no_background": False,
                        "ss_guidance_strength": ss_guidance_strength,
                        "slat_guidance_strength": slat_guidance_strength                    
                    },
                    TimeoutError=600
                )

            # Links de saída
            model_url = output["model_file"]
            #video_url = output["color_video"]

            st.markdown("### 📥 Baixe o modelo")
            st.markdown(f"[⬇️ Download GLB]({model_url})")
            #st.markdown(f"[⬇️ Download Vídeo]({video_url})")

            st.markdown("### 🌐 Visualização Interativa")
            
            components.html(f"""
                <model-viewer src="{model_url}" alt="Modelo 3D" auto-rotate camera-controls background-color="#111" style="width: 100%; height: 500px;"></model-viewer>  
                <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>   
            """, height=520)

        else:
            st.warning("⚠️ Envie uma imagem antes de continuar.")
