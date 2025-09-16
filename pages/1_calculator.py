import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import load_data,haversine,distance_ajust,co2_result, sidebar_contact, Navbar

def main():
    Navbar()
if __name__ == '__main__':
    main()

st.set_page_config(
    page_title="Calculateur CO2 ",  # titre de l'onglet navigateur
    page_icon="✈️")

sidebar_contact()


#region Chargement data
df_ap = load_data("df_ap.csv") #liste des aéroports
aeroports = df_ap['full_text']
df = load_data("df_items.csv") #liste des items pour le sunburst


#repartition camembert
poste = ["Alimentation","Déplacement","Habitat",
         "Admin, Santé, Éducation","Équipements","Autres services"]
pourcentage = [0.24,0.22,0.23,0.12,0.11,0.08]
montant = [i*9400 for i in pourcentage]
#endregion


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
user_input = st.text_input("Recherchez un aéroport (Ville, Pays, code IATA) :")

# Filtrage et tri dynamique
if user_input:
    filtered_df = df_ap[df_ap["full_text"].str.contains(user_input, case=False, na=False)]
    filtered_df = filtered_df.sort_values(by="score", ascending=False)  # Trier après filtrage
    filtered_options = filtered_df["full_text"].tolist()
    filtered_options.insert(0, "")  # Insert un élément vide en première position
else:
    filtered_options = df_ap.sort_values(by="score", ascending=False)["full_text"].tolist()

depart = st.selectbox("Sélectionnez un aéroport :", options=filtered_options,key="depart_selectbox")
#endregion

st.divider()

#region escale
activated = st.checkbox("Voyage avec Escale")    
if activated :
    user_input = st.text_input("Recherchez un aéroport d'escale :")

    # Filtrage et tri dynamique
    if user_input:
        filtered_df = df_ap[df_ap["full_text"].str.contains(user_input, case=False, na=False)]
        filtered_df = filtered_df.sort_values(by="score", ascending=False)  # Trier après filtrage
        filtered_options = filtered_df["full_text"].tolist()
    else:
        filtered_options = df_ap.sort_values(by="score", ascending=False)["full_text"].tolist()

    escale = st.selectbox("Sélectionnez un aéroport :", options=filtered_options,key="escale_selectbox")
#endregion
st.divider()

#region arrivee
user_input = st.text_input("Recherchez un aéroport :")
if user_input:
    filtered_df = df_ap[df_ap["full_text"].str.contains(user_input, case=False, na=False)]
    filtered_df = filtered_df.sort_values(by="score", ascending=False)  # Trier après filtrage
    filtered_options = filtered_df["full_text"].tolist()
else:
    filtered_options = df_ap.sort_values(by="score", ascending=False)["full_text"].tolist()

arrivee = st.selectbox("Sélectionnez un aéroport :", options=filtered_options,key="arrivee_selectbox")
#endregion

if st.button("Calculer"):
    latdep = df_ap.loc[df_ap['full_text']==depart,"latitude_deg"].values[0]
    longdep = df_ap.loc[df_ap['full_text']==depart,"longitude_deg"].values[0]
    if activated:
        latesc = df_ap.loc[df_ap['full_text']== escale,"latitude_deg"].values[0]
        longesc = df_ap.loc[df_ap['full_text']==escale,"longitude_deg"].values[0]
    latarr = df_ap.loc[df_ap['full_text']==arrivee,"latitude_deg"].values[0]
    longarr = df_ap.loc[df_ap['full_text']==arrivee,"longitude_deg"].values[0]

    #region Calcul des résultats
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
    
    if "co2_retour" in st.session_state:
        # Récupérer la ville de départ
        ville_depart = df_ap.loc[df_ap["full_text"] == depart, "municipality"].values
        ville_depart = ville_depart[0] if len(ville_depart) > 0 else "Non défini"

        # Récupérer la ville d'escale (si activée)
        if activated:
            ville_escale = df_ap.loc[df_ap["full_text"] == escale, "municipality"].values
            ville_escale = ville_escale[0] if len(ville_escale) > 0 else "Non défini"
        else:
            ville_escale = None

        # Récupérer la ville d'arrivée
        ville_arrivee = df_ap.loc[df_ap["full_text"] == arrivee, "municipality"].values
        ville_arrivee = ville_arrivee[0] if len(ville_arrivee) > 0 else "Non défini"

        # Affichage 
        st.markdown("### 🗺️ Itinéraire sélectionné :<br>", unsafe_allow_html=True)
        
        if ville_escale:
            itineraire = f"{ville_depart} ✈️ ➝ {ville_escale} ✈️ ➝ {ville_arrivee}"
        else:
            itineraire=f"{ville_depart} ✈️ ➝ {ville_arrivee}"
        st.markdown(f"<div style='text-align: center; font-size:20px;'>{itineraire}</div>",unsafe_allow_html=True)
    # region affichage résultat
            
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
        unsafe_allow_html=True
    )
    #endregion
    if "co2_retour" in st.session_state:
        st.markdown("<h2>Ce trajet en avion équivaut à : </h2>",unsafe_allow_html=True)
        dist_km = st.session_state["dist_km"]
        co2_aller = st.session_state["co2_aller"]
        co2_retour = st.session_state["co2_retour"]
        col1, col2, col3 = st.columns(3)
        

        with col1:
            st.metric("🥩 Steaks hachés", f"{int(co2_retour // 3)}", help="1 steak = 3 kg CO₂", delta_color='inverse')

        with col2:
            st.metric("🚄 Trajets TGV Paris-Marseille", f"{round(co2_retour / 1.1)}", help="1 AR ≈ 1.1 kg CO₂")
        
        with col3:
            st.metric("👖 Jeans", f"{round(co2_retour/25.1)}", help="1 Jean ≈25kg de CO₂" )

    
    #region Camembert
    if "co2_retour" in st.session_state:
        fig = go.Figure()

        #Camembert intérieur
        fig.add_trace(go.Pie(
            labels=poste,
            values=montant,
            hole=0.45,
            name="Moyenne française",
            sort=False,
            domain=dict(x=[0.08,0.92], y=[0.08,0.92]),
            marker=dict(colors = ["#8dd3c7","#fb8072","#ffffb3","#80b1d3","#fdb462","#b3de69"]),
            textinfo="label+percent"  
        ))

        # Camembert extérieur
        fig.add_trace(go.Pie(
            labels=["Mon voyage", " "],
            values=[co2_retour, sum(montant) - co2_retour],
            hole=0.90,  # rend le cercle intérieur plus petit
            name="Mon empreinte",
            marker=dict(colors=["#fb8072", "#FFFFFF"]),  # couleur perso + gris pour "reste"
            textinfo="percent"
        ))

        # Mise en forme
        fig.update_layout(
            title="Comparaison empreinte carbone moyenne d'un.e français.e",
            
            showlegend=True,
            width=900,
            height=700   
            )
        
        
        fig.add_annotation(
            text= "👤*",
            x = 0.5, y=0.5,
            font = dict(size = 48, color = "black"),
            showarrow=False
        )
        fig.add_annotation(
            text="*Un.e français.e consomme en moyenne 9,4 tonnes de CO₂ eq sur l'année 2023 - INSEE",
            x=0.0001,y=0.0001,
            font = dict(size = 12, color = "black"),
            showarrow=False)

        st.plotly_chart(fig)
        
        #interprétation
        st.markdown(f"Avec ce graphique, on comprend que ce seul voyage représente :blue-background[**{round(co2_retour/9400*100,1)}%** de l'empreinte carbone annuel] d'un.e français.e, dont :blue-background[**{round(co2_retour/2156*100,1)}%** de l'ensemble des déplacements annuels].")
        #endregion
        
        #region Sunburst
        if "co2_retour" in st.session_state:
            df['result'] = [round(co2_retour/i,0) for i in df['CO2']] 

            fig = px.sunburst(df, 
                            path=["cat", "subcat","Label"],
                            color= 'cat', branchvalues="total", maxdepth=2, color_discrete_sequence=["#8dd3c7", "#fb8072", "#ffffb3", "#80b1d3", "#fdb462", "#b3de69"])
            fig.update_layout(width=900,
                            height=700,
                            title = "Comparaison de votre voyage avec d'autres postes de consommation"
                            )


            for trace in fig.data:
                labels = list(trace.labels)
                parents = list(trace.parents)
                values = list(trace.values)

                # dictionnaire label -> (valeur, unité)
                label_to_val_unit = {row["Label"]: (row["result"], row["unité"]) for i, row in df.iterrows()}

                custom_text = []
                for l, p in zip(labels, parents):
                    if l in df["cat"].unique() or l in df["subcat"].unique():
                        # catégorie ou sous-catégorie : juste le label
                        custom_text.append(l)
                    else:
                        # feuille : label + valeur + unité
                        val, unit = label_to_val_unit[l]
                        custom_text.append(f"{l}<br>{val} {unit}")

                trace.text = custom_text
                trace.textinfo = "text"

            st.plotly_chart(fig)
        
        if "co2_retour" in st.session_state:
            st.subheader("💡 Vos suggestions")
            google_form="https://docs.google.com/forms/d/e/1FAIpQLSft_3YHclgWRMMWhjP3pHQAAujZ9JdtmN3_dqbI6PLWR4L8rw/viewform?embedded=true"
            st.components.v1.iframe(google_form, height=600)
