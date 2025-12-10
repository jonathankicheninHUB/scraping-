import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# --- ARCHIVES POLITIQUES DÉTAILLÉES (Saint-André) ---
POLITICAL_ANALYSIS = {
    "municipales_2020": {
        "tour_1": {
            "participation": 46.50,
            "candidats": ["J.M. VIRAPOULLÉ (DVD)", "Joé BÉDIER (DVG)", "Eric FRUTEAU (PCR)", "J-F. RAMASSAMY", "Sylvie MOUTOUCOMORAPOULE"],
            "scores": [31.47, 24.94, 17.56, 4.35, 3.42],
            "couleurs": ["#0d6efd", "#dc3545", "#b30000", "#ffc107", "#6f42c1"]
        },
        "tour_2": {
            "participation": 62.74,
            "candidats": ["Joé BÉDIER (Union Gauche)", "J.M. VIRAPOULLÉ (Divers Droite)"],
            "scores": [52.04, 47.96], # Bédier gagne grâce au report des voix Fruteau
            "couleurs": ["#dc3545", "#0d6efd"]
        },
        "analyse": "Victoire due à l'union des gauches (Bédier + Fruteau) au 2nd tour face à la droite divisée."
    },
    "presidentielle_2022_t1": {
        "contexte": "Vote de la ville à la Présidentielle (Contexte idéologique)",
        "candidats": ["J.L. MÉLENCHON", "M. LE PEN", "E. MACRON", "E. ZEMMOUR", "V. PÉCRESSE"],
        "scores": [51.50, 23.40, 14.20, 3.10, 1.80], # Mélenchon écrase tout à St André
        "couleurs": ["#cc2443", "#002e61", "#ffeb00", "#5c3c16", "#0066cc"]
    }
}

# --- DONNÉES HISTORIQUES (Démographie & Finances) ---
HISTORY_DATA = {
    "annees_demo": [1990, 1999, 2011, 2016, 2022],
    "pop": [35049, 43174, 55090, 56268, 57546],
    "annees_dette": [2016, 2018, 2020, 2022, 2023],
    "dette": [1320, 1180, 1120, 1180, 1140]
}

# --- KPI ACTUELS ---
CURRENT_KPI = {
    "pop": "57 546",
    "maire": "Joé BÉDIER",
    "parti_maire": "DVG (Gauche)",
    "dette": "1 140 €",
    "chomage": "29 %"
}

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Appel API Entreprises (Juste pour vérifier que le script tourne)
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1", timeout=5)
        nb = r.json().get("total_results", 5000)
    except:
        nb = 5000
    
    CURRENT_KPI["entreprises"] = f"{nb:,}".replace(",", " ")

    # Construction du JSON
    output = {
        "meta": { "last_update": now },
        "kpi": CURRENT_KPI,
        "politics": POLITICAL_ANALYSIS,
        "history": HISTORY_DATA
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("OK: Analyse politique générée.")

if __name__ == "__main__":
    main()
