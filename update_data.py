import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

# --- DONNÉES EN DUR (HISTORIQUE & ACTUEL) ---
DATA = {
    "meta": {},
    "kpi": {
        "pop": "57 546",
        "maire": "Joé BÉDIER",
        "dette": "1 140 €",
        "impot": "38.5 %"
    },
    "history": {
        "annees_demo": [1968, 1982, 1999, 2011, 2022],
        "pop": [22094, 30075, 43174, 55090, 57546],
        
        "annees_finance": [2015, 2017, 2019, 2021, 2023],
        "dette": [1380, 1250, 1100, 1150, 1140],
        
        "annees_chomage": [2010, 2015, 2020, 2023],
        "chomage": [35.0, 31.8, 31.0, 28.8]
    },
    "elections": {
        "2020": {
            "labels": ["J. BÉDIER", "J.M. VIRAPOULLÉ"],
            "data": [52.04, 47.96],
            "sieges": [30, 9]
        },
        "2014": {
            "labels": ["J.P. VIRAPOULLÉ", "J. BÉDIER"],
            "data": [51.58, 48.42],
            "sieges": [31, 8]
        }
    },
    "elus": [
        {"nom": "BÉDIER Joé", "fonction": "Maire", "groupe": "Majorité"},
        {"nom": "VIRAPOULLÉ J.M", "fonction": "Opposant", "groupe": "Opposition"},
        {"nom": "PAYET Marie", "fonction": "1ère Adj.", "groupe": "Majorité"}
    ]
}

def main():
    # Mise à jour date
    DATA["meta"]["last_update"] = datetime.
