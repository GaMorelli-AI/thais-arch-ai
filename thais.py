import streamlit as st
import replicate
import os
from PIL import Image
import io
import base64
import requests

# API key
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

st.title("🏛️ ThAIs: Tool Hyperrealistic Architectural Image Simulation")

uploaded_file = st.file_uploader("📸 Envie seu render", type=["png", "jpg", "jpeg"])

downscaling = st.selectbox("🎨 Super-resolução", [False, True])
downscaling_resolution = st.selectbox("🎨 Resolução", [1280, 1024, 768, 512])
creativity = st.slider("✨ CRIATIVIDADE (Define o nível de criatividade do modelo ao transformar a imagem. Valores baixos preservam mais a imagem original; altos mudam mais.)", 0.0, 1.0, 0.35)
resemblance = st.slider("🧠 RESEMBLANCE (Define o quanto a imagem gerada deve se parecer com a original)", 0.0, 1.0, 0.6)
sharpen = st.slider(" SHARPEN (Intensidade de nitidez aplicada no pós-processamento)", 0.0, 1.0, 0.1)
dynamic = st.slider(" DYNAMIC (ajusta o contraste ou gama)", 0.00, 50.0, 6.00)

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
                    "downscaling": downscaling,
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

            st.write("URL da imagem:", getattr(output[0], "url", "Sem URL"))
            st.image(getattr(output[0], "url", "Sem URL"))

            # Baixa a imagem da URL
            response = requests.get(getattr(output[0], "url", "Sem URL"))

            # Carrega como imagem PIL
            img = Image.open(io.BytesIO(response.content))

            # Converte para bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Cria botão de download
            st.download_button(
                label="📥 Baixar imagem",
                data=img_bytes,
                file_name="render_aprimorado.png",
                mime="image/png"
            )
