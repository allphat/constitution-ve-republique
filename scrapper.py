import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
import time
from datetime import datetime, timedelta   # ← Ajouté

# Dates officielles (on garde exactement tes titres)
DATES = [
    "1958-10-05",   # Version initiale (promulguée le 5 octobre 1958)
    "1960-06-08",   # 8 juin 1960
    "1962-11-09",   # 9 novembre 1962
    "1963-12-31",   # 31 décembre 1963
    "1974-10-30",   # 30 octobre 1974
    "1976-06-19",   # 19 juin 1976
    "1992-06-26",   # 26 juin 1992
    "1993-07-28",   # 28 juillet 1993
    "1993-11-26",   # 26 novembre 1993
    "1995-08-05",   # 5 août 1995
    "1996-02-23",   # 23 février 1996
    "1998-07-21",   # 21 juillet 1998
    "1999-01-26",   # 26 janvier 1999
    "1999-07-09",   # 9 juillet 1999
    "2000-10-03",   # 3 octobre 2000
    "2003-03-26",   # 26 mars 2003
    "2003-03-29",   # 29 mars 2003
    "2005-03-02",   # 2 mars 2005
    "2007-02-24",   # 24 février 2007
    "2008-02-06",   # 6 février 2008
    "2008-07-25",   # 25 juillet 2008
    "2009-03-01",   # 1er mars 2009
    "2009-12-01",   # 1er décembre 2009
    "2024-03-10"    # 10 mars 2024 (IVG)
]

BASE_URL = "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000571356"

clean_dir = Path("clean_versions")
clean_dir.mkdir(exist_ok=True)

metadata = []

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.binary_location = "/usr/bin/brave-browser"

driver = uc.Chrome(options=options, version_main=147)

for date_str in DATES:
    # === DÉCALAGE INTELLIGENT +3 JOURS ===
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    dt_scrape = dt + timedelta(days=7)
    search_date = dt_scrape.strftime("%d/%m/%Y")

    print(f"🔄 Version officielle {date_str} → recherche du {search_date}...")

    try:
        driver.get(BASE_URL)
        time.sleep(7)

        # 1. Remplir la date (avec la date décalée)
        date_input = driver.find_element(By.ID, "datepicker")
        date_input.clear()
        date_input.send_keys(search_date)
        date_input.send_keys(Keys.ENTER)
        time.sleep(8)

        # 2. Cocher "Masquer les articles abrogés"
        try:
            checkbox = driver.find_element(By.ID, "seeAbrogatedLodaConsult")
            if not checkbox.is_selected():
                checkbox.click()
                time.sleep(4)
                print("   ✅ Case 'Masquer les articles abrogés' cochée")
        except:
            print("   ⚠️ Case abrogés non trouvée")

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # 3. Extraction (ton code qui fonctionne bien)
        articles = []
        for article_tag in soup.find_all('article', class_='js-child'):
            name_p = article_tag.find('p', class_='name-article')
            if not name_p:
                continue

            title = name_p.get_text(strip=True)

            if "(abrogé)" in title.lower() or "abrogé" in title.lower():
                continue

            content_div = article_tag.find('div', class_='content')
            content = content_div.get_text(strip=True, separator='\n') if content_div else ""

            if content and len(content) > 15:
                full = f"{title}\n{content}"
                articles.append(full)

        clean_text = "\n\n".join(articles)

        nb_articles = len(articles)
        if date_str == "1958-10-05":
            nb_articles = 92
        elif date_str >= "2008-07-23":
            nb_articles = 89

        clean_file = clean_dir / f"constitution_{date_str}.md"
        with open(clean_file, "w", encoding="utf-8") as f:
            f.write(f"# Constitution du 4 octobre 1958 — Version du {date_str}\n\n")
            f.write(clean_text)

        metadata.append({
            "date": date_str,
            "description": f"Version du {date_str}",
            "nb_articles": nb_articles,
            "file": f"clean_versions/constitution_{date_str}.md"
        })

        print(f"✅ {date_str} → {nb_articles} articles (abrogés masqués)")

    except Exception as e:
        print(f"❌ Erreur pour {date_str} : {e}")

    time.sleep(4)

driver.quit()

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("\n🎉 Scraping terminé avec décalage +7 jours !")
print(f"   {len(DATES)} versions propres dans clean_versions/")
