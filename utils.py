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

def card_grid(main_title, items, values, tooltips):
    cards_html = ""
    for item, value, tooltip in zip(items, values, tooltips):
        cards_html += f"""
    <div
        class="flex flex-col justify-center bg-gray-100 px-6 py-3 rounded-xl shadow-md w-56 card-hover relative overflow-visible">
        <div class="text-4xl font-extrabold text-gray-900">{value}</div>
        <div class="mt-2 text-lg font-medium text-gray-600 flex items-center justify-center gap-2">
            {item}
        <span class="absolute group top-1 right-3">
            <span
                class="inline-block w-5 h-5 rounded-full bg-gray-300 text-gray-900 text-sm font-bold cursor-pointer">?</span>
            <span
                class="absolute -top-12 left-1/2 -translate-x-1/2 w-40 p-2 text-sm text-white bg-gray-800 rounded-md opacity-0 group-hover:opacity-100 transition">{tooltip}
            </span>
        </span>
        </div>
    </div>
        """

    full_html = f"""
    <style>
    .card-hover {{
        transition: transform 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
    }}
    .card-hover:hover {{
        transform: scale(1.05);
        background: linear-gradient(145deg, #4CAF50);
        box-shadow: 0 5px 5px rgba(0,0,0,0.15);
    }}
    </style>
    <div class="bg-white py-16">
      <div class="mx-auto max-w-4xl text-center">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900">
          {main_title}
        </h2>
      </div>
      <div class="mt-12 flex flex-wrap justify-center gap-4 text-center">
        {cards_html}
      </div>
    </div>
    """
    st.markdown(full_html, unsafe_allow_html=True)