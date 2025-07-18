import streamlit as st
import pandas as pd
from auto_dakar import scrape_auto

st.title("Scraping en direct - Auto Dakar")

st.sidebar.header("Paramètres")
nb_pages = st.sidebar.slider("Nombre de pages :", 1, 50, 5)

category_choice = st.sidebar.radio(
    "Catégorie à scraper :",
    ["Voitures", "Motos et Scooters", "Location de voitures"]
)

category_map = {
    "Voitures": "voitures-4",
    "Motos et Scooters": "motos-and-scooters-3",
    "Location de voitures": "location-de-voitures-19"
}

selected_category = category_map[category_choice]

if st.sidebar.button("Lancer le Scraping"):
    with st.spinner(f"Scraping '{category_choice}' sur {nb_pages} page(s)..."):
        df = scrape_auto(selected_category, nb_pages)
        if df.empty:
            st.error("Aucun résultat trouvé. Vérifiez la catégorie ou le nombre de pages.")
        else:
            st.success(f"Scraping terminé ({len(df)} résultats)")
            st.dataframe(df)
            st.download_button(
                label="Télécharger le CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{selected_category}_scraped.csv",
                mime='text/csv'
            )
