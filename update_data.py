import json
import datetime
import requests

# --- CONFIGURATION CIBLE ---
VILLE = "Saint-André"
CODE_POSTAL = "97440"
CODE_INSEE = "97411"

# =========================================================
# 1. INTELLIGENCE POLITIQUE (1983 - 2026)
# =========================================================
# Analyse : La ville est un bastion historique de droite (Virapoullé) 
# qui a basculé deux fois (Fruteau 2008, Bédier 2020).

POLITICS = {
    "kpi_maire": {
        "nom": "Joé BÉDIER",
        "parti": "DVG (Gauche)",
        "mandat": "2020 - 2026",
        "score_victoire": "52.04 %"
    },
    # La "Guerre des Blocs" : Évolution des forces sur 40 ans
    "macro_tendances": {
        "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
        "bloc_droite": [56.5, 58.2, 59.4, 52.1, 46.8, 51.6, 47.9], # J.P Virapoullé & fils
        "bloc_gauche": [43.5, 41.8, 40.6, 47.9, 53.2, 48.4, 52.0], # PCR / Fruteau / Bédier
        "abstention": [21.5, 23.5, 25.8, 27.2, 26.5, 29.6, 37.3]   # La menace silencieuse
    },
    # Archives détaillées pour le sélecteur
    "details_scrutins": {
        "2020": {
            "type": "Municipales 2020 (2nd Tour)",
            "candidats": ["Joé BÉDIER (Union Gauche)", "J.M. VIRAPOULLÉ (Droite)"],
            "scores": [52.04, 47.96],
            "couleurs": ["#e74c3c", "#3498db"],
            "analyse": "Alliance Bédier/Fruteau décisive. Basculement des quartiers Fayard/Cambuston."
        },
        "2014": {
            "type": "Municipales 2014 (2nd Tour)",
            "candidats": ["J.P. VIRAPOULLÉ (UDI)", "Joé BÉDIER (DVG)"],
            "scores": [51.58, 48.42],
            "couleurs": ["#3498db", "#e74c3c"],
            "analyse": "Retour de J.P. Virapoullé après la parenthèse Fruteau."
        },
        "2008": {
            "type": "Municipales 2008 (2nd Tour)",
            "candidats": ["Eric FRUTEAU (PCR)", "J.P. VIRAPOULLÉ (UMP)"],
            "scores": [53.20, 46.80],
            "couleurs": ["#c0392b", "#3498db"],
            "analyse": "Fin de 30 ans de règne Virapoullé. Victoire historique du PCR."
        }
    },
    # Le Benchmark des Gestionnaires
    "benchmark_maires": [
        {"periode": "2020-...", "nom": "J. BÉDIER", "bord": "Gauche", "dette_fin": "1140 € (Est.)", "style": "Social / Proximité", "color": "#e74c3c"},
        {"periode": "2014-2020", "nom": "J.P. VIRAPOULLÉ", "bord": "Droite", "dette_fin": "1120 €", "style": "Grands Travaux (Colosse)", "color": "#3498db"},
        {"periode": "2008-2014", "nom": "E. FRUTEAU", "bord": "PCR", "dette_fin": "1410 €", "style": "Structuration / Écoles", "color": "#c0392b"},
        {"periode": "1972-2008", "nom": "J.P. VIRAPOULLÉ", "bord": "Droite", "dette_fin": "Variable", "style": "Bâtisseur / Sucre", "color": "#2980b9"}
    ]
}

# =========================================================
# 2. DIAGNOSTIC SOCIAL & DÉMOGRAPHIQUE (Le Terrain)
# =========================================================
SOCIAL = {
    # Série Longue Démographie (INSEE RGP)
    "demographie_historique": {
        "annees": [1968, 1975, 1982, 1990, 1999, 2009, 2014, 2020, 2024],
        "population": [22094, 25231, 30075, 35049, 43174, 53290, 55090, 57150, 58000]
    },
    "indicateurs_precarite": {
        "taux_pauvrete": "42 %",       # Le chiffre clé
        "allocataires_caf": "16 800",
        "beneficiaires_rsa": "5 400",
        "chomage_jeunes": "48 %",      # 15-24 ans
        "comparaison_region": [42, 37] # St-André vs Réunion
    },
    "education": {
        "illettrisme_jdc": "22.5 %",
        "sans_diplome": "39 %"
    }
}

# =========================================================
# 3. SÉCURITÉ & FINANCES (Les points chauds)
# =========================================================
REGALIEN = {
    # Évolution Délinquance (Estimations basées SSMSI)
    "securite_trend": {
        "annees": [2015, 2017, 2019, 2020, 2021, 2022, 2023],
        "faits": [2300, 2250, 1980, 1900, 2050, 2200, 2150]
    },
    # Évolution de la Dette par Habitant
    "finances_trend": {
        "annees": [2013, 2015, 2017, 2019, 2021, 2023],
        "dette": [1350, 1380, 1250, 1100, 1150, 1140]
    },
    "impots_2023": {
        "foncier_bati": "38.50 %",
        "foncier_non_bati": "45.20 %"
    }
}

# =========================================================
# 4. ORCHESTRATEUR
# =========================================================
def get_live_economy():
    """Récupère les entreprises actives en temps réel"""
    try:
        url = f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1"
        r = requests.get(url, timeout=4)
        return f"{r.json().get('total_results', 5000):,}".replace(",", " ")
    except:
        return "5 000+"

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # 1. Agrégation des données
    data = {
        "meta": {
            "last_update": now,
            "version": "WAR_ROOM_V3"
        },
        "kpi_global": {
            "pop": f"{SOCIAL['demographie_historique']['population'][-1]:,}".replace(",", " "),
            "entreprises": get_live_economy(),
            "dette": REGALIEN['finances_trend']['dette'][-1],
            "pauvrete": SOCIAL['indicateurs_precarite']['taux_pauvrete']
        },
        "politique": POLITICS,
        "social": SOCIAL,
        "regalien": REGALIEN
    }

    # 2. Export
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Base de données Saint-André (1968-2024) générée avec succès.")

if __name__ == "__main__":
    main()
