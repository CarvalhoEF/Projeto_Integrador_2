import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Previsão de Preços", layout="centered")

st.title("✈️ Previsão de Preços de Passagens Aéreas")
st.write("Preencha as informações abaixo para estimar o preço da passagem.")

# =============================
# CARREGAMENTO DO MODELO
# =============================
@st.cache_resource
def carregar_modelo():
    try:
        modelo = joblib.load("Projeto_Integrador_2_clean/models/best_model_RandomForest.joblib")
        return modelo
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        st.stop()

modelo = carregar_modelo()

# =============================
# INTERFACE DE ENTRADA
# =============================
col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("Companhia", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
    source_city = st.selectbox("Origem", ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bangalore', 'Hyderabad'])
    departure_time = st.selectbox("Horário de Saída", ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night'])
    stops = st.selectbox("Paradas", ['zero', 'one', 'two_or_more'])
    flight_class = st.selectbox("Classe", ['Economy', 'Business'])

with col2:
    destination_city = st.selectbox("Destino", ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bangalore', 'Hyderabad'])
    arrival_time = st.selectbox("Horário de Chegada", ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night'])
    duration = st.number_input("Duração (horas)", min_value=0.5, max_value=30.0, value=2.0, step=0.5)
    days_left = st.slider("Dias até o voo", 1, 60, 15)

# =============================
# FUNÇÕES AUXILIARES
# =============================
def calcular_periodo(departure_time):
    period_mapping = {
        'Early_Morning': 'madrugada', 'Morning': 'manha', 'Afternoon': 'tarde',
        'Evening': 'noite', 'Night': 'noite', 'Late_Night': 'madrugada'
    }
    return period_mapping.get(departure_time, 'manha')

def categorizar_dias(days_left):
    if days_left <= 7:
        return 'ultima_hora'
    elif days_left <= 30:
        return 'curto_prazo'
    else:
        return 'longo_prazo'

def categorizar_duracao(duration):
    if duration <= 2:
        return 'curta'
    elif duration <= 5:
        return 'media'
    else:
        return 'longa'

# =============================
# PREDIÇÃO
# =============================
if st.button("💰 Prever Preço"):
    try:
        entrada = pd.DataFrame({
            'airline': [airline],
            'class': [flight_class],
            'source_city': [source_city],
            'departure_time': [departure_time],
            'stops': [stops],
            'arrival_time': [arrival_time],
            'destination_city': [destination_city],
            'days_left': [days_left],
            'duration': [duration],
            'departure_period': [calcular_periodo(departure_time)],
            'days_category': [categorizar_dias(days_left)],
            'duration_cat': [categorizar_duracao(duration)]
        })

        preco_previsto = modelo.predict(entrada)[0]
        st.success(f"💸 Preço estimado: ₹ {preco_previsto:,.2f}")

    except Exception as e:
        st.error(f"Erro na previsão: {e}")

st.markdown("---")
st.caption("Desenvolvido para o Projeto Integrador 2 — Previsão de Passagens Aéreas")

