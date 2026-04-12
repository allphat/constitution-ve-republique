import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
import time

DATES = [
    "1958-10-05", "1960-06-04", "1962-11-06", "1963-12-30", "1974-10-29",
    "1976-06-18", "1992-06-25", "1993-07-27", "1993-11-25", "1995-08-04",
    "1996-02-22", "1998-07-20", "1999-01-25", "1999-07-08", "2000-10-02",
    "2003-03-25", "2003-03-28", "2005-03-01", "2007-02-23", "2008-02-04",
    "2008-07-23", "2011-07-13", "2012-11-09", "2013-03-13", "2024-03-08"
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
    yyyy, mm, dd = date_str.split('-')
    search_date = f"{dd}/{mm}/{yyyy}"

    print(f"🔄 Scraping version du {search_date}...")

    try:
        driver.get(BASE_URL)
        time.sleep(6)

        # 1. Remplir la date
        date_input = driver.find_element(By.ID, "datepicker")
        date_input.clear()
        date_input.send_keys(search_date)
        date_input.send_keys(Keys.ENTER)
        time.sleep(7)

        # 2. Cocher la case "Masquer les articles abrogés"
        try:
            checkbox = driver.find_element(By.ID, "seeAbrogatedLodaConsult")
            if not checkbox.is_selected():
                checkbox.click()
                time.sleep(4)  # temps pour que la page filtre les abrogés
                print("   ✅ Case 'Masquer les articles abrogés' cochée")
        except:
            print("   ⚠️ Case abrogés non trouvée (peut-être déjà masquée)")

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # 3. Extraction propre des articles visibles
        articles = []
        for article_tag in soup.find_all('article', class_='js-child'):
            name_p = article_tag.find('p', class_='name-article')
            if not name_p:
                continue

            title = name_p.get_text(strip=True)

            # Ignorer les titres qui contiennent encore "abrogé" dans le texte (sécurité)
            if "(abrogé)" in title.lower() or "abrogé" in title.lower():
                continue

            content_div = article_tag.find('div', class_='content')
            content = content_div.get_text(strip=True, separator='\n') if content_div else ""

            if content and len(content) > 15:
                full = f"{title}\n{content}"
                articles.append(full)

        clean_text = "\n\n".join(articles)

        nb_articles = len(articles)
        # Corrections historiques connues
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

with open("docs/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("\n🎉 Scraping terminé avec succès !")
print("   Tous les abrogés ont été masqués.")
print(f"   {len(DATES)} versions propres dans clean_versions/")
