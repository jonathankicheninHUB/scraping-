import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# ==========================================
# 1. DONNÉES POLITIQUES (Détail T1/T2 + Prés.)
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
# 2. DONNÉES HISTORIQUES (Démographie & Finances)
# ==========================================
HISTORY = {
    # Evolution population 1968-2022
    "annees_demo": [1968, 1982, 1999, 2011, 2022],
    "pop": [22094, 30075, 43174, 55090, 57546],
    
    # Evolution Dette 2013-2023
    "annees_fin": [2013, 2015, 2017, 2019, 2021, 2023],
    "dette": [1350, 1380, 1250, 1100, 1150, 1140]
}

# ==========================================
# 3. DONNÉES ACTUELLES (KPI & Fiscalité)
# ==========================================
KPI = {
    "pop": "57 546",
    "maire": "Joé BÉDIER",
    "parti": "DVG (Gauche)",
    "dette_hab": "1 140 €",
    "chomage": "29.2 %",
    "revenu": "14 500 €"
}

FISCALITE = {
    "foncier_bati": "38.50 %",
    "foncier_non_bati": "45.20 %",
    "habitation_sec": "22.50 %"
}

# ==========================================
# FONCTION PRINCIPALE
# ==========================================
def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Tentative API Sirene (Entreprises)
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1", timeout=5)
        nb = r.json().get("total_results", 5000)
    except:
        nb = 5000
    
    KPI["entreprises"] = f"{nb:,}".replace(",", " ")

    # Assemblage final du JSON
    output = {
        "meta": { "last_update": now },
        "kpi": KPI,
        "politics": POLITICS,
        "history": HISTORY,
        "finance": FISCALITE
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("OK: Fichier complet généré.")

if __name__ == "__main__":
    main()
