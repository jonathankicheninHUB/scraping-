import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# =========================================================
# 1. VISION MACRO-POLITIQUE (1983 - 2020)
# =========================================================
# Permet de tracer la courbe de force Gauche/Droite sur 40 ans
MACRO_POLITIQUE = {
    "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
    "bloc_droite": [56.5, 58.2, 59.4, 54.8, 46.8, 51.6, 47.9], # J.P Virapoullé / J.M Virapoullé
    "bloc_gauche": [43.5, 41.8, 40.6, 45.2, 53.2, 48.4, 52.0], # PCR / Fruteau / Bédier
    "participation": [78.0, 76.5, 74.2, 72.8, 73.5, 70.4, 62.7] # L'abstention monte
}

# =========================================================
# 2. DÉTAIL DES ÉLECTIONS CLÉS (Pour le sélecteur)
# =========================================================
POLITICS_DETAILS = {
    "2020": {
        "titre": "Municipales 2020 (Victoire J. Bédier)",
        "candidats": ["Joé BÉDIER (Union Gauche)", "J.M. VIRAPOULLÉ (Droite)"],
        "scores": [52.04, 47.96],
        "couleurs": ["#dc3545", "#0d6efd"]
    },
    "2014": {
        "titre": "Municipales 2014 (Retour J.P. Virapoullé)",
        "candidats": ["J.P. VIRAPOULLÉ (UDI)", "Joé BÉDIER (DVG)"],
        "scores": [51.58, 48.42],
        "couleurs": ["#0d6efd", "#dc3545"]
    },
    "2008": {
        "titre": "Municipales 2008 (Victoire E. Fruteau)",
        "candidats": ["Eric FRUTEAU (PCR)", "J.P. VIRAPOULLÉ (UMP)"],
        "scores": [53.20, 46.80],
        "couleurs": ["#b30000", "#0d6efd"] # Rouge foncé pour PCR
    }
}

# =========================================================
# 3. BENCHMARK DES MAIRES (Comparatif Mandats)
# =========================================================
BENCHMARK = [
    {
        "periode": "2020 - ...",
        "maire": "Joé BÉDIER",
        "parti": "DVG",
        "dette_fin": "1 140 €",
        "pop_evo": "+1.2%",
        "style": "Proximité / Social",
        "color": "#e74c3c"
    },
    {
        "periode": "2014 - 2020",
        "maire": "J-Paul VIRAPOULLÉ",
        "parti": "UDI",
        "dette_fin": "1 120 €",
        "pop_evo": "+0.5%",
        "style": "Grands Projets",
        "color": "#3498db"
    },
    {
        "periode": "2008 - 2014",
        "maire": "Eric FRUTEAU",
        "parti": "PCR",
        "dette_fin": "1 410 €",
        "pop_evo": "+1.8%",
        "style": "Education / Quartiers",
        "color": "#c0392b"
    },
    {
        "periode": "1972 - 2008",
        "maire": "J-Paul VIRAPOULLÉ",
        "parti": "UDF/UMP",
        "dette_fin": "Variable",
        "pop_evo": "+3.5% (Boom)",
        "style": "Transformation Ville",
        "color": "#2980b9"
    }
]

# =========================================================
# 4. DONNÉES CONTEXTUELLES (Social, Sécu, Histoire)
# =========================================================
# On garde tout ce qu'on avait déjà
HISTORY = {
    "annees_demo": [1968, 1982, 1999, 2010, 2015, 2022],
    "pop": [22094, 30075, 43174, 53290, 56000, 57546],
    "annees_secu": [2015, 2017, 2019, 2020, 2021, 2022, 2023],
    "faits_delinquance": [2300, 2250, 1980, 1900, 2050, 2200, 2180],
    "annees_fin": [2013, 2015, 2017, 2019, 2021, 2023],
    "dette": [1350, 1380, 1250, 1100, 1150, 1140]
}

DIAGNOSTIC = {
    "social": {
        "pauvrete": "42 %",
        "chomage_jeunes": "48 %",
        "allocataires_caf": "16 500",
        "beneficiaires_rsa": "5 200",
        "illettrisme": "22 %"
    }
}

KPI = {
    "pop": "57 546",
    "maire": "Joé BÉDIER",
    "parti": "Union Gauche",
    "dette_hab": "1 140 €",
    "pauvrete": "42 %",
    "entreprises": "5 000"
}

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # API Sirene
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1", timeout=5)
        nb = r.json().get("total_results", 5000)
        KPI["entreprises"] = f"{nb:,}".replace(",", " ")
    except:
        KPI["entreprises"] = "5 000"

    output = {
        "meta": { "last_update": now },
        "kpi": KPI,
        "macro_politique": MACRO_POLITIQUE, # La nouvelle courbe 40 ans
        "politics_details": POLITICS_DETAILS, # Le détail par élection
        "benchmark": BENCHMARK,
        "history": HISTORY,
        "diagnostic": DIAGNOSTIC
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("OK: Données Historiques Complètes générées.")

if __name__ == "__main__":
    main()
