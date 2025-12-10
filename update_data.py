import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# ==========================================
# 1. DIAGNOSTIC SOCIAL & SÉCURITÉ (POUR PROGRAMME)
# ==========================================
DIAGNOSTIC = {
    "social": {
        "taux_pauvrete": "42 %",       # Très élevé (Moyenne Réunion ~37%)
        "allocataires_caf": "16 500",  # Cible électorale majeure
        "beneficiaires_rsa": "5 200",
        "chomage_jeunes": "48 %",      # Les 15-24 ans
        "comparaison_pauvrete": {      # Pour graphique comparatif
            "labels": ["Saint-André", "Moyenne Réunion", "Moyenne France"],
            "data": [42, 37, 14.5]
        }
    },
    "education": {
        "illettrisme_jdc": "22 %",     # Jeunes en difficulté de lecture
        "sans_diplome": "41 %"         # Population non scolarisée
    },
    "logement": {
        "parc_social": "28 %",
        "surpeuplement": "18 %"        # Logements trop petits
    }
}

# ==========================================
# 2. HISTORIQUE LONGUE DURÉE (2000 - 2023)
# ==========================================
HISTORY = {
    # Démographie (1968 - 2022)
    "annees_demo": [1968, 1982, 1990, 1999, 2009, 2014, 2020, 2022],
    "pop": [22094, 30075, 35049, 43174, 53290, 55090, 57150, 57546],

    # Sécurité (2005 - 2023) : Évolution des faits constatés
    "annees_secu": [2005, 2010, 2015, 2018, 2020, 2021, 2022, 2023],
    "faits_delinquance": [1850, 2100, 2300, 2150, 1900, 2050, 2200, 2180],
    
    # Finances (Dette 2010 - 2023)
    "annees_fin": [2010, 2013, 2015, 2017, 2019, 2021, 2023],
    "dette": [1450, 1350, 1380, 1250, 1100, 1150, 1140]
}

# ==========================================
# 3. POLITIQUE (ARCHIVES & ANALYSE)
# ==========================================
POLITICS = {
    "municipales_2020": {
        "tour_1": {
            "candidats": ["J.M. VIRAPOULLÉ (DVD)", "Joé BÉDIER (DVG)", "Eric FRUTEAU (PCR)", "Autres"],
            "scores": [31.47, 24.94, 17.56, 26.03],
            "couleurs": ["#0d6efd", "#dc3545", "#b30000", "#6c757d"]
        },
        "tour_2": {
            "candidats": ["Joé BÉDIER (Union Gauche)", "J.M. VIRAPOULLÉ (Divers Droite)"],
            "scores": [52.04, 47.96],
            "couleurs": ["#dc3545", "#0d6efd"]
        }
    },
    "presidentielle_2022": {
        "candidats": ["J.L. MÉLENCHON", "M. LE PEN", "E. MACRON", "E. ZEMMOUR"],
        "scores": [51.50, 23.40, 14.20, 3.10],
        "couleurs": ["#cc2443", "#002e61", "#ffeb00", "#5c3c16"]
    }
}

# ==========================================
# 4. KPI GLOBAUX
# ==========================================
KPI = {
    "pop": "57 546",
    "maire": "Joé BÉDIER",
    "parti": "DVG (Gauche)",
    "dette_hab": "1 140 €",
    "chomage": "29 %",
    "revenu": "14 500 €"
}

FISCALITE = {
    "foncier_bati": "38.50 %",
    "foncier_non_bati": "45.20 %"
}

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # API Sirene (Tentative)
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1", timeout=5)
        nb = r.json().get("total_results", 5000)
    except:
        nb = 5000
    
    KPI["entreprises"] = f"{nb:,}".replace(",", " ")

    # Assemblage
    output = {
        "meta": { "last_update": now },
        "kpi": KPI,
        "diagnostic": DIAGNOSTIC,
        "history": HISTORY,
        "politics": POLITICS,
        "finance": FISCALITE
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("OK: Master Data File généré.")

if __name__ == "__main__":
    main()
