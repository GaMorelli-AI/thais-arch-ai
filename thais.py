import streamlit as st
import streamlit.components.v1 as components
import replicate
import os
from PIL import Image
import io
import base64
import requests

def run_projeto1():
    
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

    # API key
    REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

    st.title("🏛️ ThAIs: Tool Hyperrealistic Architectural Image Simulation")

    st.sidebar.markdown("## ⚙️ Configurações")
    uploaded_file = st.sidebar.file_uploader("📸 Envie seu render", type=["png", "jpg", "jpeg"])

    st.sidebar.markdown("🎨 **Resolução**")
    # Layout 2x2 com botões
    col1, col2 = st.sidebar.columns(2)

    with col1:
        btn_1280 = st.button("1280", key="res_1280")
    with col2:
        btn_1024 = st.button("1024", key="res_1024")
    with col1:
        btn_768 = st.button("768", key="res_768")
    with col2:
        btn_512 = st.button("512", key="res_512")

    # Definindo a seleção com base no botão clicado
    if btn_1280:
        downscaling_resolution = 1280
    elif btn_1024:
        downscaling_resolution = 1024
    elif btn_768:
        downscaling_resolution = 768
    elif btn_512:
        downscaling_resolution = 512
    else:
        downscaling_resolution = 1280  # padrão

    creativity = st.sidebar.slider("🧠 CRIATIVIDADE (Define o nível de criatividade do modelo ao transformar a imagem. )", 0.0, 1.0, 0.35)
    resemblance = st.sidebar.slider("✨ RESEMBLANCE (Define o quanto a imagem gerada deve se parecer com a original)", 0.0, 1.0, 0.8)
    sharpen = st.sidebar.slider("⚙️ SHARPEN (Intensidade de nitidez aplicada no pós-processamento)", 0.0, 1.0, 0.2)
    dynamic = st.sidebar.slider("💄 DYNAMIC (ajusta o contraste ou gama)", 0.00, 50.0, 7.00)

    if st.button("🚀 Aprimorar Render"):
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)

            # Codifica imagem para base64
            img_base64 = base64.b64encode(buffered.read()).decode()
            data_uri = f"data:image/png;base64,{img_base64}"

            with st.spinner("Gerando imagem com IA..."):
                output = replicate.run(
                    "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
                    input={
                        "image": data_uri,
                        "prompt": "masterpiece, best quality, highres, realistic, modern architecture, sunlight, volumetric light, HDR, 8k <lora:more_details:0.7> <lora:SDXLrender_v2.0:1> <lora: architecture_lines:0.8> <lora: product_photography:0.7> <lora:film_light:0.5>",
                        "dynamic": dynamic,
                        "handfix": "disabled",
                        "pattern": False,
                        "sharpen": sharpen,
                        "sd_model": "juggernaut_reborn.safetensors [338b85bc4f]",
                        "scheduler": "DPM++ 3M SDE Karras",
                        "creativity": creativity,
                        "lora_links": "",
                        "downscaling": False,
                        "resemblance": resemblance,
                        "scale_factor": 2,
                        "tiling_width": 112,
                        "output_format": "png",
                        "tiling_height": 144,
                        "custom_sd_model": "",
                        "negative_prompt": "(worst quality, low quality, normal quality:2) JuggernautNegative-neg",
                        "num_inference_steps": 18,
                        "downscaling_resolution": downscaling_resolution,
                    }
                )

                # Gera o código HTML com o antes e depois
                html_code = f"""
                <link rel="stylesheet" type="text/css" href="https://cdn.knightlab.com/libs/juxtapose/latest/css/juxtapose.css">
                <div id="juxtapose" style="width: 100%; height: 500px;"></div>
                <script src="https://cdn.knightlab.com/libs/juxtapose/latest/js/juxtapose.min.js"></script>
                <script>
                new juxtapose.JXSlider('#juxtapose',
                [
                    {{
                    src: "{data_uri}",
                    label: "Antes"
                    }},
                    {{
                    src: "{getattr(output[0], "url", "Sem URL")}",
                    label: "Depois"
                    }}
                ],
                {{
                    animate: true,
                    showLabels: true,
                    showCredits: false,
                    makeResponsive: true
                }});
                </script>
                """

                components.html(html_code, height=550)

                # Baixa a imagem da URL
                response = requests.get(getattr(output[0], "url", "Sem URL"))

                # Carrega como imagem PIL
                img = Image.open(io.BytesIO(response.content))

                # Converte para bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
                img_bytes.seek(0)

                # Cria botão de download
                st.download_button(label="📥 Baixar imagem", data=img_bytes, file_name="render_aprimorado.png", mime="image/png")
                