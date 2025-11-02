import streamlit as st
import requests
import os
from dotenv import load_dotenv
# ⚪ Forçar fundo branco manualmente
st.set_page_config(page_title="Azure Vision Analyzer", page_icon="🧠")
st.markdown(
    """
    <style>
    .stApp {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Carrega variáveis do .env
load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

# Função de análise
def analyze_image(image_bytes):
    if not AZURE_ENDPOINT or not AZURE_VISION_KEY:
        return {"error": "Chaves do Azure não configuradas. Verifique seu arquivo .env"}

    analyze_url = f"{AZURE_ENDPOINT}/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=caption,tags,objects"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_VISION_KEY,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(analyze_url, headers=headers, data=image_bytes)

    if response.status_code != 200:
        return {"error": f"Erro {response.status_code}: {response.text}"}
    return response.json()

# Interface
st.set_page_config(page_title="Azure Vision Analyzer", page_icon="🧠")
st.title("🧠 Analisador de Imagens com Azure AI Vision")

uploaded_file = st.file_uploader("Selecione uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagem carregada", use_container_width=True)

    if st.button("Analisar"):
        with st.spinner("Analisando imagem..."):
            result = analyze_image(uploaded_file.getvalue())

        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("🔍 Resultado da análise:")
            if "captionResult" in result:
                st.write("**Descrição:**", result["captionResult"]["text"])
            if "tagsResult" in result:
                st.write("**Tags:**", ", ".join([t["name"] for t in result["tagsResult"]["values"]]))
            if "objectsResult" in result:
                st.write("**Objetos detectados:**")
                for obj in result["objectsResult"]["values"]:
                    st.write(f"- {obj['name']} (confiança: {obj['confidence']:.2f})")
