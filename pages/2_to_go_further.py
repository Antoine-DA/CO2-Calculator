import streamlit as st
from utils import Navbar, sidebar_contact

def main():
    Navbar()
if __name__ == '__main__':
    main()

st.set_page_config(
    page_title="Calculateur CO2 ",  # titre de l'onglet navigateur
    page_icon="✈️")
sidebar_contact()

st.markdown("""
<div style="background-color:#4CAF50; padding:15px; border-radius:10px">
    <h1 style="color:white; text-align:center;">📖 Pour aller plus loin</h1>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("Cette section regroupe les sources utilisées dans ce projet, ainsi que des ressources complémentaires pour approfondir vos connaissances.")

# --- Sources principales
st.subheader("🔗 Sources principales")
st.markdown("""
- [ADEME – Base Carbone®](https://www.bilans-ges.ademe.fr)  
- [OpenFlights Airports Database](https://openflights.org/data)  
- [Publications ADEME sur l’empreinte carbone des Français](https://www.ademe.fr)
- [Citepa]("https://www.citepa.org/")
- [INSEE]("https://www.insee.fr/fr/outil-interactif/5367857/details/90_DDE/92_DEV/92G_Figure7")  
""")

# --- Ressources complémentaires
st.subheader("📚 Ressources complémentaires")

with st.expander("🌍 Rapports et sites institutionnels"):
    st.markdown("""
    - [GIEC (IPCC) – Rapports scientifiques](https://www.ipcc.ch)  
    - [Haut Conseil pour le Climat](https://www.hautconseilclimat.fr)  
    """)

with st.expander("📘 Ouvrages grand public"):
    st.markdown("""
    - *Comprendre le climat* – Jean-Marc Jancovici  
    - *Petit manuel de résistance contemporaine* – Cyril Dion  
    - *Le climat expliqué à ma fille* – Jean-Marc Jancovici & Alain Grandjean  
    """)

# --- Outils similaires
st.subheader("🛠️ Outils et calculateurs similaires")
st.markdown("""
- [Nos Gestes Climat (ADEME & ABC)](https://nosgestesclimat.fr)  
- [ICAO – Carbon Footprint Calculator](https://www.icao.int/environmental-protection/CarbonOffset/Pages/default.aspx)  
""")

st.subheader("💻 Stack technique utilisée")
st.markdown("""
Cette application a été développée avec les technologies et bibliothèques Python suivantes :  
- **Streamlit** – framework pour créer des applications web interactives  
- **Pandas** – manipulation et analyse de données  
- **Plotly (graph_objects & express)** – visualisation interactive de données  
- **Pathlib** – gestion des chemins de fichiers  
- **Math** – calculs géographiques et trigonométriques (distance, coordonnées)  
""")

st.markdown("## 💡 Vos suggestions")
activated= st.checkbox("✍️ Laissez un avis")
if activated :    
    google_form="https://docs.google.com/forms/d/e/1FAIpQLSft_3YHclgWRMMWhjP3pHQAAujZ9JdtmN3_dqbI6PLWR4L8rw/viewform?embedded=true"
    st.components.v1.iframe(google_form, height=600)