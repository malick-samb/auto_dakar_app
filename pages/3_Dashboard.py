import streamlit as st
import pandas as pd

st.title("📊 Dashboard des Annonces")

st.write("Chargez un fichier CSV nettoyé (scrapé via WebScraper) pour explorer les données.")

uploaded_file = st.file_uploader("📂 Uploader votre fichier CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Données chargées avec succès !")

    st.subheader("🔎 Aperçu des données")
    st.dataframe(df.head())

    st.subheader("📌 Nombre total d'annonces")
    st.write(df.shape[0])

    if "Prix" in df.columns:
        try:
            df['Prix'] = df['Prix'].replace('[^\d.]', '', regex=True).astype(float)
            st.subheader("💰 Prix moyen")
            st.write(f"{df['Prix'].mean():,.0f} FCFA")
            st.subheader("📈 Distribution des prix")
            st.bar_chart(df['Prix'])
        except Exception:
            st.warning("⚠️ Impossible de traiter la colonne Prix.")

    if "Année" in df.columns:
        st.subheader("📊 Répartition par année")
        st.bar_chart(df['Année'].value_counts().sort_index())

    if "Carburant" in df.columns:
        st.subheader("⛽ Répartition par type de carburant")
        st.bar_chart(df['Carburant'].value_counts())
