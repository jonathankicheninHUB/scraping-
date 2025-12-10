import json
import datetime
import requests
import sys
import os

# Fonction pour afficher les logs en temps réel dans GitHub
def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

log("🚀 DÉMARRAGE DU SCRIPT D'AUDIT...")

# Structure de base (au cas où tout plante)
DATA = {
    "meta": {
        "status": "INITIALIZING",
        "last_run": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    },
    "audit_logs": []
}

def add_audit(source, status, details):
    DATA["audit_logs"].append({
        "source": source,
        "status": status,
        "details": details
    })
    log(f" > {source}: {status} - {details}")

# --- TEST 1 : CONNEXION INTERNET SIMPLE ---
log("1. Test de connexion Internet (Google)...")
try:
    requests.get("https://www.google.com", timeout=5)
    add_audit("Internet", "OK", "Connexion sortante fonctionnelle")
except Exception as e:
    add_audit("Internet", "FAIL", str(e))

# --- TEST 2 : SCRAPING WIKIPEDIA ---
log("2. Tentative Scraping Wikipédia (Saint-André)...")
try:
    from bs4 import BeautifulSoup
    url = "https://fr.wikipedia.org/wiki/Saint-Andr%C3%A9_(La_R%C3%A9union)"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        page_title = soup.title.string
        add_audit("Wikipedia", "OK", f"Page trouvée : {page_title}")
        
        # Tentative d'extraction du maire
        infobox = soup.find('table', {'class': 'infobox_v2'})
        if infobox:
            DATA["wikipedia_raw"] = "Infobox trouvée"
        else:
            DATA["wikipedia_raw"] = "Infobox NON trouvée (Structure HTML a changé ?)"
    else:
        add_audit("Wikipedia", "FAIL", f"Status Code: {r.status_code}")

except Exception as e:
    add_audit("Wikipedia", "CRASH", str(e))

# --- TEST 3 : API GOUV (Population) ---
log("3. Test API Géo (Population)...")
try:
    r = requests.get("https://geo.api.gouv.fr/communes/97411?fields=population", timeout=5)
    if r.status_code == 200:
        pop = r.json().get('population', 'Inconnu')
        add_audit("API Géo", "OK", f"Population récupérée : {pop}")
        DATA["population_live"] = pop
    else:
        add_audit("API Géo", "FAIL", f"Erreur {r.status_code}")
except Exception as e:
    add_audit("API Géo", "CRASH", str(e))

# --- SAUVEGARDE FINALE ---
log("4. Sauvegarde du fichier data.json...")
try:
    # On force le statut final
    DATA["meta"]["status"] = "COMPLETED"
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(DATA, f, ensure_ascii=False, indent=2)
    
    # Vérification que le fichier existe
    if os.path.exists("data.json"):
        size = os.path.getsize("data.json")
        log(f"✅ SUCCÈS : Fichier créé ({size} octets).")
    else:
        log("❌ ERREUR MAJEURE : Le fichier n'est pas sur le disque après écriture.")
        sys.exit(1) # Force l'échec de l'action GitHub

except Exception as e:
    log(f"❌ CRASH ÉCRITURE : {e}")
    sys.exit(1)
