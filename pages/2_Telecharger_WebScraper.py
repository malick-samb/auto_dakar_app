import streamlit as st
import os

st.title("📥 Télécharger des données WebScraper")

st.write("Sélectionnez et téléchargez les fichiers CSV déjà collectés et nettoyés.")

files_available = {
    "Voitures": "voitures_webscraper.csv",
    "Motos et Scooters": "motos_webscraper.csv",
    "Location de voitures": "location_webscraper.csv"
}

choix_fichier = st.selectbox("Choisissez la catégorie :", list(files_available.keys()))
selected_file = files_available[choix_fichier]

if os.path.exists(selected_file):
    with open(selected_file, "rb") as f:
        st.download_button(
            label=f"⬇️ Télécharger {choix_fichier}",
            data=f,
            file_name=selected_file,
            mime="text/csv"
        )
else:
    st.warning(f"⚠️ Le fichier {selected_file} n'est pas encore disponible sur le serveur.")
