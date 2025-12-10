import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# ==========================================
# 1. BENCHMARK DES MAIRES (1972 - 2024)
# ==========================================
BENCHMARK = [
    {
        "periode": "2020 - ...",
        "maire": "Joé BÉDIER",
        "parti": "Union Gauche",
        "dette_fin": "1 140 €",
        "pop_evo": "+1.2%",
        "style": "Social / Proximité",
        "color": "#e74c3c"
    },
    {
        "periode": "2014 - 2020",
        "maire": "J-Paul VIRAPOULLÉ",
        "parti": "UDI (Droite)",
        "dette_fin": "1 120 €",
        "pop_evo": "+0.5%",
        "style": "Grands Projets (Colosse)",
        "color": "#3498db"
    },
    {
        "periode": "2008 - 2014",
        "maire": "Eric FRUTEAU",
        "parti": "PCR",
        "dette_fin": "1 410 €",
        "pop_evo": "+1.8%",
        "style": "Structuration / École",
        "color": "#c0392b"
    }
]

# ==========================================
# 2. HISTORIQUE & SÉCURITÉ
# ==========================================
HISTORY = {
    # Démographie (1968-2022)
    "annees_demo": [1968, 1982, 1999, 2010, 2015, 2022],
    "pop": [22094, 30075, 43174, 53290, 56000, 57546],

    # Sécurité (Faits constatés 2015-2023)
    "annees_secu": [2015, 2017, 2019, 2020, 2021, 2022, 2023],
    "faits": [2300, 2250, 1980, 1900, 2050, 2200, 2180],
    
    # Finances (Dette)
    "annees_fin": [2013, 2015, 2017, 2019, 2021, 2023],
    "dette": [1350, 1380, 1250, 1100, 1150, 1140]
}

# ==========================================
# 3. DIAGNOSTIC SOCIAL & POLITIQUE
# ==========================================
DIAGNOSTIC = {
    "social": {
        "pauvrete": "42 %",
        "chomage_jeunes": "48 %",
        "rsa": "5 200",
        "illettrisme": "22 %"
    },
    "politique": {
        "maire_actuel": "Joé BÉDIER",
        "tendance": "Majorité (DVG)",
        "score_2020": "52.04 %"
    }
}

KPI = {
    "pop": "57 546",
    "entreprises": "5 000+", # Sera mis à jour par l'API
    "dette": "1 140 €",
    "pauvrete": "42 %"
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
        "benchmark": BENCHMARK,
        "history": HISTORY,
        "diagnostic": DIAGNOSTIC
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("OK: Données FUSIONNÉES générées.")

if __name__ == "__main__":
    main()
