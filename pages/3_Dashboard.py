import streamlit as st
import pandas as pd
from visualisation import Visualisation, traitement_de_donnees

st.title("Dashboard des Annonces")
source = st.selectbox("Choisir une source", ["Voitures", "Motos", "Locations"])


colonnes_voitures = ['marque', 'année', 'prix', 'adresse', 'kilométrage', 'boite', 'carburant', 'propriétaire']
colonnes_motos = ['marque', 'année', 'prix', 'adresse', 'kilométrage', 'propriétaire']
colonnes_locations = ['marque', 'année', 'prix', 'adresse', 'propriétaire']

if source == "Voitures":
    df = pd.read_csv('data/vente_auto.csv')
    df = traitement_de_donnees(df)
    colonnes = [c for c in colonnes_voitures if c in df.columns]
    df = df[colonnes]
elif source == "Motos":
    df = pd.read_csv('data/vente_moto.csv')
    df = traitement_de_donnees(df)
    colonnes = [c for c in colonnes_motos if c in df.columns]
    df = df[colonnes]
elif source == "Locations":
    df = pd.read_csv('data/location_auto.csv')
    df = traitement_de_donnees(df)
    colonnes = [c for c in colonnes_locations if c in df.columns]
    df = df[colonnes]
else:
    st.warning("Aucune donnée disponible.")
    st.stop()

vis = Visualisation(df)

st.subheader("Aperçu des données")
st.dataframe(vis.get_dataframe())

st.subheader("Prix moyen par marque")
st.bar_chart(vis.prix_moyen_par_marque())

st.subheader("Répartition des années")
st.line_chart(vis.repartition_annees())

fig = vis.plot_distribution_kilometrage()
if fig is not None:
    st.subheader("Distribution du kilométrage")
    st.pyplot(fig)
else:
    st.warning("Aucune donnée de kilométrage disponible.")
