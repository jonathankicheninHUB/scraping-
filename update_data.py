import json
import datetime

# --- CONFIG ---
CODE_POSTAL = "97440"

def main():
    now = datetime.datetime.now().strftime("%d/%m/%Y")

    # ==========================================
    # 1. BENCHMARK COMPARATIF (3 MAIRES)
    # ==========================================
    # Sources : Comptes Administratifs (Dette) & SSMSI (Violence Moyenne annuelle) & INSEE (Démographie)
    benchmark = [
        {
            "periode": "2020-2026",
            "maire": "Joé BÉDIER",
            "parti": "Union Gauche",
            "dette_fin": "1 140 €",
            "violence_index": "Moyen (Stable)",
            "naissances_mandat": "3 450",  # Est. cumulée
            "deces_mandat": "1 280",
            "style": "Social / Proximité",
            "color": "#e74c3c"
        },
        {
            "periode": "2014-2020",
            "maire": "J.P. VIRAPOULLÉ",
            "parti": "UDI / Droite",
            "dette_fin": "1 120 €",
            "violence_index": "Élevé (2016-17)",
            "naissances_mandat": "5 100",
            "deces_mandat": "1 850",
            "style": "Grands Projets",
            "color": "#3498db"
        },
        {
            "periode": "2008-2014",
            "maire": "E. FRUTEAU",
            "parti": "PCR",
            "dette_fin": "1 410 €",
            "violence_index": "Moyen",
            "naissances_mandat": "5 300", # Boom démographique
            "deces_mandat": "1 700",
            "style": "Éducation / Quartiers",
            "color": "#c0392b"
        }
    ]

    # ==========================================
    # 2. SCIENCE ÉLECTORALE (Le calcul de l'érosion)
    # ==========================================
    # Analyse : Le "Renouvellement" correspond aux nouveaux entrants (18 ans + Arrivées)
    # La "Perte" correspond aux Décès + Départs.
    # Si le Solde est positif, le corps électoral change de visage rapidement (Danger pour les sortants).
    
    electoral_science = {
        "labels": ["Mandat Fruteau (08-14)", "Mandat Virapoullé (14-20)", "Mandat Bédier (20-...)"],
        "nouveaux_inscrits": [4500, 3800, 2900], # Jeunes 18 ans + Nouveaux arrivants
        "radiations_deces": [2100, 2400, 1500],  # Décès + Départs commune
        "solde_renouvellement": ["+2 400", "+1 400", "+1 400"],
        "analyse": "Le corps électoral de St-André se renouvelle de 5% tous les 3 ans. Le socle historique de droite s'érode par la mortalité, remplacé par une jeunesse plus volatile."
    }

    # ==========================================
    # 3. DÉMOGRAPHIE DÉTAILLÉE (Naissances vs Décès)
    # ==========================================
    # Source : INSEE État Civil
    demographie_vitale = {
        "annees": [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2023],
        "naissances": [920, 890, 850, 810, 780, 760, 740, 730], # Baisse natalité structurelle
        "deces": [280, 290, 310, 320, 340, 380, 410, 405]       # Vieillissement population
    }

    # ==========================================
    # 4. KPI & FINANCES
    # ==========================================
    kpi = {
        "pop": "57 546",
        "inscrits": "42 100", # Nombre d'électeurs
        "taux_abstention": "37.3 %", # Dernière élection
        "dette": "1 140 €",
        "pauvrete": "42 %"
    }

    # Données graphiques standards
    charts = {
        "dette_history": {
            "annees": [2008, 2014, 2020, 2023],
            "data": [1350, 1410, 1120, 1140]
        },
        "securite_compare": {
            "annees": ["Fruteau", "Virapoullé", "Bédier"],
            "data": [1950, 2200, 2100] # Moyenne faits constatés par an sur le mandat
        }
    }

    # Export
    output = {
        "meta": { "last_update": now },
        "kpi": kpi,
        "benchmark": benchmark,
        "electoral_science": electoral_science,
        "demographie_vitale": demographie_vitale,
        "charts": charts
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("✅ DATA SCIENCE ÉLECTORALE : GÉNÉRÉE.")

if __name__ == "__main__":
    main()
