import streamlit as st

st.set_page_config(
    page_title="Auto Dakar Scraper",
    layout="wide",
)

st.title("Auto Dakar - Accueil")
st.write("""
Bienvenue dans l'application Auto Dakar !

Utilisez le menu à gauche pour :
- Scraper des annonces en direct
- Télécharger des données déjà scrapées
- Explorer les données avec le Dashboard
- Remplir le formulaire d'évaluation

Sélectionnez une page dans la sidebar pour commencer.
""")
