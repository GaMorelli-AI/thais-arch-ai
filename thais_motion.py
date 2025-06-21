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

def run_projeto4():

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
    uploaded_file = st.sidebar.file_uploader("📸 Envie sua imagem", type=["png", "jpg", "jpeg"])

    def traduzir_para_ingles(prompt_pt):
        return GoogleTranslator(source='auto', target='en').translate(prompt_pt)

    # Parâmetros
    prompt_pt = st.text_input("Prompt:")
    aspect_ratio = st.sidebar.selectbox("🎨 Proporção", ["1:1", "16:9", "9:16"], index=0)

    if st.button("🚀 Gerar Motion"):
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)

            # Codifica imagem para base64
            img_base64 = base64.b64encode(buffered.read()).decode()
            data_uri = f"data:image/png;base64,{img_base64}"

            with st.spinner("🔄 Traduzindo prompt..."):
                prompt_en = traduzir_para_ingles(prompt_pt)
                #st.caption(f"🔤 Prompt traduzido: *{prompt_en}*")

            with st.spinner("Gerando Motion com IA..."):
                output = replicate.run(
                    "pixverse/pixverse-v4.5",
                    input={
                            "image": data_uri,
                            "style": "None",
                            "effect": "None",
                            "prompt": prompt_en,
                            "quality": "1080p",
                            "duration": 5,
                            "motion_mode": "normal",
                            "aspect_ratio": aspect_ratio,
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
