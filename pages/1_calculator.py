import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import load_data,haversine,distance_ajust,co2_result, sidebar_contact, Navbar, card_grid
from streamlit_searchbox import st_searchbox


def main():
    Navbar()
if __name__ == '__main__':
    main()

st.set_page_config(
    page_title="Calculateur CO2 ",  # titre de l'onglet navigateur
    page_icon="✈️",
    layout="centered")

#Chargement du sommaire
sidebar_contact()

#Chargement Tailwind
tailwind_cdn = """<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">"""
st.markdown(tailwind_cdn, unsafe_allow_html=True)


#region Chargement data
df_ap = load_data("df_ap.csv") #liste des aéroports
df_ap= df_ap.sort_values(by="score", ascending = False)
aeroports = df_ap['full_text']
df = load_data("df_items.csv") #liste des items pour le sunburst


#repartition camembert
poste = ["Alimentation","Déplacement","Habitat",
         "Admin, Santé, Éducation","Équipements","Autres services"]
pourcentage = [0.24,0.22,0.23,0.12,0.11,0.08]
montant = [i*9400 for i in pourcentage]
#endregion

#Titre de la section
st.markdown("""
<div style="background-color:#4CAF50; padding:15px; border-radius:10px">
    <h1 style="color:white; text-align:center;">🌍 Calculateur d'empreinte carbone</h1>
    <p style="color:white; text-align:center; font-size:18px;">
        Comparez vos voyages aériens avec l’empreinte moyenne d’un·e français·e
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

#region depart
def search_airports(searchterm: str): # Fonction filtrage et tri dynamique
    if not searchterm:
        return []
    filtered = df_ap[df_ap["full_text"].str.contains(searchterm, case=False, na=False)]
    return filtered["full_text"].head(10).tolist()  # limite à 10 suggestions

depart = st_searchbox(
    search_airports,
    key="depart",
    placeholder="D'où partez-vous ?",
    label="Recherchez un aéroport (Ville, Pays, code IATA) :")   
#endregion

st.divider()

#region escale
activated = st.checkbox("Voyage avec Escale")    
if activated :
    escale = st_searchbox(
        search_airports,
        key="escale",
        placeholder="Recherchez un aéroport d'escale...",
        label="Aéroport d'escale")
#endregion

st.divider()

#region arrivee
arrivee = st_searchbox(
    search_airports,
    key="arrivee",
    placeholder="Où arrivez-vous ?",
    label="Recherchez un aéroport (Ville, Pays, code IATA) :")
#endregion

#region Calcul des résultats
if st.button("Calculer"):
    latdep = df_ap.loc[df_ap['full_text']==depart,"latitude_deg"].values[0]
    longdep = df_ap.loc[df_ap['full_text']==depart,"longitude_deg"].values[0]
    if activated:
        latesc = df_ap.loc[df_ap['full_text']== escale,"latitude_deg"].values[0]
        longesc = df_ap.loc[df_ap['full_text']==escale,"longitude_deg"].values[0]
    latarr = df_ap.loc[df_ap['full_text']==arrivee,"latitude_deg"].values[0]
    longarr = df_ap.loc[df_ap['full_text']==arrivee,"longitude_deg"].values[0]

    if activated: 
        voyage1 = haversine(latdep,longdep,latesc,longesc)
        voyage2 = haversine(latesc,longesc,latarr,longarr)
        dist_km = distance_ajust(voyage1)+distance_ajust(voyage2)
        co2_aller = round(co2_result(dist_km))
        co2_retour = round(co2_aller * 2)          
        

    else :
        voyage1 = (haversine(latdep,longdep,latarr,longarr))
        dist_km=round(distance_ajust(voyage1))
        co2_aller = round(co2_result(dist_km))
        co2_retour = round(co2_aller * 2)
    
    st.session_state["dist_km"] = round(dist_km)
    st.session_state["co2_aller"] = co2_aller
    st.session_state["co2_retour"] = co2_retour

#endregion
    
    #Affichage de l'itinéraire    
    if "co2_retour" in st.session_state:
        ville_depart = df_ap.loc[df_ap["full_text"] == depart, "municipality"].values
        ville_depart = ville_depart[0] if len(ville_depart) > 0 else "Non défini"
        if activated:
            ville_escale = df_ap.loc[df_ap["full_text"] == escale, "municipality"].values
            ville_escale = ville_escale[0] if len(ville_escale) > 0 else "Non défini"
        else:
            ville_escale = None
        ville_arrivee = df_ap.loc[df_ap["full_text"] == arrivee, "municipality"].values
        ville_arrivee = ville_arrivee[0] if len(ville_arrivee) > 0 else "Non défini"

        st.markdown('<h2 class="text-3xl font-bold tracking-tight text-gray-900 text-center">Itinéraire sélectionné :</h2>',unsafe_allow_html=True)
        
        if ville_escale:
            itineraire = f"{ville_depart} ✈️ ➝ {ville_escale} ✈️ ➝ {ville_arrivee}"
        else:
            itineraire=f"{ville_depart} ✈️ ➝ {ville_arrivee}"
        st.markdown(f"<div style='text-align: center; font-size:20px;'>{itineraire}</div>",unsafe_allow_html=True)

#region Cards Distance, CO2 Aller, CO2 AR            
    st.markdown(
        f"""
        <style>
        .results-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
            margin-bottom: 10px;
            animation: fadeIn 1s ease-in-out;
        }}

        .result-box {{
            background-color: #f0f2f6;
            border: 2px solid #cccccc;
            border-radius: 12px;
            padding: 30px;
            min-width: 280px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #333;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .result-box:hover {{
            transform: scale(1.03);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }}

        .big-result {{
            background: linear-gradient(145deg, #dff6ff, #c2e9fb);
            border: 3px solid #1890ff;
            border-radius: 14px;
            padding: 40px;
            margin-top: 30px;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #003366;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            animation: fadeIn 1s ease-in-out;

        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes popIn {{
            0% {{
                transform: scale(0.8);
                opacity: 0;
            }}
            100% {{
                transform: scale(1);
                opacity: 1;
            }}
        }}
        </style>

        <div class="results-container">
            <div class="result-box">
                ✈️ Distance : {round(dist_km)} km
            </div>
            <div class="result-box">
                🌍 CO₂ Aller : {co2_aller} kg
            </div>
        </div>

        <div class="big-result">
            🔁 Aller-Retour : {co2_retour} kg CO₂
        </div>
        """,
        unsafe_allow_html=True)
#endregion

#region Cards Data
    if "co2_retour" in st.session_state:
        card_grid("Ce trajet en avion équivaut à :",
                  ["🥩 Steaks hachés", "🚄 Trajets TGV Paris-Marseille", "👖 Jeans"],
                  [round(co2_retour/3,ndigits=None),round(co2_retour/1.1,ndigits=None),round(co2_retour/25,ndigits=None)],
                  ["1 steak = 3 kg CO₂", "1 trajet ≈ 1.1 kg CO₂", "1 jean = 25 kg CO₂"])
#endregion

#region Camembert
    if "co2_retour" in st.session_state:
        
        st.markdown("""
        <div class="bg-white py-16">
            <div class="mx-auto max-w-4xl text-center -mb-10 -mt-20">
            <h2 class="text-3xl font-bold tracking-tight text-gray-900">
            Comparaison de votre vol avec l'empreinte carbone moyenne d'un.e français.e
            </h2>
        </div>""",unsafe_allow_html=True)
        fig = go.Figure()
        # Camembert intérieur
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

        # Camembert extérieur (mon voyage vs reste)
        fig.add_trace(go.Pie(
            labels=["Mon voyage", "Reste"],
            values=[co2_retour, sum(montant) - co2_retour],
            hole=0.88,
            name = "Mon voyage",
            marker=dict(colors=["#fb8072", "#FFFFFF"],line=dict(color="gray", width=[1,0])),
            text=["Mon voyage {:.1f}%".format(co2_retour/sum(montant)*100), ""],  # texte seulement pour "Mon voyage"
            textinfo="text",
            textposition="inside",
            hovertemplate=[f"✈️ Mon voyage<br>{co2_retour:.0f} kg CO₂ eq<br>({round(co2_retour/sum(montant)*100,1)}%)<extra></extra>", "<extra></extra>"],
            
        ))

        # Mise en forme
        fig.update_layout(
            showlegend=False,
            width=700,
            height=700,
            margin=dict(t=0, b=0, l=0, r=0)
        )

        # Annotation centrale
        fig.add_annotation(
            text="👤*",
            x=0.5, y=0.5,
            font=dict(size=48, color="black"),
            showarrow=False
        )

        # Source en bas
        fig.add_annotation(
            text="*Un.e français.e consomme en moyenne 9,4 tCO₂ eq en 2023 - INSEE",
            x=0.5, y=0.01,  # placé dans la zone visible
            xref="paper", yref="paper",
            font=dict(size=12, color="black"),
            showarrow=False
        )


        # Affichage Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Interprétation
        st.markdown(
            f"Avec ce graphique, on comprend que ce seul voyage représente "
            f":blue-background[**{round(co2_retour/9400*100,1)}%** de l'empreinte carbone annuel] "
            f"d'un.e français.e, dont :blue-background[**{round(co2_retour/2156*100,1)}%** "
            f"de l'ensemble des déplacements annuels]."
        )
        st.divider()
        #region Sunburst
        if "co2_retour" in st.session_state:
            
            
            
            df['result'] = [round(co2_retour/i,0) for i in df['CO2']] 
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
        
        if "co2_retour" in st.session_state:
            st.subheader("💡 Vos suggestions")
            google_form="https://docs.google.com/forms/d/e/1FAIpQLSft_3YHclgWRMMWhjP3pHQAAujZ9JdtmN3_dqbI6PLWR4L8rw/viewform?embedded=true"
            st.components.v1.iframe(google_form, height=600)
