import streamlit as st
import pandas as pd
import os
from auto_dakar import scrape_auto

# ✅ CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Auto Dakar Scraper",
    layout="wide",
    page_icon="🚗"
)

# ✅ TITRE PRINCIPAL
st.title("🚗 Auto Dakar - Application Complète")

# ✅ INIT de session_state pour la page
if "page" not in st.session_state:
    st.session_state.page = "Scraping"

# ✅ SIDEBAR ➜ MESSAGE D'INFO
st.sidebar.info(
    "⚠️ Astuce : attendez la fin du chargement avant de changer de page "
    "pour éviter d'éventuelles erreurs d'affichage."
)

# ✅ SIDEBAR ➜ MENU DE NAVIGATION avec mémoire
page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Scraping",
        "Télécharger données WebScraper",
        "Dashboard",
        "Formulaire d'évaluation"
    ],
    index=[
        "Scraping",
        "Télécharger données WebScraper",
        "Dashboard",
        "Formulaire d'évaluation"
    ].index(st.session_state.page)
)
st.session_state.page = page

# ✅ PAGE 1 ➜ SCRAPING EN LIVE
if page == "Scraping":
    st.header("🕸️ Scraping en direct du site Dakar-Auto")
    st.write("Choisissez la catégorie et le nombre de pages à scraper.")

    nb_pages = st.sidebar.slider(
        "Nombre de pages à scraper :",
        min_value=1,
        max_value=50,
        value=5
    )

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

    if st.sidebar.button("🚀 Lancer le Scraping"):
        with st.spinner(f"Scraping '{category_choice}' sur {nb_pages} page(s)..."):
            df = scrape_auto(selected_category, nb_pages)
            if df.empty:
                st.error("❌ Aucun résultat n'a été trouvé. Vérifiez la catégorie ou le nombre de pages.")
            else:
                st.success(f"✅ Scraping terminé ({len(df)} résultats)")
                st.dataframe(df)
                st.download_button(
                    label="⬇️ Télécharger le CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{selected_category}_scraped.csv",
                    mime='text/csv'
                )

# ✅ PAGE 2 ➜ TÉLÉCHARGER DONNÉES WEBSCRAPER
elif page == "Télécharger données WebScraper":
    st.header("📥 Télécharger des données déjà scrapées avec WebScraper")
    st.write("Sélectionnez et téléchargez les fichiers CSV déjà collectés et nettoyés.")

    files_available = {
        "Voitures": "voitures_webscraper.csv",
        "Motos et Scooters": "motos_webscraper.csv",
        "Location de voitures": "location_webscraper.csv"
    }

    choix_fichier = st.selectbox(
        "Choisissez la catégorie :",
        list(files_available.keys())
    )

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

# ✅ PAGE 3 ➜ DASHBOARD
elif page == "Dashboard":
    st.header("📊 Dashboard des Annonces")
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

# ✅ PAGE 4 ➜ FORMULAIRE D'ÉVALUATION KOBO
elif page == "Formulaire d'évaluation":
    st.header("📝 Formulaire d'évaluation de l'app")
    st.write("Merci de prendre quelques minutes pour nous aider à améliorer cette application !")
    st.components.v1.iframe(
        "https://ee.kobotoolbox.org/i/ofN781in",
        width=800,
        height=600
    )
