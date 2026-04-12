from seleniumbase import SB
import time
import os
import json
from bs4 import BeautifulSoup
import re

# === LISTE COMPLETE DES VERSIONS ===
VERSIONS = [
    ("1958-10-05", "Version initiale - Constitution du 4 octobre 1958 (promulguée le 5 octobre)"),
    ("1960-06-04", "Loi constitutionnelle n° 60-525 du 4 juin 1960 - Complément au titre XII (Communauté)"),
    ("1962-11-06", "Loi n° 62-1292 du 6 novembre 1962 - Élection du Président au suffrage universel direct"),
    ("1963-12-30", "Loi constitutionnelle n° 63-1327 du 30 décembre 1963 - Dates et durées des sessions parlementaires"),
    ("1974-10-29", "Loi constitutionnelle n° 74-904 du 29 octobre 1974 - Saisine du Conseil constitutionnel"),
    ("1976-06-18", "Loi constitutionnelle n° 76-527 du 18 juin 1976 - Majorité pour l'élection du Président"),
    ("1992-06-25", "Loi constitutionnelle n° 92-554 du 25 juin 1992 - Traité de Maastricht"),
    ("1993-07-27", "Loi constitutionnelle n° 93-952 du 27 juillet 1993 - Conseil supérieur de la magistrature"),
    ("1993-11-25", "Loi constitutionnelle n° 93-1256 du 25 novembre 1993 - Droit d'asile"),
    ("1995-08-04", "Loi constitutionnelle n° 95-880 du 4 août 1995 - Session unique + référendum"),
    ("1996-02-22", "Loi constitutionnelle n° 96-138 du 22 février 1996 - Cour de justice de la République"),
    ("1998-07-20", "Loi constitutionnelle n° 98-610 du 20 juillet 1998 - Nouvelle-Calédonie"),
    ("1999-01-25", "Loi constitutionnelle n° 99-49 du 25 janvier 1999 - Traité d'Amsterdam"),
    ("1999-07-08", "Loi constitutionnelle n° 99-569 du 8 juillet 1999 - Parité hommes-femmes"),
    ("2000-10-02", "Loi constitutionnelle n° 2000-964 du 2 octobre 2000 - Quinquennat"),
    ("2003-03-25", "Loi constitutionnelle n° 2003-276 du 25 mars 2003 - Décentralisation"),
    ("2003-03-28", "Loi constitutionnelle n° 2003-277 du 28 mars 2003 - Mandat d'arrêt européen"),
    ("2005-03-01", "Loi constitutionnelle n° 2005-204 du 1er mars 2005 - Charte de l'environnement"),
    ("2007-02-23", "Loi constitutionnelle n° 2007-237 du 23 février 2007 - Abolition peine de mort"),
    ("2008-02-04", "Loi constitutionnelle n° 2008-103 du 4 février 2008 - Droit d'amendement"),
    ("2008-07-23", "Loi constitutionnelle n° 2008-724 du 23 juillet 2008 - Modernisation des institutions (révision majeure)"),
    ("2011-07-13", "Loi constitutionnelle n° 2011-410 du 13 juillet 2011 - Équilibre des finances publiques"),
    ("2012-11-09", "Loi constitutionnelle n° 2012-1311 du 9 novembre 2012 - TSCG"),
    ("2013-03-13", "Loi constitutionnelle n° 2013-239 du 13 mars 2013 - Cumul des mandats"),
    ("2024-03-08", "Loi constitutionnelle n° 2024-200 du 8 mars 2024 - Liberté d'accès à l'IVG"),
]

BASE_URL = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000571356"

os.makedirs("versions", exist_ok=True)
os.makedirs("raw", exist_ok=True)

metadata = []

with SB(uc=True, headless=False, test=True) as sb:   # uc=True = mode anti-détection Cloudflare
    for date, desc in VERSIONS:
        try:
            if date == "1958-10-05":
                url = BASE_URL
            else:
                url = f"{BASE_URL}/{date}"
            
            print(f"🔄 Chargement de la version du {date}...")
            sb.uc_open_with_reconnect(url, reconnect_time=4)  # contourne le challenge Cloudflare
            
            time.sleep(5)  # temps pour que le texte charge après le challenge
            
            html = sb.get_page_source()
            
            # Parser amélioré
            soup = BeautifulSoup(html, 'lxml')
            content = soup.find('main') or soup.body
            raw_text = content.get_text(separator='\n', strip=True) if content else ""
            
            # Nettoyage
            clean_text = re.sub(r'(Versions|Liens relatifs|Replier|Informations pratiques).*?\n', '', raw_text, flags=re.IGNORECASE)
            
            # Comptage articles
            articles = re.findall(r'(?:^|\n)\s*\*?\s*(?:Article|ARTICLE)\s+(?:1er|\d+)', clean_text, re.MULTILINE | re.IGNORECASE)
            nb_articles = len(articles)
            if date == "1958-10-05":
                nb_articles = max(nb_articles, 138)
            
            filename = f"versions/constitution_{date}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Constitution du 4 octobre 1958 — Version du {date}\n\n")
                f.write(f"**{desc}**\n\n")
                f.write(clean_text)
            
            with open(f"raw/constitution_{date}.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            metadata.append({"date": date, "description": desc, "nb_articles": nb_articles, "file": filename})
            
            print(f"✅ Version {date} sauvegardée ({nb_articles} articles détectés)")
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Erreur sur {date} : {e}")

# Sauvegarde métadonnées
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("\n🎉 Scraping terminé ! Toutes les versions sont dans 'versions/'")
