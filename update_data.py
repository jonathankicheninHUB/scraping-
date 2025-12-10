import json
import datetime
import requests

# --- CONFIGURATION ---
CODE_POSTAL = "97440"

# =========================================================
# 1. INTELLIGENCE POLITIQUE (DONNÉES OFFICIELLES MIN. INTÉRIEUR)
# =========================================================
POLITICS = {
    "kpi_maire": {
        "nom": "Joé BÉDIER",
        "parti": "DVG (Gauche)",
        "mandat": "2020 - 2026",
        "score_victoire": "52.04 %"
    },
    # Évolution historique des blocs (Source: Archives Électorales)
    "macro_tendances": {
        "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
        # L'ère Virapoullé (D) vs PCR/Union (G)
        "bloc_droite": [56.5, 58.2, 59.4, 52.1, 46.8, 51.6, 47.9], 
        "bloc_gauche": [43.5, 41.8, 40.6, 47.9, 53.2, 48.4, 52.0]
    },
    # Résultats détaillés des scrutins clés
    "details_scrutins": {
        "2020": {
            "type": "Municipales 2020 (2nd Tour)",
            "candidats": ["Joé BÉDIER (Union G.)", "J.M. VIRAPOULLÉ (Droite)"],
            "scores": [52.04, 47.96],
            "couleurs": ["#e74c3c", "#3498db"],
            "analyse": "Basculement : Fusion des listes de gauche (Bédier + Fruteau)."
        },
        "2014": {
            "type": "Municipales 2014 (2nd Tour)",
            "candidats": ["J.P. VIRAPOULLÉ (UDI)", "Joé BÉDIER (DVG)"],
            "scores": [51.58, 48.42],
            "couleurs": ["#3498db", "#e74c3c"],
            "analyse": "Reconquête de la droite après la mandature Fruteau."
        },
        "2008": {
            "type": "Municipales 2008 (2nd Tour)",
            "candidats": ["Eric FRUTEAU (PCR)", "J.P. VIRAPOULLÉ (UMP)"],
            "scores": [53.20, 46.80],
            "couleurs": ["#c0392b", "#3498db"],
            "analyse": "Victoire historique du PCR, fin de 30 ans de règne."
        }
    },
    # Benchmark des gestionnaires
    "benchmark_maires": [
        {"periode": "2020-...", "nom": "J. BÉDIER", "bord": "Gauche", "dette_fin": "1140 € (Est.)", "style": "Social / Proximité", "color": "#e74c3c"},
        {"periode": "2014-2020", "nom": "J.P. VIRAPOULLÉ", "bord": "Droite", "dette_fin": "1120 €", "style": "Grands Travaux", "color": "#3498db"},
        {"periode": "2008-2014", "nom": "E. FRUTEAU", "bord": "PCR", "dette_fin": "1410 €", "style": "Éducation", "color": "#c0392b"}
    ]
}

# =========================================================
# 2. DIAGNOSTIC SOCIAL & DÉMO (SOURCES: INSEE, CAF)
# =========================================================
SOCIAL = {
    # Données RGP INSEE (Recensement Général Population)
    "demographie_historique": {
        "annees": [1968, 1975, 1982, 1990, 1999, 2009, 2014, 2020, 2022],
        "population": [22094, 25231, 30075, 35049, 43174, 53290, 55090, 57150, 57546]
    },
    "indicateurs_precarite": {
        "taux_pauvrete": "42 %",       # Source: INSEE (Moyenne Réunion ~37%)
        "allocataires_caf": "16 800",  # Source: CAF Open Data
        "beneficiaires_rsa": "5 400",  # Source: CD974
        "chomage_jeunes": "48 %",      # Source: Pôle Emploi (Cat A,B,C 15-24 ans)
        "comparaison_region": [42, 37] 
    },
    "education": {
        "illettrisme_jdc": "22.5 %",   # Source: JDC (Journée Défense Citoyenneté)
        "sans_diplome": "39 %"
    }
}

# =========================================================
# 3. RÉGALIEN & FINANCES (SOURCES: ONDRP, DGFIP)
# =========================================================
REGALIEN = {
    # Faits constatés (Police/Gendarmerie) - Tendance locale
    "securite_trend": {
        "annees": [2015, 2017, 2019, 2020, 2021, 2022, 2023],
        "faits": [2300, 2250, 1980, 1900, 2050, 2200, 2150]
    },
    # Dette par habitant (Comptes administratifs communaux)
    "finances_trend": {
        "annees": [2013, 2015, 2017, 2019, 2021, 2023],
        "dette": [1350, 1380, 1250, 1100, 1150, 1140]
    }
}

# =========================================================
# 4. ORCHESTRATEUR (LIVE SCRAPING SÉCURISÉ)
# =========================================================
def get_live_economy():
    """Tente de récupérer le nombre d'entreprises via l'API Sirene de l'État"""
    try:
        url = f"https://recherche-entreprises.api.
