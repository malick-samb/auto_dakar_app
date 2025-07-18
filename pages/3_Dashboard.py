import streamlit as st
import pandas as pd
from visualisation import Visualisation, traitement_de_donnees

st.title("Dashboard des Annonces")
source = st.selectbox("Choisir une source", ["Voitures", "Motos", "Locations"])

if source == "Voitures":
    df = pd.read_csv('data/vente_auto.csv')
    df = traitement_de_donnees(df)
    df = pd.DataFrame(df)[[
        'marque', 'année', 'prix', 'adresse', 'kilométrage', 'boite', 'carburant', 'propriétaire'
    ]]
elif source == "Motos":
    df = pd.read_csv('data/vente_moto.csv')
    df = traitement_de_donnees(df)
    df = pd.DataFrame(df)[[
        'marque', 'année', 'prix', 'adresse', 'kilométrage', 'propriétaire'
    ]]
elif source == "Locations":
    df = pd.read_csv('data/location_auto.csv')
    df = traitement_de_donnees(df)
    df = pd.DataFrame(df)[[
        'marque', 'année', 'prix', 'adresse', 'propriétaire'
    ]]
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
