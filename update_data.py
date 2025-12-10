import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# ==========================================
# 1. BENCHMARK DES MAIRES (1983 - 2024)
# ==========================================
# Analyse comparative des performances par mandat
BENCHMARK_MANDATS = [
    {
        "periode": "2020 - ...",
        "maire": "Joé BÉDIER",
        "tendance": "Union Gauche",
        "dette_fin_mandat": "1 140 € (En cours)", # Est. 2023
        "pop_evolution": "+1.2 % / an",
        "faits_marquants": "Social, Rénovation urbaine",
        "couleur": "#dc3545" # Rouge
    },
    {
        "periode": "2014 - 2020",
        "maire": "J-Paul VIRAPOULLÉ",
        "tendance": "Droite (UDI)",
        "dette_fin_mandat": "1 120 €",
        "pop_evolution": "+0.5 % / an",
        "faits_marquants": "Désendettement, Colosse",
        "couleur": "#0d6efd" # Bleu
    },
    {
        "periode": "2008 - 2014",
        "maire": "Eric FRUTEAU",
        "tendance": "PCR (Gauche)",
        "dette_fin_mandat": "1 410 €",
        "pop_evolution": "+1.8 % / an",
        "faits_marquants": "Investissements scolaires",
        "couleur": "#b30000" # Rouge foncé
    },
    {
        "periode": "1972 - 2008",
        "maire": "J-Paul VIRAPOULLÉ",
        "tendance": "UDF/UMP (Droite)",
        "dette_fin_mandat": "NC",
        "pop_evolution": "+3.5 % / an (Boom)",
        "faits_marquants": "Transformation Ville, Sucre",
        "couleur": "#0d6efd"
    }
]

# ==========================================
# 2. ARCHIVES ÉLECTORALES COMPLÈTES (1983-2020)
# ==========================================
MACRO_ELECTIONS = {
    "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
    "scores_droite": [54.0, 56.5, 58.2, 52.1, 46.8, 51.6, 47.9], # Virapoullé Dynastie
    "scores_gauche": [45.0, 42.0, 40.5, 46.5, 53.2, 48.4, 52.0], # PCR / Union
    "participation": [78.5, 76.0, 74.5, 72.0, 73.5, 70.4, 62.7]  # Chute progressive
}

# ==========================================
# 3. DIAGNOSTIC SOCIAL & SÉCURITÉ (EXISTANT)
# ==========================================
DIAGNOSTIC = {
    "social": {
        "taux_pauvrete": "42 %",
        "allocataires_caf": "16 500",
        "beneficiaires_rsa": "5 200",
        "chomage_jeunes": "48 %",
        "comparaison_pauvrete": {
            "labels": ["Saint-André", "Moyenne Réunion", "Moyenne France"],
            "data": [42, 37, 14.5]
        }
    },
    "education": {
        "illettrisme_jdc": "22 %",
        "sans_diplome": "41 %"
    },
    "logement": {
        "parc_social": "28 %",
        "surpeuplement": "18 %"
    }
}

# ==========================================
# 4. HISTORIQUE & FINANCES (EXISTANT)
# ==========================================
HISTORY = {
    "annees_demo": [1968, 1982, 1990, 1999, 2009, 2014, 2020, 2022],
    "pop": [22094, 30075, 35049, 43174, 53290, 55090, 57150, 57546],
    "annees_secu": [2005, 2010, 2015, 2018, 2020, 2021, 2022, 2023],
    "faits_delinquance": [1850, 2100, 2300, 2150, 1900, 2050, 2200, 2180],
    "annees_fin": [2010, 2013, 2015, 2017, 2019, 2021, 2023],
    "dette": [1450, 1350, 1380, 1250, 1100, 1150, 1140]
}

# ==========================================
# 5. POLITIQUE RÉCENTE (EXISTANT)
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
    
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1", timeout=5)
        nb = r.json().get("total_results", 5000)
    except:
        nb = 5000
    
    KPI["entreprises"] = f"{nb:,}".replace(",", " ")

    output = {
        "meta": { "last_update": now },
        "kpi": KPI,
        "benchmark": BENCHMARK_MANDATS,
        "macro_elections": MACRO_ELECTIONS,
        "diagnostic": DIAGNOSTIC,
        "history": HISTORY,
        "politics": POLITICS,
        "finance": FISCALITE
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("OK: Données complètes (Benchmark inclus) générées.")

if __name__ == "__main__":
    main()
