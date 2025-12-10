import json
import datetime
import requests

# --- CONFIG ---
CODE_POSTAL = "97440"

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # 1. KPI PRINCIPAUX
    kpi = {
        "pop": "57 546",
        "maire": "Joé BÉDIER",
        "parti": "Union Gauche",
        "dette": "1 140 €",
        "pauvrete": "42 %",
        "entreprises": "5 000+"
    }

    # 2. BENCHMARK MAIRES (Tableau)
    benchmark = [
        {"periode": "2020-...", "maire": "J. BÉDIER", "parti": "DVG", "dette": "1140 €", "style": "Social", "color": "#e74c3c"},
        {"periode": "2014-2020", "maire": "J.P. VIRAPOULLÉ", "parti": "UDI", "dette": "1120 €", "style": "Bâtisseur", "color": "#3498db"},
        {"periode": "2008-2014", "maire": "E. FRUTEAU", "parti": "PCR", "dette": "1410 €", "style": "Éducation", "color": "#c0392b"}
    ]

    # 3. DONNÉES SOCIALES (Texte)
    social = {
        "chomage": "48 %",
        "illettrisme": "22 %",
        "caf": "16 800",
        "rsa": "5 400"
    }

    # 4. DONNÉES GRAPHIQUES (Arrays simples pour ChartJS)
    charts = {
        # Politique : Évolution des Blocs (1983-2020)
        "politique_macro": {
            "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
            "droite": [56.5, 58.2, 59.4, 52.1, 46.8, 51.6, 47.9],
            "gauche": [43.5, 41.8, 40.6, 47.9, 53.2, 48.4, 52.0]
        },
        # Sécurité : Faits constatés
        "securite": {
            "annees": [2015, 2017, 2019, 2020, 2021, 2022, 2023],
            "data": [2300, 2250, 1980, 1900, 2050, 2200, 2180]
        },
        # Histoire : Population
        "demographie": {
            "annees": [1968, 1982, 1999, 2010, 2015, 2022],
            "data": [22094, 30075, 43174, 53290, 56000, 57546]
        },
        # Finances : Dette
        "dette": {
            "annees": [2013, 2015, 2017, 2019, 2021, 2023],
            "data": [1350, 1380, 1250, 1100, 1150, 1140]
        },
        # Détails Élections (Pour le sélecteur)
        "elections": {
            "2020": { "labels": ["J. BÉDIER", "J.M. VIRAPOULLÉ"], "data": [52.04, 47.96], "colors": ["#e74c3c", "#3498db"], "analyse": "Victoire de la Gauche unie." },
            "2014": { "labels": ["J.P. VIRAPOULLÉ", "J. BÉDIER"], "data": [51.58, 48.42], "colors": ["#3498db", "#e74c3c"], "analyse": "Retour de la Droite." },
            "2008": { "labels": ["E. FRUTEAU", "J.P. VIRAPOULLÉ"], "data": [53.20, 46.80], "colors": ["#c0392b", "#3498db"], "analyse": "Basculement historique PCR." }
        }
    }

    # Structure Finale
    output = {
        "meta": { "last_update": now },
        "kpi": kpi,
        "benchmark": benchmark,
        "social": social,
        "charts": charts
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("✅ data.json généré (Structure Synchronisée).")

if __name__ == "__main__":
    main()
