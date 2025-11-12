import streamlit as st
import pandas as pd
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from io import BytesIO

def Navbar():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Présentation', icon='👋')
        st.page_link('pages/1_calculator.py', label='Calculateur', icon='🧮')
        st.page_link('pages/2_to_go_further.py', label = "Pour aller plus loin", icon='📚')
    
def sidebar_contact():
    st.sidebar.title("Contact : ")
    contact = ["Antoine BARBIER",
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
        
def load_data(filename):
    BASE_DIR = Path(__file__).resolve().parent
    return pd.read_csv(BASE_DIR / "data" / filename)

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

def get_airport_info(df, full_text):
    """Retourne (lat, lon, ville) pour un aéroport donné, ou None si introuvable."""
    try:
        row = df.loc[full_text]
    except KeyError:
        return None, None, None
    lat, lon = row[["latitude_deg", "longitude_deg"]]
    ville = row["municipality"] if pd.notna(row["municipality"]) else "Non défini"
    return lat, lon, ville

def distance_ajust(distance):
    if distance < 500:
        marge = 0.12
    elif distance < 1000:
        marge = 0.1
    elif distance < 3500:
        marge = 0.07
    else :
        marge = 0.05
    return (distance * (1 + marge))

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

def card_grid(main_title, items, values, tooltips):
    cards_html = ""
    for item, value, tooltip in zip(items, values, tooltips):
        cards_html += f"""
        <div class="card animate-fadeIn">
            <span class="tooltip-trigger">?</span>
            <span class="tooltip">{tooltip}</span>
            <div class="card-value">{value}</div>
            <div class="card-title">
                {item}
            </div>
        </div>
        """

    full_html = f"""
        <div>
        <h2 style="text-align:center; font-size:2rem; font-weight:bold; color:#111827;">
            {main_title}
        </h2>
        <div class="card-container">
            {cards_html}
        </div>
        </div>
        """
    st.markdown(full_html, unsafe_allow_html=True)
    
def draw_footer(canvas, doc):
    """Dessine le footer en bas de chaque page."""
    app_url = "https://co2-airplane-calculator.streamlit.app/"
    footer_text = (
        f"© 2025 - Calculateur CO2 — "
        f"<a href='{app_url}' color='blue'>Ouvrir l’application Streamlit</a>"
    )
    from reportlab.platypus import Paragraph
    styles = getSampleStyleSheet()
    footer_style = ParagraphStyle(
        "footer_style",
        parent=styles["Normal"],
        alignment=1,  
        fontSize=9,
        textColor=colors.HexColor("#6b7280"),
    )

    p = Paragraph(footer_text, footer_style)

    width, height = A4
    w, h = p.wrap(width - 2 * 72, height)
    p.drawOn(canvas, 72, 20)  

    page_num = canvas.getPageNumber()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#9ca3af"))
    canvas.drawRightString(width - 72, 20, f"Page {page_num}")  
    
def create_pdf(all_journeys, img_path):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    card_text_style = ParagraphStyle(
        "card_text",
        parent=styles["Normal"],
        alignment=1,  # centré
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#333333"),
    )
    nb_trajets = len(all_journeys)
    dist_total = sum(journey["distance"] for journey in all_journeys)
    co2_total = sum(journey["co2_total"] for journey in all_journeys)
    elements.append(Paragraph("<b>Bilan Carbone</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    card1 = Paragraph(f"<b>Nombre de trajets :</b><br/>{nb_trajets}", card_text_style)
    card2 = Paragraph(f"<b>CO2 cumulé :</b><br/>{co2_total} kg CO2", card_text_style)
    card3 = Paragraph(f"<b>Distance totale :</b> {dist_total} km", card_text_style)
    
    elements.append(Spacer(1, 12))

    cards_data = [[card1, card2, card3]]
    table = Table(
        cards_data,
        colWidths=[150, 150],
        hAlign="CENTER",
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5f5")),
        ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#d1d5db")),
        ("INNERGRID", (0, 0), (-1, -1), 2, colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 15),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    
    for i, j in enumerate(all_journeys, 1):
        itin = j["itineraire"]
        dist = j["distance"]
        co2 = j["co2_total"]

        trajet_txt = (
            f"<b>{i}.</b> {itin} — "
            f"<font color='#2563eb'>{dist:.0f} km</font> — "
            f"<font color='#dc2626'>{co2:.0f} kg CO2</font>"
        )

        elements.append(Paragraph(trajet_txt))

    elements.append(Spacer(1, 24))
    elements.append(Paragraph("<b>Graphique :</b>", styles["Heading2"]))
    elements.append(Image(img_path, width=300, height=300))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Avec ces voyage, vous atteignez {round(co2_total/9400*100,1)}% de l'empreinte carbone annuelle moyenne d'un.e français.e dont {round(co2_total/2156*100,1)}% de l'ensemble des déplacements annuels.", styles["Normal"]))
    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    buffer.seek(0)
    return buffer
