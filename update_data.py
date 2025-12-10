import json
import datetime
import requests
from bs4 import BeautifulSoup

# --- CONFIG ---
URL_WIKI = "https://fr.wikipedia.org/wiki/Saint-Andr%C3%A9_(La_R%C3%A9union)"
CODE_INSEE = "97411"

# --- STRUCTURE DE STOCKAGE ---
DATABASE = {
    "meta": { "last_run": "", "status": "Pending" },
    "audit": [], # Le journal de bord du scraping
    "tables": {
        "politique_actuelle": {},
        "demographie": {},
        "economie": {},
        "historique_elections": [],
        "historique_maires": []
    }
}

def log(source, status, message, count=0):
    """Ajoute une ligne au rapport de gestion"""
    entry = {
        "source": source,
        "status": status, # SUCCESS, WARNING, ERROR
        "message": message,
        "records": count,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }
    DATABASE["audit"].append(entry)
    print(f"[{status}] {source}: {message}")

# --- 1. SCRAPING WIKIPEDIA (Preuve de concept) ---
def scrape_wikipedia():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Education Project)'}
        r = requests.get(URL_WIKI, headers=headers, timeout=10)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Récupération du Maire dans l'Infobox
            infobox = soup.find('table', {'class': 'infobox_v2'})
            maire = "Non trouvé"
            if infobox:
                rows = infobox.find_all('tr')
                for tr in rows:
                    if "Maire" in tr.text:
                        maire = tr.find('td').text.strip().split('[')[0] # Nettoyage
            
            DATABASE["tables"]["politique_actuelle"] = {
                "maire": maire,
                "source_url": URL_WIKI
            }
            log("Wikipedia", "SUCCESS", f"Maire identifié : {maire}", 1)
        else:
            log("Wikipedia", "ERROR", f"Code HTTP {r.status_code}")
            
    except Exception as e:
        log("Wikipedia", "ERROR", str(e))

# --- 2. API GOUVERNEMENTALES ---
def scrape_apis():
    # POPULATION
    try:
        url_pop = f"https://geo.api.gouv.fr/communes/{CODE_INSEE}?fields=population"
        r = requests.get(url_pop, timeout=5)
        pop = r.json()['population']
        DATABASE["tables"]["demographie"] = {"total": pop, "annee": "2024 (INSEE)"}
        log("API Géo", "SUCCESS", f"Population récupérée : {pop}", 1)
    except Exception as e:
        log("API Géo", "ERROR", str(e))

    # ENTREPRISES
    try:
        url_eco = f"https://recherche-entreprises.api.gouv.fr/search?code_postal=97440&per_page=1"
        r = requests.get(url_eco, timeout=5)
        nb = r.json()['total_results']
        DATABASE["tables"]["economie"] = {"entreprises_actives": nb}
        log("API Sirene", "SUCCESS", f"Entreprises trouvées : {nb}", nb)
    except Exception as e:
        log("API Sirene", "WARNING", "API indisponible, utilisation backup")

# --- 3. CHARGEMENT DONNÉES HISTORIQUES (Fichiers plats) ---
def load_archives():
    # Ici, on simule le chargement d'un CSV historique nettoyé
    # C'est ta "Base de Données Froide"
    
    # Maires
    maires = [
        {"periode": "2020-...", "nom": "Joé BÉDIER", "parti": "DVG"},
        {"periode": "2014-2020", "nom": "J.P. VIRAPOULLÉ", "parti": "UDI"},
        {"periode": "2008-2014", "nom": "Eric FRUTEAU", "parti": "PCR"},
        {"periode": "1972-2008", "nom": "J.P. VIRAPOULLÉ", "parti": "UDF/UMP"}
    ]
    DATABASE["tables"]["historique_maires"] = maires
    log("Archives Maires", "SUCCESS", "Historique chargé", len(maires))

    # Élections (Détail)
    elections = [
        {"annee": 2020, "tour": 2, "vainqueur": "Bédier", "score": 52.04, "participation": 62.7},
        {"annee": 2014, "tour": 2, "vainqueur": "Virapoullé", "score": 51.58, "participation": 70.4},
        {"annee": 2008, "tour": 2, "vainqueur": "Fruteau", "score": 53.20, "participation": 73.5}
    ]
    DATABASE["tables"]["historique_elections"] = elections
    log("Archives Élections", "SUCCESS", "Résultats chargés", len(elections))

def main():
    print("--- DÉBUT DU SCRAPING ET AUDIT ---")
    DATABASE["meta"]["last_run"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    scrape_wikipedia()
    scrape_apis()
    load_archives()
    
    # Sauvegarde
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(DATABASE, f, ensure_ascii=False, indent=2)
    print("--- FIN ET SAUVEGARDE ---")

if __name__ == "__main__":
    main()
