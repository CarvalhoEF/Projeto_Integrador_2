# ✈️ Previsão de Preços de Passagens Aéreas

Este projeto aplica **Ciência de Dados e Machine Learning** para prever o preço de passagens aéreas com base em informações como companhia aérea, origem, destino, horário de saída, duração e antecedência da compra.

---

## 🚀 Estrutura do Projeto
```
📁 previsao-passagens/
│
├── app.py                             # Aplicativo Streamlit
├── previsao_passagens_notebook.ipynb  # Notebook de modelagem e EDA
├── models/
│   └── best_model_RandomForest.joblib # Modelo salvo para predição
├── requirements.txt                   # Dependências do projeto
└── README.md                          # Este arquivo
```

---

## 🧩 Tecnologias Utilizadas
- Python 3.10+
- Pandas, NumPy
- Scikit-learn
- Streamlit
- Joblib
- XGBoost

---

## 🧠 Como Executar Localmente

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/seuusuario/previsao-passagens.git
cd previsao-passagens

# 2️⃣ Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate     # (no Windows)
# ou source venv/bin/activate  # (no Linux/Mac)

# 3️⃣ Instale as dependências
pip install -r requirements.txt

# 4️⃣ Execute o app
streamlit run app.py
```

---

## ☁️ Deploy no Streamlit Cloud

1. Suba o projeto completo no seu repositório GitHub.  
2. Acesse [https://share.streamlit.io](https://share.streamlit.io).  
3. Clique em **“New app” → Conecte seu GitHub → Escolha o repositório**.  
4. No campo **Main file path**, insira:  
   ```
   app.py
   ```
5. Clique em **Deploy** ✅  

O Streamlit Cloud instalará automaticamente as dependências listadas em `requirements.txt`.

---

## 🔄 Atualizando o App

Após modificar o notebook, o modelo ou o app, execute:

```bash
git add .
git commit -m "Atualiza modelo e interface"
git push origin main
```

O Streamlit Cloud detectará as alterações e fará o redeploy automaticamente.

---

## 👩‍💻 Autoria

**Elen Carvalho**  
💡 *“Da análise à aplicação: dados que conectam destinos.”*
