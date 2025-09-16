import streamlit as st
import pandas as pd
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2 

def load_data(filename):
    BASE_DIR = Path(__file__).resolve().parent
    return pd.read_csv(BASE_DIR / "data" / filename)
    

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon moyen de la Terre en km

    # Convertir les degrés en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Différences des coordonnées
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Formule de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # Distance en km
    distance = R * c  
    return distance
 
def distance_ajust(distance):
    if distance < 500:
        marge = 0.03
    elif distance < 1000:
        marge = 0.03
    elif distance < 3500:
        marge = 0.03
    else :
        marge = 0.03
    return (distance * (1 + marge))

def co2_result(dist):
    if dist < 500:
        co2_km = 0.163
    elif dist < 1000:
        co2_km = 0.18
    elif dist < 3500:
        co2_km = 0.1
    else :
        co2_km = 0.0915
    return dist*co2_km

def sidebar_contact():
    st.sidebar.title("Contact :")
    contact = [
        "Antoine BARBIER",
        "https://github.com/Antoine-DA",
        "https://www.linkedin.com/in/antoine-barbier-83654415b/",
        "mailto:antoine.barbier.pro@gmail.com"
    ]

    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;" class="contact-icons">
            <div style="flex: 1;">{contact[0]}</div>
            <a href="{contact[1]}" target="_blank" style="margin-right: 12px;">
                <img src="https://cdn-icons-png.flaticon.com/32/25/25231.png" width="20" alt="GitHub">
            </a>
            <a href="{contact[2]}" target="_blank" style="margin-right: 12px;">
                <img src="https://cdn-icons-png.flaticon.com/32/174/174857.png" width="20" alt="LinkedIn">
            </a>
            <a href="{contact[3]}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/32/561/561127.png" width="22" alt="Email">
            </a>
        </div>
        """, unsafe_allow_html=True)
    
def Navbar():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Présentation', icon='👋')
        st.page_link('pages/1_calculator.py', label='Calculateur', icon='🧮')
        st.page_link('pages/2_to_go_further.py', label = "Pour aller plus loin", icon='📚')
