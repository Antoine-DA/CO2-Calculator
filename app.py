#region librarie
import streamlit as st
from utils import sidebar_contact


#region sommaire

#Config de la page
st.set_page_config(
    page_title="Calculateur CO2 ✈️",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)



sidebar_contact()

st.markdown("""
<div style="background-color:#4CAF50; padding:15px; border-radius:10px">
    <h1 style="color:white; text-align:center;">🌍 Calculateur d'empreinte carbone</h1>
    <p style="color:white; text-align:center; font-size:18px;">
        Comparez vos voyages aériens avec l’empreinte moyenne d’un·e français·e
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>Ce projet a pour objectif d’illustrer comment des données environnementales peuvent être mises en valeur grâce à des outils techniques interactifs.<br><br>En renseignant simplement deux aéroports, l’application estime les émissions de CO₂ liées au trajet en avion. Le résultat est ensuite comparé à l’empreinte carbone moyenne d’un·e Français·e et exprimé en équivalents concrets (déplacements, alimentation, habitat, etc.).<br><br>L’approche se veut avant tout pédagogique et visuelle : fournir un repère clair et accessible pour comprendre l’impact carbone d’un vol, tout en démontrant des compétences en traitement de données, visualisation et développement d’applications interactives.",
            unsafe_allow_html=True)

st.page_link("pages/1_calculator.py", label="Découvrez le calculateur", icon="✈️")

#endregion
