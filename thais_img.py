import streamlit as st
import streamlit.components.v1 as components
import replicate
import os
from PIL import Image
import io
import base64
import requests
from deep_translator import GoogleTranslator

def traduzir_para_ingles(prompt_pt):
    return GoogleTranslator(source='auto', target='en').translate(prompt_pt)

def run_projeto3():

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

    # Parâmetros
    prompt_pt = st.text_input("Prompt:")
    aspect_ratio = st.sidebar.selectbox("🎨 Proporção", ["1:1", "16:9", "21:9", "9:16", "9:21"], index=0)

    if st.button("🚀 Gerar imagem"):
        with st.spinner("🔄 Traduzindo prompt..."):
            prompt_en = traduzir_para_ingles(prompt_pt)
            #st.caption(f"🔤 Prompt traduzido: *{prompt_en}*")
        with st.spinner("🧠 Processando com IA..."):
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt_en,
                    "go_fast": True,
                    "megapixels": "1",
                    "num_outputs": 4,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "png",
                    "output_quality": 80,
                    "num_inference_steps": 4
                }
            )

            col1, col2 = st.columns(2)

            with col1:
                url1 = getattr(output[0], "url", "")
                st.image(url1, use_column_width=True)
                if url1:
                    img1 = requests.get(url1).content
                    st.download_button("⬇️ Baixar Imagem 1", data=img1, file_name="imagem_1.png", mime="image/png")

            with col2:
                url2 = getattr(output[1], "url", "")
                st.image(url2, use_column_width=True)
                if url2:
                    img2 = requests.get(url2).content
                    st.download_button("⬇️ Baixar Imagem 2", data=img2, file_name="imagem_2.png", mime="image/png")

            col3, col4 = st.columns(2)

            with col3:
                url3 = getattr(output[2], "url", "")
                st.image(url3, use_column_width=True)
                if url3:
                    img3 = requests.get(url3).content
                    st.download_button("⬇️ Baixar Imagem 3", data=img3, file_name="imagem_3.png", mime="image/png")

            with col4:
                url4 = getattr(output[3], "url", "")
                st.image(url4, use_column_width=True)
                if url4:
                    img4 = requests.get(url4).content
                    st.download_button("⬇️ Baixar Imagem 4", data=img4, file_name="imagem_4.png", mime="image/png")
