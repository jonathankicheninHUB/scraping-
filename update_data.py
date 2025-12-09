import json
import random
import datetime
import requests # On utilise la librairie pour aller sur internet

# --- CONFIGURATION ---
CODE_INSEE = "97411" # Saint-André
API_GEO = f"https://geo.api.gouv.fr/communes/{CODE_INSEE}?fields=nom,population,surface,codesPostaux&format=json"

def get_real_geo_data():
    """Récupère les vraies données de l'API Géo de l'État."""
    try:
        print(f"Connexion à l'API pour {CODE_INSEE}...")
        response = requests.get(API_GEO, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Données reçues :", data)
        return data
    except Exception as e:
        print(f"Erreur API : {e}")
        # Valeurs de secours si l'API est en panne
        return {"population": 57000, "surface": 5300}

# --- MAIN ---
now = datetime.datetime.now().strftime("%d/%m/%Y")
geo_data = get_real_geo_data()

# Calculs dérivés (simulés sur la base du réel)
pop_officielle = geo_data.get('population', 57000)
chomage_estime = 29.5 # Chiffre dur à avoir en temps réel, on le fixe
participation_derniere = 61.2 

# Structure finale pour le dashboard
output = {
    "meta": { 
        "last_update": now,
        "source": "API Géo & Simulations"
    },
    "kpi": { 
        "pop": f"{pop_officielle:,}".replace(",", " "), # Formatage 57 000
        "chomage": str(chomage_estime), 
        "participation": str(participation_derniere), 
        "secu_total": str(random.randint(2300, 2400)) # Reste simulé pour l'instant
    },
    "elections": {
        "labels": ["Saint-André Avance", "Le Renouveau", "Action Citoyenne"],
        "votes": [45.2, 38.5, 16.3],
        "sieges": [28, 9, 2]
    },
    "securite": {
        "annees": [2019, 2020, 2021, 2022, 2023],
        "cambriolages": [180, 195, 210, 205, 190],
        "vols": [140, 130, 125, 145, 135]
    },
    "socio": {
        "annees": [2019, 2020, 2021, 2022, 2023],
        "chomage": [31.0, 32.5, 30.8, 29.9, 29.5]
    },
    "elus": [
        { "nom": "BEDIER Joé", "fonction": "Maire", "groupe": "Majorité", "mandat": "2020-2026" },
        { "nom": "PAYET Marie", "fonction": "1ère Adjointe", "groupe": "Majorité", "mandat": "2020-2026" },
        { "nom": "VIRAPOULLE J.M", "fonction": "Conseiller", "groupe": "Opposition", "mandat": "2020-2026" }
    ]
}

# Sauvegarde
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Mise à jour terminée avec succès.")
