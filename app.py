import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Previsão de Preços de Passagens", layout="centered")

@st.cache_resource
def carregar_modelo():
    return joblib.load("models/best_model_RandomForest.joblib")

modelo = carregar_modelo()

# Funções auxiliares que o modelo espera
def calcular_periodo(departure_time):
    period_mapping = {
        'Early_Morning': 'madrugada',
        'Morning': 'manha',
        'Afternoon': 'tarde', 
        'Evening': 'noite',
        'Night': 'noite',
        'Late_Night': 'madrugada'
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

st.title("✈️ Previsão de Preços de Passagens Aéreas")
st.write("Preencha as informações abaixo para estimar o preço da passagem.")

col1, col2 = st.columns(2)
with col1:
    airline = st.selectbox("Companhia aérea", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
    source_city = st.selectbox("Cidade de origem", ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bangalore', 'Hyderabad'])
    departure_time = st.selectbox("Período de saída", ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night'])
    stops = st.selectbox("Número de paradas", ['zero', 'one', 'two_or_more'])
    flight_class = st.selectbox("Classe", ['Economy', 'Business'])

with col2:
    destination_city = st.selectbox("Cidade de destino", ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bangalore', 'Hyderabad'])
    arrival_time = st.selectbox("Período de chegada", ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night'])
    duration = st.number_input("Duração do voo (horas)", min_value=0.5, max_value=30.0, step=0.5)
    days_left = st.slider("Dias até o voo", 0, 60, 10)

# Função de previsão CORRIGIDA
def prever_preco(airline, flight_class, source_city, departure_time, stops, 
                arrival_time, destination_city, days_left, duration):
    
    # Calcular as features derivadas
    departure_period = calcular_periodo(departure_time)
    days_category = categorizar_dias(days_left)
    duration_cat = categorizar_duracao(duration)
    
    # Criar DataFrame com TODAS as colunas necessárias
    dados = pd.DataFrame({
        'airline': [airline],
        'class': [flight_class],
        'source_city': [source_city],
        'departure_time': [departure_time],
        'stops': [stops],
        'arrival_time': [arrival_time],
        'destination_city': [destination_city],
        'days_left': [days_left],  # COLUNA ORIGINAL
        'duration': [duration],  # COLUNA ORIGINAL
        'departure_period': [departure_period],  # COLUNA DERIVADA
        'days_category': [days_category],  # COLUNA DERIVADA
        'duration_cat': [duration_cat]  # COLUNA DERIVADA
    })
    
    # Fazer previsão
    preco_predito = modelo.predict(dados)[0]
    return preco_predito

if st.button("Prever Preço"):
    try:
        preco_predito = prever_preco(
            airline=airline,
            flight_class=flight_class,
            source_city=source_city,
            departure_time=departure_time,
            stops=stops,
            arrival_time=arrival_time,
            destination_city=destination_city,
            days_left=days_left,
            duration=duration
        )
        st.success(f"💰 Preço estimado: ₹ {preco_predito:,.2f}")
        
        # Debug info (opcional)
        with st.expander("🔍 Ver detalhes técnicos"):
            st.write("Colunas enviadas para o modelo:")
            dados_debug = pd.DataFrame({
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
            st.write(dados_debug)
            
    except Exception as e:
        st.error("Ocorreu um erro na predição.")
        st.exception(e)

st.markdown("---")
st.caption("Aplicativo desenvolvido para o projeto de Machine Learning: Previsão de Preços de Passagens Aéreas ✈️")