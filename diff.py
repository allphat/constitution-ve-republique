from pathlib import Path
import subprocess

dates = [
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

diff_dir = Path("./diffs")
diff_dir.mkdir(exist_ok=True, parents=True)

print("🔨 Génération des diffs propres...\n")

for i in range(len(dates)):
    for j in range(i + 1, len(dates)):
        d1 = dates[i]
        d2 = dates[j]
        
        file1 = Path("clean_versions") / f"constitution_{d1}.md"
        file2 = Path("clean_versions") / f"constitution_{d2}.md"
        
        if not file1.exists() or not file2.exists():
            print(f"⚠️ Fichier manquant : {d1} ou {d2}")
            continue

        try:
            # Génération du diff brut
            result = subprocess.run(['diff', '-u', str(file1), str(file2)], 
                                  capture_output=True, text=True)

            # Nettoyage : on enlève les 2 premières lignes + toutes les lignes @@ 
            lines = result.stdout.splitlines()
            clean_lines = []
            
            for line in lines:
                if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                    continue
                clean_lines.append(line)

            diff_file = diff_dir / f"{d1}_vs_{d2}.diff"
            with open(diff_file, "w", encoding="utf-8") as f:
                f.write('\n'.join(clean_lines))

            print(f"✓ {d1} vs {d2}  →  {len(clean_lines)} lignes conservées")

        except Exception as e:
            print(f"✗ Erreur {d1} vs {d2} : {e}")

print("\n✅ Tous les diffs ont été générés et nettoyés dans diffs/")
print("Tu peux maintenant relancer ton serveur local et tester la comparaison.")
