#region librarie
import streamlit as st
from utils import sidebar_contact, Navbar

def main():
    Navbar()
if __name__ == '__main__':
    main()

#region sommaire
#Config de la page
st.set_page_config(
    page_title="Calculateur CO2",
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
st.divider()

st.markdown("<br>Ce projet a pour objectif d’illustrer comment des données environnementales peuvent être mises en valeur grâce à des outils techniques interactifs.<br><br>En renseignant simplement deux aéroports, l’application **calcule les émissions de CO₂ liées au trajet en avion**. :blue-background[Le résultat est ensuite comparé à l’empreinte carbone moyenne d’un·e Français·e et exprimé en équivalents concrets (déplacements, alimentation, habitat, etc.)].<br><br>L’approche se veut avant tout pédagogique et visuelle : fournir un repère clair et accessible pour comprendre l’impact carbone d’un vol, tout en démontrant des compétences en traitement de données, visualisation et développement d’applications interactives.",
            unsafe_allow_html=True)
st.divider()

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    div.stButton > button:first-child:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

if st.button(label="Découvez le calculateur ✈️"):
    st.switch_page("pages/1_calculator.py")

st.divider()

st.title("🤔 FAQ")
with st.expander("❓ Qu’est-ce que l’empreinte carbone ?"):
    st.markdown("""L’empreinte carbone correspond à la quantité totale de gaz à effet de serre (principalement du dioxyde de carbone – CO₂) émise directement ou indirectement par une activité, une organisation ou un individu.
Dans notre cas, il s’agit de mesurer l’impact environnemental d’un trajet en avion, exprimé en kilogrammes de CO₂ équivalent.""")

with st.expander("❓ Pourquoi est-ce important de mesurer le CO₂ ?"):
    st.markdown(""" L’aviation représente une part significative des émissions mondiales de CO₂.
Mesurer ces émissions permet de :
- Prendre conscience de l’impact de nos déplacements.
- Comparer un voyage en avion avec d’autres postes d’émissions du quotidien (logement, alimentation, transport terrestre…).
- Donner des repères concrets pour orienter ses choix vers des alternatives plus durables lorsque c’est possible.""")

with st.expander("""❓ Quelles différences avec le calculateur de l’ADEME ?"""):
    st.markdown("""[Le calculateur de l’ADEME](https://nosgestesclimat.fr/fin) fournit une estimation chiffrée des émissions de CO₂ d’un vol ou de l’empreinte carbone totale d’un individu. On obtient donc une valeur brute, exprimée en kilogrammes ou en tonnes de CO₂.
Le présent projet a une approche complémentaire : il ne se limite pas à donner un chiffre, mais cherche à le mettre en perspective.
Quand on parle d’empreinte carbone, on manipule souvent de grandes masses abstraites difficiles à interpréter. 

Ici, l’idée est de :
- comparer l’impact d’un vol à l’empreinte carbone annuelle moyenne d’un·e Français·e,
- le replacer dans différents postes de consommation (déplacements, alimentation, habitat, etc.),
- fournir ainsi une échelle concrète et visuelle pour mieux appréhender ce que représente un seul vol.

👉 Ce projet est donc avant tout pédagogique et visuel, et sert de vitrine technique (données, calculs, visualisations interactives). Il n’a pas vocation à remplacer le calculateur de l’ADEME, mais à donner du contexte et des repères pour rendre ces chiffres plus parlants.
""")


with st.expander("❓ Comment ça fonctionne ?"):
    st.markdown("""Le calculateur suit plusieurs étapes :

- Liste des aéroports → importée depuis une base de données internationale (codes IATA, villes, pays).
- Recherche et tri → l’utilisateur tape quelques lettres et les résultats sont filtrés et classés selon leur pertinence.
- Calcul de la distance → application de la formule de Haversine, qui estime la distance entre deux points de la surface terrestre à partir de leurs coordonnées géographiques.
- Émission de CO₂ → conversion de la distance parcourue en émissions grâce aux facteurs d’émission fournis par l’ADEME (Agence de la Transition Écologique).
- Mise en contexte → les résultats sont comparés à l’empreinte carbone annuelle moyenne d’un·e Français·e et à différents postes de consommation (déplacements, alimentation, habitat, etc.). """)
    
with st.expander("""❓ Quelles sources ont été utilisées ?"""):
    st.markdown("""
    - Base de données aéroportuaire pour les localisations et codes IATA,
    - ADEME (Base Carbone®) pour les facteurs d’émission CO₂ des trajets en avion,
    - Publications de référence pour les données de comparaison avec les grands postes de consommation.""")
    if st.button(label="En savoir plus 🤔"):
        st.switch_page("pages/2_to_go_further.py")

#endregion

st.markdown("## 💡 Vos suggestions")
activated= st.checkbox("✍️ Laissez un avis")
if activated :    
    google_form="https://docs.google.com/forms/d/e/1FAIpQLSft_3YHclgWRMMWhjP3pHQAAujZ9JdtmN3_dqbI6PLWR4L8rw/viewform?embedded=true"
    st.components.v1.iframe(google_form, height=600)