# Calculateur d'empreinte carbone ✈️🌍

**Comparez vos voyages aériens avec l’empreinte moyenne d’un·e Français·e**

---

## Description

Ce projet a pour objectif d’illustrer comment des données environnementales peuvent être mises en valeur grâce à des outils techniques interactifs.

En renseignant simplement deux aéroports, l’application calcule les émissions de CO₂ liées au trajet en avion. Le résultat est ensuite comparé à l’empreinte carbone moyenne d’un·e Français·e et exprimé en équivalents concrets (déplacements, alimentation, habitat, etc.).

L’approche se veut avant tout **pédagogique et visuelle** : fournir un repère clair et accessible pour comprendre l’impact carbone d’un vol, tout en démontrant des compétences en traitement de données, visualisation et développement d’applications interactives.

---

## Différences avec le calculateur de l’ADEME

Le calculateur de l’ADEME fournit une estimation chiffrée des émissions de CO₂ d’un vol ou de l’empreinte carbone totale d’un individu. On obtient donc une valeur brute, exprimée en kilogrammes ou en tonnes de CO₂.  

Le présent projet a une approche complémentaire : il ne se limite pas à donner un chiffre, mais cherche à **le mettre en perspective**. L’objectif est de :

- Comparer l’impact d’un vol à l’empreinte carbone annuelle moyenne d’un·e Français·e.  
- Le replacer dans différents postes de consommation (déplacements, alimentation, habitat, etc.).  
- Fournir une échelle concrète et visuelle pour mieux appréhender ce que représente un seul vol.  

👉 Ce projet est donc avant tout **pédagogique et visuel**, et sert de **vitrine technique** (données, calculs, visualisations interactives). Il **ne remplace pas** le calculateur officiel de l’ADEME, mais fournit un contexte et des repères pour rendre ces chiffres plus parlants.

---

## Démo

Lien vers l’application en ligne : [Streamlit App](https://share.streamlit.io/ton_utilisateur/ton_depot/main/streamlit_app.py)

---

## Stack technique

L’application a été développée avec les technologies Python suivantes :

- **Streamlit** – création d’applications web interactives  
- **Pandas** – manipulation et analyse de données  
- **Plotly** – visualisation interactive de données  
- **Pathlib** – gestion des chemins de fichiers  
- **Math** – calculs géographiques et trigonométriques (distance, coordonnées)  

---

## Structure du projet

calculateur_CO2/
├─ streamlit_app.py # Point d'entrée principal
├─ pages/ # Pages supplémentaires Streamlit
├─ data/ # Fichiers de données
├─ utils.py # Fonctions utilitaires partagées
├─ requirements.txt # Dépendances Python
├─ .streamlit/ # Configuration Streamlit
└─ README.md # Documentation

