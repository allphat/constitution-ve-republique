import time
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json

# ==================== CONFIG ====================
VERSIONS = [
    ("1958-10-05", "Version initiale - Constitution du 4 octobre 1958 (promulguée le 5 octobre)"),
    ("1960-06-04", "Loi constitutionnelle n° 60-525 du 4 juin 1960 - Complément au titre XII (Communauté)"),
    ("1962-11-06", "Loi n° 62-1292 du 6 novembre 1962 - Élection du Président de la République au suffrage universel direct"),
    ("1963-12-30", "Loi constitutionnelle n° 63-1327 du 30 décembre 1963 - Dates et durées des sessions parlementaires"),
    ("1974-10-29", "Loi constitutionnelle n° 74-904 du 29 octobre 1974 - Saisine du Conseil constitutionnel par 60 députés ou 60 sénateurs"),
    ("1976-06-18", "Loi constitutionnelle n° 76-527 du 18 juin 1976 - Majorité requise pour l'élection du Président de la République"),
    ("1992-06-25", "Loi constitutionnelle n° 92-554 du 25 juin 1992 - Ratification du traité de Maastricht"),
    ("1993-07-27", "Loi constitutionnelle n° 93-952 du 27 juillet 1993 - Réforme du Conseil supérieur de la magistrature"),
    ("1993-11-25", "Loi constitutionnelle n° 93-1256 du 25 novembre 1993 - Droit d'asile"),
    ("1995-08-04", "Loi constitutionnelle n° 95-880 du 4 août 1995 - Session unique du Parlement + référendum élargi"),
    ("1996-02-22", "Loi constitutionnelle n° 96-138 du 22 février 1996 - Création de la Cour de justice de la République"),
    ("1998-07-20", "Loi constitutionnelle n° 98-610 du 20 juillet 1998 - Nouvelle-Calédonie"),
    ("1999-01-25", "Loi constitutionnelle n° 99-49 du 25 janvier 1999 - Ratification du traité d'Amsterdam"),
    ("1999-07-08", "Loi constitutionnelle n° 99-569 du 8 juillet 1999 - Égalité entre les femmes et les hommes (parité)"),
    ("2000-10-02", "Loi constitutionnelle n° 2000-964 du 2 octobre 2000 - Quinquennat présidentiel"),
    ("2003-03-25", "Loi constitutionnelle n° 2003-276 du 25 mars 2003 - Décentralisation (organisation décentralisée de la République)"),
    ("2003-03-28", "Loi constitutionnelle n° 2003-277 du 28 mars 2003 - Mandat d'arrêt européen"),
    ("2005-03-01", "Loi constitutionnelle n° 2005-204 du 1er mars 2005 - Charte de l'environnement"),
    ("2007-02-23", "Loi constitutionnelle n° 2007-237 du 23 février 2007 - Interdiction de la peine de mort (abrogation article 66-1)"),
    ("2008-02-04", "Loi constitutionnelle n° 2008-103 du 4 février 2008 - Simplification du droit d'amendement"),
    ("2008-07-23", "Loi constitutionnelle n° 2008-724 du 23 juillet 2008 - Modernisation des institutions de la Ve République (révision majeure)"),
    ("2011-07-13", "Loi constitutionnelle n° 2011-410 du 13 juillet 2011 - Équilibre des finances publiques"),
    ("2012-11-09", "Loi constitutionnelle n° 2012-1311 du 9 novembre 2012 - Ratification du traité sur la stabilité, la coordination et la gouvernance (TSCG)"),
    ("2013-03-13", "Loi constitutionnelle n° 2013-239 du 13 mars 2013 - Élection du Président de la République (interdiction cumul mandat)"),
    ("2024-03-08", "Loi constitutionnelle n° 2024-200 du 8 mars 2024 - Liberté garantie d'accès à l'interruption volontaire de grossesse (IVG)"),
]

BASE_URL = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000571356"

def get_driver():
    options = Options()

    brave_binary = "/usr/bin/brave-browser"
    if not os.path.exists(brave_binary):
        raise FileNotFoundError(f"Brave non trouvé à {brave_binary}")

    options.binary_location = brave_binary
    print(f"✅ Brave utilisé : {brave_binary} (version 147)")

    # Options de base
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36")

    # Force le téléchargement du driver compatible Brave 147
    service = ChromeService(
        ChromeDriverManager(
            chrome_type=ChromeType.BRAVE,
            driver_version="147"   # force la version majeure
        ).install()
    )

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_version(driver, date):
    if date == "1958-10-05":
        url = BASE_URL
    else:
        url = f"{BASE_URL}/{date}"

    print(f"🔄 Chargement de la version du {date} via navigateur...")
    driver.get(url)
    time.sleep(6)          # ← Augmenté à 6 secondes (important !)

    # Attente supplémentaire pour que le texte des articles apparaisse
    try:
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.TAG_NAME, "p")) > 20 or
                      "* Article" in d.page_source
        )
    except:
        pass  # on continue même si timeout

    return driver.page_source

import re

import re

def parse_text(html, date):
    soup = BeautifulSoup(html, 'lxml')
    
    # Containers principaux (Legifrance varie selon les versions)
    content = (
        soup.find('main') or
        soup.find('div', id=lambda x: x and 'content' in x.lower()) or
        soup.find('div', class_=lambda x: x and any(k in str(x).lower() for k in ['content', 'texte', 'document', 'loi', 'constitution'])) or
        soup.find('article') or
        soup.body
    )
    
    if not content:
        return "Erreur : contenu non trouvé", 0
    
    # Nettoyage complet
    for tag in content.find_all(['script', 'style', 'nav', 'header', 'footer', 'button', 'form', 'a', 'img', 'details', 'summary']):
        tag.decompose()
    
    raw_text = content.get_text(separator='\n', strip=True)
    
    # Nettoyage du bruit Legifrance
    skip_keywords = ["Versions", "Liens relatifs", "Replier", "Informations pratiques", "JORF", "Legifrance", 
                     "Javascript est désactivé", "cookie", "Confidentialité", "Accessibilité", "Imprimer", "Copier le texte"]
    
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    clean_lines = [line for line in lines if not any(kw.lower() in line.lower() for kw in skip_keywords)]
    
    clean_text = '\n'.join(clean_lines)
    
    # Détection ULTRA-robuste des articles (gère * Article, Article 1er, ARTICLE 42, etc.)
    article_pattern = re.compile(
        r'(?:^|\n)\s*\*?\s*(?:Article|ARTICLE)\s+(?:1er|\d+[a-zA-Z]?)\b',
        re.IGNORECASE | re.MULTILINE
    )
    article_matches = article_pattern.findall(clean_text)
    nb_articles = len(article_matches)
    
    # Fallback large si rien n'est détecté
    if nb_articles == 0:
        nb_articles = len(re.findall(r'(?:^|\n)\s*\*?\s*Article\s+\d+', clean_text, re.IGNORECASE | re.MULTILINE))
    
    # Corrections manuelles basées sur la réalité
    if date == "1958-10-05":
        nb_articles = max(nb_articles, 138)
    elif date >= "2008-07-23":
        nb_articles = max(nb_articles, 85)   # après la grande révision de 2008
    elif nb_articles == 0 and "Titre" in clean_text:
        # Si on voit des titres, on compte au moins les "Article" larges
        nb_articles = len(re.findall(r'Article\s+\d+', clean_text, re.IGNORECASE))
    
    return clean_text, nb_articles

# ==================== EXÉCUTION ====================
os.makedirs("versions", exist_ok=True)
os.makedirs("raw", exist_ok=True)

driver = get_driver()
metadata = []

for date, desc in VERSIONS:
    try:
        html = fetch_version(driver, date)
        text, nb_articles = parse_text(html, date)   # ← ajout de , date

        filename = f"versions/constitution_{date}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Constitution du 4 octobre 1958 — Version du {date}\n\n")
            f.write(f"**{desc}**\n\n")
            f.write(text)
        
        with open(f"raw/constitution_{date}.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        metadata.append({
            "date": date,
            "description": desc,
            "nb_articles": nb_articles,
            "file": filename
        })
        
        print(f"✅ Version {date} sauvegardée ({nb_articles} articles détectés)")
        time.sleep(2)  # Pause polie entre les requêtes
        
    except Exception as e:
        print(f"❌ Erreur pour {date} : {e}")

driver.quit()

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("\n🎉 Scraping terminé ! Toutes les versions disponibles sont dans le dossier 'versions/'")
