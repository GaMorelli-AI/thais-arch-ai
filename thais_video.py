import streamlit as st
import streamlit.components.v1 as components
import replicate
import os
from PIL import Image
import io
import base64
import requests
import tempfile
from deep_translator import GoogleTranslator

def run_projeto5():

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

    st.title("🏛️ ThAIs: Tool Hyperrealistic Architectural Image Simulation")

    st.sidebar.markdown("## ⚙️ Configurações")
    uploaded_file_1 = st.sidebar.file_uploader("📸 Envie sua imagem de início:", type=["png", "jpg", "jpeg"])
    uploaded_file_2 = st.sidebar.file_uploader("📸 Envie sua imagem de saída", type=["png", "jpg", "jpeg"])

    def traduzir_para_ingles(prompt_pt):
        return GoogleTranslator(source='auto', target='en').translate(prompt_pt)

    # Parâmetros
    prompt_pt = st.text_input("Prompt:")
    aspect_ratio = st.sidebar.selectbox("🎨 Proporção", ["9:16","16:9","1:1"], index=0)
    duration = st.sidebar.selectbox("⏰ Duração", [5,10], index=0)

    if st.button("🚀 Gerar Motion"):
        if uploaded_file_1:
            image_1 = Image.open(uploaded_file_1).convert("RGB")
            buffered_1 = io.BytesIO()
            image_1.save(buffered_1, format="PNG")
            buffered_1.seek(0)

            # Codifica imagem para base64
            img_base64_1 = base64.b64encode(buffered_1.read()).decode()
            data_uri_1 = f"data:image/png;base64,{img_base64_1}"

            image_2 = Image.open(uploaded_file_2).convert("RGB")
            buffered_2 = io.BytesIO()
            image_2.save(buffered_2, format="PNG")
            buffered_2.seek(0)

            # Codifica imagem para base64
            img_base64_2 = base64.b64encode(buffered_2.read()).decode()
            data_uri_2 = f"data:image/png;base64,{img_base64_2}"            

            with st.spinner("🔄 Traduzindo prompt..."):
                prompt_en = traduzir_para_ingles(prompt_pt)
                #st.caption(f"🔤 Prompt traduzido: *{prompt_en}*")

            with st.spinner("Gerando Motion com IA..."):
                output = replicate.run(
                    "kwaivgi/kling-v1.6-pro",
                    input={
                        "prompt": prompt_en,
                        "duration": duration,
                        "cfg_scale": 0.5,
                        "start_image": data_uri_1,
                        "end_image": data_uri_2,
                        "aspect_ratio": aspect_ratio,
                        "quality": "1080p",
                        "negative_prompt": ""
                    }
                )

            #st.image(getattr(output[0], "url", "Sem URL"), use_column_width=True)

            video_url = str(output)  # ou: output.url
            st.video(video_url)

            # Baixar o vídeo da URL
            response = requests.get(video_url)

            # Salva temporariamente o vídeo
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_file.write(response.content)
            temp_file.seek(0)

            # Cria botão de download
            st.download_button(
                label="⬇️ Baixar vídeo",
                data=temp_file.read(),
                file_name="thais_render.mp4",
                mime="video/mp4"
            )
