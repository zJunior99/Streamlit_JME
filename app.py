import streamlit as st
from textblob import TextBlob
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Sentiment Lab PRO", page_icon="📊", layout="centered")

# Inicialización del historial
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📊 Smart Sentiment Dashboard")
st.markdown("---")

# 2. Sidebar para contexto
with st.sidebar:
    st.header("About the App")
    st.info("This tool uses Natural Language Processing (NLP) to determine if a text is positive, negative, or neutral.")
    st.write("Built with: Streamlit & TextBlob")
    st.markdown("---")
    st.caption("Data Visualization Course 2026")

# 3. Entrada de texto
user_input = st.text_area("Enter text to analyze:", placeholder="I'm having a wonderful day learning Streamlit!", height=150)

# Columnas para organizar botones
col1, col2 = st.columns([1, 5])
with col1:
    btn_analyze = st.button("Analyze")

if btn_analyze:
    if user_input:
        blob = TextBlob(user_input)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)
        
        # 4. Lógica de Emojis y Umbrales
        if polarity > 0.1:
            label = "POSITIVE"
            emoji = "🙂"
            color = "success"
        elif polarity < -0.1:
            label = "NEGATIVE"
            emoji = "☹️"
            color = "error"
        else:
            label = "NEUTRAL"
            emoji = "😐"
            color = "warning"

        # 5. Guardar en el historial (Se agrega al inicio de la lista)
        st.session_state.history.insert(0, {
            "Text": user_input[:50] + "...", 
            "Polarity": polarity, 
            "Subjectivity": subjectivity, 
            "Label": label
        })

        # 6. Visualización de resultados inmediatos
        st.subheader(f"Analysis Results {emoji}")
        m1, m2 = st.columns(2)
        m1.metric("Sentiment Score", f"{polarity}")
        m2.metric("Subjectivity", f"{subjectivity} (0=Fact, 1=Opinion)")

        # Alerta visual
        getattr(st, color)(f"The detected sentiment is {label}")

        # 7. Gráfico de barras
        df_chart = pd.DataFrame({"Metric": ["Polarity", "Subjectivity"], "Value": [polarity, subjectivity]})
        st.bar_chart(df_chart.set_index("Metric"))
    else:
        st.warning("Please enter some text first.")

# 8. Sección del historial
if st.session_state.history:
    st.markdown("---")
    st.subheader("Analysis History")
    
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history, use_container_width=True)
    
    # Botón para limpiar historial con reinicio de app
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

st.markdown("---")
st.caption("Developed by Junior Mamani Estaña | Contact: junmamanie@upt.pe")
