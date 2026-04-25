import streamlit as st
from textblob import TextBlob
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Sentiment Lab PRO", page_icon="📊", layout="centered")

# Inicialización de estados
if "history" not in st.session_state:
    st.session_state.history = []

# Función para procesar y limpiar
def handle_analyze():
    # Recuperamos el texto del estado antes de que se borre
    text_to_analyze = st.session_state.user_text
    
    if text_to_analyze:
        blob = TextBlob(text_to_analyze)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)
        
        # Lógica de Emojis
        if polarity > 0.1:
            label, emoji, color = "POSITIVE", "🙂", "success"
        elif polarity < -0.1:
            label, emoji, color = "NEGATIVE", "☹️", "error"
        else:
            label, emoji, color = "NEUTRAL", "😐", "warning"

        # Guardar en historial
        st.session_state.history.insert(0, {
            "Text": text_to_analyze[:30] + "...", 
            "Polarity": polarity, 
            "Subjectivity": subjectivity, 
            "Label": label
        })
        st.session_state.history = st.session_state.history[:20]
        
        # Guardamos el resultado actual para mostrarlo abajo
        st.session_state.current_result = {
            "emoji": emoji, "polarity": polarity, 
            "subjectivity": subjectivity, "label": label, "color": color
        }
    # Limpiamos el widget de texto
    st.session_state.user_text = ""

st.title("📊 Smart Sentiment Dashboard")
st.markdown("---")

# 2. Sidebar
with st.sidebar:
    st.header("About the App")
    st.info("NLP Tool for real-time sentiment analysis.")
    st.write("Built with: Streamlit & TextBlob")

# 3. Entrada de texto vinculada al estado
st.text_area("Enter text to analyze:", key="user_text", placeholder="Type here...", height=150)

# Botón que dispara la función
st.button("Analyze", on_click=handle_analyze)

# 4. Mostrar resultados si existen
if "current_result" in st.session_state and st.session_state.history:
    res = st.session_state.current_result
    st.subheader(f"Last Analysis {res['emoji']}")
    m1, m2 = st.columns(2)
    m1.metric("Sentiment Score", f"{res['polarity']}")
    m2.metric("Subjectivity", f"{res['subjectivity']}")
    getattr(st, res['color'])(f"The detected sentiment is {res['label']}")

# 5. Comparativa e historial
if st.session_state.history:
    st.markdown("---")
    st.subheader("Sentiment Comparison (Historical)")
    df_history = pd.DataFrame(st.session_state.history)
    st.bar_chart(df_history.set_index("Text")[["Polarity", "Subjectivity"]])

    with st.expander("View Detailed History Log"):
        st.dataframe(df_history, use_container_width=True)
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            if "current_result" in st.session_state: del st.session_state.current_result
            st.rerun()

st.markdown("---")
st.caption("Developed by Junior Mamani Estaña | Contact: junmamanie@upt.pe")
