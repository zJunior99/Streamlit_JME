import streamlit as st
from textblob import TextBlob
import pandas as pd

# Configuración estética de la página
st.set_page_config(page_title="Sentiment Lab", page_icon="🧠")

st.title("🧠 Sentiment Analysis Dashboard")
st.markdown("""
Esta aplicación demuestra la potencia de **Streamlit** al procesar lenguaje natural 
en tiempo real. ¡Escribe una frase en inglés y observa los resultados!
""")

# Entrada de datos
user_input = st.text_area("Ingresa tu texto aquí:", placeholder="Example: I love how easy is to build apps with Streamlit!")

if st.button("Analizar Sentimiento"):
    if user_input:
        # Procesamiento
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity # Rango de -1 a 1
        
        # Lógica de colores y resultados
        st.subheader("Resultado del Análisis")
        if polarity > 0:
            st.success(f"Sentimiento Positivo (Score: {polarity})")
        elif polarity < 0:
            st.error(f"Sentimiento Negativo (Score: {polarity})")
        else:
            st.warning("Sentimiento Neutral")

        # Visualización de datos rápida
        data = pd.DataFrame({"Métrica": ["Polaridad"], "Valor": [polarity]})
        st.bar_chart(data.set_index("Métrica"))
    else:
        st.info("Por favor, escribe algo antes de analizar.")

st.sidebar.info("Herramientas utilizadas: Python, Streamlit, TextBlob.")
