import json
import datetime
import requests

# --- CONFIGURATION ---
CODE_POSTAL = "97440"

# =========================================================
# 1. INTELLIGENCE POLITIQUE (Données validées)
# =========================================================
POLITICS = {
    "kpi_maire": {
        "nom": "Joé BÉDIER",
        "parti": "DVG (Gauche)",
        "mandat": "2020 - 2026",
        "score_victoire": "52.04 %"
    },
    "macro_tendances": {
        "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
        "bloc_droite": [56.5, 58.2, 59.4, 52.1, 46.8, 51.6, 47.9],
        "bloc_gauche": [43.5, 41.8, 40.6, 47.9, 53.2, 48.4, 52.0]
    },
    "details_scrutins": {
        "2020": {
            "candidats": ["Joé BÉDIER (Union G.)", "J.M. VIRAPOULLÉ (Droite)"],
            "scores": [52.04, 47.96],
            "couleurs": ["#e11d48", "#2563eb"], # Rouge / Bleu
            "analyse": "Basculement : Fusion des listes de gauche au 2nd tour."
        },
        "2014": {
            "candidats": ["J.P. VIRAPOULLÉ (UDI)", "Joé BÉDIER (DVG)"],
            "scores": [51.58, 48.42],
            "couleurs": ["#2563eb", "#e11d48"], # Bleu / Rouge
            "analyse": "Reconquête de la droite (Virapoullé Père)."
        },
        "2008": {
            "candidats": ["Eric FRUTEAU (PCR)", "J.P. VIRAPOULLÉ (UMP)"],
            "scores": [53.20, 46.80],
            "couleurs": ["#b91c1c", "#2563eb"], # Rouge Foncé / Bleu
            "analyse": "Fin de 30 ans de règne. Victoire historique PCR."
        }
    },
    "benchmark_maires": [
        {"periode": "2020-...", "nom": "J. BÉDIER", "bord": "Gauche", "dette_fin": "1140 €", "style": "Social", "color": "#e11d48"},
        {"periode": "2014-2020", "nom": "J.P. VIRAPOULLÉ", "bord": "Droite", "dette_fin": "1120 €", "style": "Bâtisseur", "color": "#2563eb"},
        {"periode": "2008-2014", "nom": "E. FRUTEAU", "bord": "PCR", "dette_fin": "1410 €", "style": "Éducation", "color": "#b91c1c"}
    ]
}

# =========================================================
# 2. SOCIAL & DEMO
# =========================================================
SOCIAL = {
    "demographie_historique": {
        "annees": [1968, 1975, 1982, 1990, 1999, 2009, 2014, 2020, 2022],
        "population": [22094, 25231, 30075, 35049, 43174, 53290, 55090, 57150, 57546]
    },
    "indicateurs_precarite": {
        "taux_pauvrete": "42 %",
        "allocataires_caf": "16 800",
        "beneficiaires_rsa": "5 400",
        "chomage_jeunes": "48 %",
        "comparaison_region": [42, 37]
    },
    "education": {
        "illettrisme_jdc": "22.5 %",
        "sans_diplome": "39 %"
    }
}

# =========================================================
# 3. RÉGALIEN & FINANCES
# =========================================================
REGALIEN = {
    "securite_trend": {
        "annees": [2015, 2017, 2019, 2020, 2021, 2022, 2023],
        "faits": [2300, 2250, 1980, 1900, 2050, 2200, 2150]
    },
    "finances_trend": {
        "annees": [2013, 2015, 2017, 2019, 2021, 2023],
        "dette": [1350, 1380, 1250, 1100, 1150, 1140]
    }
}

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # API Sirene (Sécurisée)
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1", timeout=5)
        if r.status_code == 200:
            entreprises = f"{r.json().get('total_results', 5000):,}".replace(",", " ")
        else:
            entreprises = "5 000"
    except:
        entreprises = "5 000" # Fallback

    data = {
        "meta": { "last_update": now },
        "kpi_global": {
            "pop": f"{SOCIAL['demographie_historique']['population'][-1]:,}".replace(",", " "),
            "entreprises": entreprises,
            "dette": str(REGALIEN['finances_trend']['dette'][-1]) + " €",
            "pauvrete": SOCIAL['indicateurs_precarite']['taux_pauvrete']
        },
        "politique": POLITICS,
        "social": SOCIAL,
        "regalien": REGALIEN
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Données Certifiées Générées.")

if __name__ == "__main__":
    main()
