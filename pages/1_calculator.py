import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import load_data,haversine,distance_ajust,co2_result, sidebar_contact, Navbar, card_grid, get_airport_info,create_pdf
from streamlit_searchbox import st_searchbox
import pathlib
import tempfile
import time

#region Config
def main():
    Navbar()
if __name__ == '__main__':
    main()
    
st.set_page_config(
    page_title="Calculateur CO2 ",  # titre de l'onglet navigateur
    page_icon="✈️",
    layout="centered")

sidebar_contact()

df_ap = load_data("df_ap.csv") #liste des aéroports
df_ap= df_ap.sort_values(by="score", ascending = False)
df_ap=df_ap.set_index("full_text") 
df = load_data("df_items.csv") #liste des items pour le sunburst

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("assets/style.css")
load_css(css_path)

#repartition camembert
poste = ["Alimentation","Déplacement","Habitat",
         "Admin, Santé, Éducation","Équipements","Autres services"]
pourcentage = [0.24,0.22,0.23,0.12,0.11,0.08]
montant = [i*9400 for i in pourcentage]

st.markdown("""
<div style="background-color:#4CAF50; padding:15px; border-radius:10px">
    <h1 style="color:white; text-align:center;">🌍 Calculateur d'empreinte carbone</h1>
    <p style="color:white; text-align:center; font-size:18px;">
        Comparez vos voyages aériens avec l’empreinte moyenne d’un·e français·e
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()
#endregion

#region Interface
def search_airports(searchterm: str):
    if not searchterm:
        return []
    filtered = df_ap.reset_index()
    filtered = filtered[filtered["full_text"].str.contains(searchterm, case=False, na=False)]
    return filtered["full_text"].head(10).tolist()

depart = st_searchbox(
    search_airports,
    key="depart",
    placeholder="D'où partez-vous ?",
    label="Recherchez un aéroport (Ville, Pays, code IATA) :",
    help="⚠️ La liste des aéroports est en anglais",
)
def reset_escales():
    if "escales" in st.session_state:
        del st.session_state.escales

def add_escale():
    st.session_state.escales.append(None)

def remove_escale(idx):
    st.session_state.escales.pop(idx)
    if len(st.session_state.escales) == 0:
        st.session_state.toggle_escale = False
        del st.session_state.escales

toggle = st.toggle(
    "Voyage avec escale",
    key="toggle_escale",
    help="Vous pouvez ajouter jusqu'à 3 escales",
    on_change=reset_escales,
)

if toggle:
    if "escales" not in st.session_state:
        st.session_state.escales = [None]

    for i, escale in enumerate(st.session_state.escales):
        with st.container(horizontal=True, horizontal_alignment="center", key=f"container_escale_{i}"):
            st.session_state.escales[i] = st_searchbox(
                search_airports,
                key=f"sb_escale_{i}",
                placeholder=f"Escale {i+1} (Ville, Pays, code IATA)...",
                label=f"Aéroport d’escale {i+1}",
            )

            st.button(
                "",
                icon=":material/delete:",
                key=f"escale_delete_{i}",
                on_click=remove_escale,
                args=(i,),
            )

    if len(st.session_state.escales) < 3:
        st.button(
            "",
            icon=":material/add:",
            key="escale_add",
            on_click=add_escale,
        )

arrivee = st_searchbox(
    search_airports,
    key="arrivee",
    placeholder="Où arrivez-vous ?",
    label="Recherchez un aéroport (Ville, Pays, code IATA) :",
    help="⚠️ La liste des aéroports est en anglais",
)
#endregion

#region Calcul
if st.button("Calculer", key='calcul_button', icon=":material/calculate:"):
    trajet = []
    distances = []

    lat, lon, ville = get_airport_info(df_ap, depart)
    if lat is None:
        st.error("Aéroport de départ introuvable ⚠️")
        st.stop()
    trajet.append({"coords": (lat, lon), "ville": ville})

    if toggle:
        for escale in st.session_state.escales:
            if escale:
                lat, lon, ville = get_airport_info(df_ap, escale)
                if lat is None:
                    st.warning(f"Escale '{escale}' introuvable, ignorée ⚠️")
                    continue
                trajet.append({"coords": (lat, lon), "ville": ville})

    lat, lon, ville = get_airport_info(df_ap, arrivee)
    if lat is None:
        st.error("Aéroport d'arrivée introuvable ⚠️")
        st.stop()
    trajet.append({"coords": (lat, lon), "ville": ville})

    # Distances et CO2
    for depart_point, arrivee_point in zip(trajet[:-1], trajet[1:]):
        dist_segment = distance_ajust(haversine(*depart_point["coords"], *arrivee_point["coords"]))
        distances.append(dist_segment)
    dist_km= round(sum(distances))
    co2_aller= round(sum(co2_result(d) for d in distances))
    co2_total= co2_aller*2
    
    st.session_state["dist_km"] = dist_km
    st.session_state["co2_aller"] = co2_aller
    st.session_state["co2_total"] = co2_total
    
    st.markdown(
        
        '<h2 style="text-align:center; font-size:2rem; font-weight:bold; color:#111827;">Itinéraire sélectionné :</h2>',
        unsafe_allow_html=True,
    )
    itineraire = " ➝ ".join([etape["ville"] for etape in trajet])
    st.markdown(f"<div style='text-align: center; font-size:20px;'>{itineraire}</div>", unsafe_allow_html=True)

    st.session_state["last_journey"] = {
        "itineraire": itineraire,
        "distance": dist_km,
        "co2_total": co2_total
    }
#endregion

#region Cards
    st.markdown(
            f"""
            <div class="result-cards animate-fadeIn">
                <div class="result-card">✈️ Distance : {round(dist_km)} km</div>
                <div class="result-card">🌍 CO₂ Aller : {round(co2_aller)} kg </div>
            </div>
            <div class ="result-summary animate-fadeIn">
                🔁 Aller-Retour : {co2_total} kg CO₂
            </div>                
            """,unsafe_allow_html=True)    
    
    if "co2_total" in st.session_state:
        card_grid("Ce trajet en avion équivaut à :",
                  ["🥩 Steaks hachés", "🚄 Trajets TGV Paris-Marseille", "👖 Jeans"],
                  [round(co2_total/3,ndigits=None),round(co2_total/1.1,ndigits=None),round(co2_total/25,ndigits=None)],
                  ["1 steak = 3 kg CO₂", "1 trajet ≈ 1.1 kg CO₂", "1 jean = 25 kg CO₂"])
#endregion

#region Camembert
    if "co2_total" in st.session_state:
        
        st.markdown("""
        <div class="bg-white py-16">
            <div class="mx-auto max-w-4xl text-center -mb-10 -mt-20">
            <h2 class="text-3xl font-bold tracking-tight text-gray-900">
            Comparaison de votre vol avec l'empreinte carbone moyenne d'un.e français.e
            </h2>
        </div>""",unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=poste,
            values=montant,
            hole=0.38,
            name="Moyenne française",
            sort=False,
            domain=dict(x=[0.08,0.92], y=[0.08,0.92]),
            marker=dict(colors=["#8dd3c7","#fb8072","#ffffb3","#80b1d3","#fdb462","#b3de69"]),
            textinfo="label+percent",
            hovertemplate="%{label}<br>%{value:.0f} kg CO₂ eq<br>(%{percent})<extra></extra>"
        ))

        fig.add_trace(go.Pie(
            labels=["Mon voyage", "Reste"],
            values=[co2_total, sum(montant) - co2_total],
            hole=0.88,
            name = "Mon voyage",
            marker=dict(colors=["#fb8072", "#FFFFFF"],line=dict(color="gray", width=[1,0])),
            text=["Mon voyage {:.1f}%".format(co2_total/sum(montant)*100), ""],  # texte seulement pour "Mon voyage"
            textinfo="text",
            textposition="inside",
            hovertemplate=[f"✈️ Mon voyage<br>{co2_total:.0f} kg CO₂ eq<br>({round(co2_total/sum(montant)*100,1)}%)<extra></extra>", "<extra></extra>"],
            
        ))

        fig.update_layout(
            showlegend=False,
            width=700,
            height=700,
            margin=dict(t=0, b=0, l=0, r=0)
        )

        fig.add_annotation(
            text="👤*",
            x=0.5, y=0.5,
            font=dict(size=48, color="black"),
            showarrow=False
        )

        fig.add_annotation(
            text="*Un.e français.e consomme en moyenne 9,4 tCO₂ eq en 2023 - INSEE",
            x=0.5, y=0.0001,  # placé dans la zone visible
            xref="paper", yref="paper",
            font=dict(size=12, color="black"),
            showarrow=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f"Avec ce voyage, vous atteignez"
            f":blue-background[**{round(co2_total/9400*100,1)}%** de l'empreinte carbone annuel] "
            f"d'un.e français.e, dont :blue-background[**{round(co2_total/2156*100,1)}%** "
            f"de l'ensemble des déplacements annuels]."
        )
#endregion

#region Sunburst
    if "co2_total" in st.session_state:
        
        df['result'] = [round(co2_total/i,0) for i in df['CO2']] 
        st.markdown("""
    <div class="bg-white py-16">
        <div class="mx-auto max-w-4xl text-center -mb-10 -mt-20">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900">
        Comparaison de votre vol avec l'empreinte carbone moyenne d'un.e français.e
        </h2>
    </div>""",unsafe_allow_html=True)
        fig = px.sunburst(df, 
                        path=["cat", "subcat","Label"],
                        color= 'cat', branchvalues="total", maxdepth=2, color_discrete_sequence=["#8dd3c7", "#fb8072", "#ffffb3", "#80b1d3", "#fdb462", "#b3de69"])
        fig.update_layout(width=900,
                        height=700,
                        margin=dict(t=0,b=0,l=0,r=0)
                        )


        for trace in fig.data:
            labels = list(trace.labels)
            parents = list(trace.parents)
            values = list(trace.values)

            # dictionnaire label -> (valeur, unité)
            label_to_val_unit = {row["Label"]: (row["result"], row["unité"]) for i, row in df.iterrows()}

            custom_text = []
            for o, p in zip(labels, parents):
                if o in df["cat"].unique() or o in df["subcat"].unique():
                    # catégorie ou sous-catégorie : juste le label
                    custom_text.append(o)
                else:
                    # feuille : label + valeur + unité
                    val, unit = label_to_val_unit[o]
                    custom_text.append(f"{o}<br>{val} {unit}")

            trace.text = custom_text
            trace.textinfo = "text"

        st.plotly_chart(fig)
#endregion

#region Bilan
if "all_journeys" not in st.session_state:
    st.session_state["all_journeys"] = []
    
if "show_bilan" not in st.session_state:
    st.session_state["show_bilan"] = False

if "pdf_buffer" not in st.session_state:
    st.session_state["pdf_buffer"] = None

if "last_journey" in st.session_state:
    col1, col2 = st.columns(2)

    with col1:
        add_button = st.button("Ajouter ce trajet à la liste", icon=":material/airplane_ticket:", use_container_width=True, key = "add_journey_button")

    with col2:
        reset_button = st.button("Réinitialiser la liste",icon=":material/restart_alt:", use_container_width=True, disabled=not st.session_state["all_journeys"], key = "reset_journey_button")
        
    if len(st.session_state["all_journeys"]) >= 2:
        bouton_bilan = st.button("Afficher le bilan", icon=":material/assignment:",key = "bilan_button")
        if bouton_bilan:
            st.session_state["show_bilan"]= not st.session_state["show_bilan"]

    if add_button and "last_journey" in st.session_state:
        st.session_state["all_journeys"].append(st.session_state["last_journey"])
        st.success("✅ Trajet ajouté à la liste !")
        st.rerun()

    if reset_button:
        st.session_state["all_journeys"].clear()
        st.warning("Liste des trajets réinitialisée 🧹")
        st.rerun()

    if st.session_state["all_journeys"]:
        st.markdown("### ✈️ Vos trajets ajoutés :")
        total_co2 = sum(j["co2_total"] for j in st.session_state["all_journeys"])
        dist_total = sum(j["distance"] for j in st.session_state["all_journeys"])

        for idx, j in enumerate(st.session_state["all_journeys"], 1):
            st.markdown(
                f"**{idx} - {j['itineraire']}** — {j['distance']} km — {j['co2_total']} kg CO₂"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**🌍 Total cumulé : {dist_total} km — {total_co2} kg CO₂**")

if len(st.session_state["all_journeys"]) >= 2 and st.session_state["show_bilan"]:
    total_co2 = sum(j["co2_total"] for j in st.session_state["all_journeys"])
    st.markdown("---")
    st.markdown("## 🌍 Bilan cumulé de vos trajets")

    st.markdown(
        f"""
        <div class="result-cards animate-fadeIn">
            <div class="result-card">🔢 Nombre de trajets : {len(st.session_state["all_journeys"])}</div>
            <div class="result-card">🌍 CO₂ cumulé : {total_co2} kg</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    card_grid("Ces trajets en avion équivalent à :",
            ["🥩 Steaks hachés", "🚄 Trajets TGV Paris-Marseille", "👖 Jeans"],
            [round(total_co2/3), round(total_co2/1.1), round(total_co2/25)],
            ["1 steak = 3 kg CO₂", "1 trajet ≈ 1.1 kg CO₂", "1 jean = 25 kg CO₂"])

    st.markdown("""
    <div class="bg-white py-16">
        <div class="mx-auto max-w-4xl text-center -mb-10 -mt-20">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900">
        Comparaison de vos vols cumulés avec l'empreinte carbone moyenne d'un.e français.e
        </h2>
    </div>""",unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=poste,
        values=montant,
        hole=0.38,
        name="Moyenne française",
        sort=False,
        domain=dict(x=[0.08,0.92], y=[0.08,0.92]),
        marker=dict(colors=["#8dd3c7","#fb8072","#ffffb3","#80b1d3","#fdb462","#b3de69"]),
        textinfo="label+percent",
        hovertemplate="%{label}<br>%{value:.0f} kg CO₂ eq<br>(%{percent})<extra></extra>"
    ))
    
    labels_voyage = [f"voyage {i+1}" for i in range(len(st.session_state["all_journeys"]))]
    labels_voyage.append("Reste")
    values_voyage = [j["co2_total"] for j in st.session_state["all_journeys"]]
    values_voyage.append(sum(montant) - sum(values_voyage))
    
    couleurs = ["#fb8072", "#e76051", "#c4210e", "#aa1f10", "#891a0d", "#fb8072"]
    couleurs = couleurs[:len(labels_voyage)-1]
    couleurs.append("#FFFFFF")
    fig.add_trace(go.Pie(
        labels=labels_voyage,
        values=values_voyage,
        hole=0.88,
        name = "Mes voyages",
        marker=dict(colors=couleurs,line=dict(color="gray", width=[1,0])),
        text=["Mes voyages {:.1f}%".format(total_co2/sum(montant)*100), ""],
        textinfo="label",
        textposition="inside",
    ))
    fig.update_layout(
        showlegend=False,
        width=700,
        height=700,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    fig.add_annotation(
        text="👤*",
        x=0.5, y=0.5,
        font=dict(size=48, color="black"),
        showarrow=False
    )
    fig.add_annotation(
        text="*Un.e français.e consomme en moyenne 9,4 tCO₂ eq en 2023 - INSEE",
        x=0.5, y=0.0001,
        xref="paper", yref="paper",
        font=dict(size=12, color="black"),
        showarrow=False
    )
    st.plotly_chart(fig, use_container_width=True)
    #endregion
    
    with tempfile.NamedTemporaryFile(suffix=".png",delete=False) as tmp_img:
        img_path=tmp_img.name
        fig.write_image(img_path, engine="kaleido") 

    st.markdown(
        f"Avec ces voyages, vous atteignez "
        f":blue-background[**{round(total_co2/9400*100,1)}%** de l'empreinte carbone annuelle] "
        f"d'un.e français.e, dont :blue-background[**{round(total_co2/2156*100,1)}%** "
        f"de l'ensemble des déplacements annuels].<br></br>", unsafe_allow_html=True
    )
            
    if st.button("Générer le PDF", icon=":material/build_circle:", key="generate_pdf_button"):
        pdf_buffer = create_pdf(st.session_state["all_journeys"], img_path)
        with st.spinner("Préparation du PDF...",show_time=True):
            time.sleep(3)
            st.success("PDF prêt !")
        
        st.download_button(
            label="Télécharger le bilan au format PDF",
            data=pdf_buffer,
            file_name="bilan_carbone.pdf",
            mime="application/pdf",
            icon=":material/file_download:",
            key="download_pdf_button"
        )
