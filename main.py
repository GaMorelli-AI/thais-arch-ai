# app.py

import streamlit as st
from thais import run_projeto1
from thais_3d import run_projeto2
from thais_img import run_projeto3
from thais_motion import run_projeto4
from thais_video import run_projeto5

st.sidebar.title("🧭 Navegação")
opcao = st.sidebar.radio("Escolha a ferramenta:", ["Melhorar imagem", "Modelagem 3D", "Gerar imagem", "Gerar motion", "Gerar video"])

if opcao == "Melhorar imagem":
    run_projeto1()
elif opcao == "Modelagem 3D":
    run_projeto2()
elif opcao == "Gerar imagem":
    run_projeto3()
elif opcao == "Gerar motion":
    run_projeto4()
elif opcao == "Gerar video":
    run_projeto5()