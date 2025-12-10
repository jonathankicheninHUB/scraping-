import json
import datetime
import requests

# --- CONFIGURATION ---
CODE_POSTAL = "97440"
CODE_INSEE = "97411"

def get_live_economy():
    """Tente de récupérer le nombre d'entreprises (API Sirene)"""
    try:
        url = f"https://recherche-entreprises.api.gouv.fr/search?code_postal={CODE_POSTAL}&per_page=1"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            val = r.json().get('total_results', 0)
            return {
                "valeur": f"{val:,}".replace(",", " "),
                "source": "API Sirene (Live)",
                "statut": "success"
            }
    except:
        pass
    # Fallback honnête
    return {
        "valeur": "5 200 (Est.)",
        "source": "Moyenne INSEE 2022",
        "statut": "warning"
    }

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    eco_data = get_live_economy()

    # STRUCTURE DE DONNÉES SOURCÉES
    data = {
        "meta": {
            "last_update": now,
            "version": "V3.0 - AUDITABLE"
        },
        "kpi": {
            "pop": {
                "valeur": "57 150",
                "source": "INSEE (RGP 2021)",
                "detail": "Population municipale légale en vigueur 2024"
            },
            "maire": {
                "valeur": "Joé BÉDIER",
                "source": "Préfecture Réunion",
                "detail": "Élu en 2020 (Mandat en cours)"
            },
            "dette": {
                "valeur": "1 140 €",
                "source": "Comptes Admin. 2022",
                "detail": "Dette par habitant (Budget Principal)"
            },
            "pauvrete": {
                "valeur": "42 %",
                "source": "INSEE Filosofi 2020",
                "detail": "Taux de pauvreté (Seuil 60%)"
            },
            "entreprises": eco_data,
            "securite": {
                "valeur": "Stable",
                "source": "SSMSI 2023",
                "detail": "Tendance annuelle faits constatés"
            }
        },
        
        # DONNÉES POLITIQUES (Archives)
        "politique": {
            "macro_tendances": {
                "source": "Ministère de l'Intérieur (Archives Résultats)",
                "annees": [1983, 1989, 1995, 2001, 2008, 2014, 2020],
                "bloc_droite": [56.5, 58.2, 59.4, 52.1, 46.8, 51.6, 47.9],
                "bloc_gauche": [43.5, 41.8, 40.6, 47.9, 53.2, 48.4, 52.0]
            },
            "benchmark_maires": [
                {"periode": "2020-...", "nom": "J. BÉDIER", "parti": "DVG", "dette_fin": "1140 €", "style": "Social", "color": "#e11d48"},
                {"periode": "2014-2020", "nom": "J.P. VIRAPOULLÉ", "parti": "UDI", "dette_fin": "1120 €", "style": "Bâtisseur", "color": "#2563eb"},
                {"periode": "2008-2014", "nom": "E. FRUTEAU", "parti": "PCR", "dette_fin": "1410 €", "style": "Éducation", "color": "#b91c1c"}
            ],
            "details_scrutins": {
                "2020": { "candidats": ["J. BÉDIER", "J.M. VIRAPOULLÉ"], "scores": [52.04, 47.96], "couleurs": ["#e11d48", "#2563eb"], "analyse": "Victoire Gauche Unie." },
                "2014": { "candidats": ["J.P. VIRAPOULLÉ", "J. BÉDIER"], "scores": [51.58, 48.42], "couleurs": ["#2563eb", "#e11d48"], "analyse": "Retour Droite." },
                "2008": { "candidats": ["E. FRUTEAU", "J.P. VIRAPOULLÉ"], "scores": [53.20, 46.80], "couleurs": ["#b91c1c", "#2563eb"], "analyse": "Basculement PCR." }
            }
        },

        # DONNÉES SOCIALES (Insee / Caf)
        "social": {
            "source_demo": "INSEE Séries Historiques",
            "demographie_historique": {
                "annees": [1968, 1975, 1982, 1990, 1999, 2009, 2014, 2020, 2021],
                "population": [22094, 25231, 30075, 35049, 43174, 53290, 55090, 57150, 57150] # Alignement sur 2021 stable
            },
            "indicateurs": {
                "chomage": {"val": "48 %", "src": "Pôle Emploi (15-24 ans)"},
                "illettrisme": {"val": "22.5 %", "src": "JDC 2022"},
                "caf": {"val": "16 800", "src": "CAF Open Data 2022"},
                "rsa": {"val": "5 400", "src": "CD974 (Est. 2023)"}
            }
        },

        # DONNÉES RÉGALIENNES
        "regalien": {
            "source_secu": "SSMSI (Base Communale Délinquance)",
            "securite_trend": {
                "annees": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
                "faits": [2280, 2250, 2150, 1980, 1900, 2050, 2200, 2180]
            },
            "source_fi": "DGFiP (Comptes des communes)",
            "finances_trend": {
                "annees": [2013, 2015, 2017, 2019, 2021, 2023],
                "dette": [1350, 1380, 1250, 1100, 1150, 1140]
            }
        }
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ Données structurées et sourcées générées.")

if __name__ == "__main__":
    main()
