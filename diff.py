from pathlib import Path
import subprocess

dates = [
    "1958-10-05", "1960-06-04", "1962-11-06", "1963-12-30", "1974-10-29",
    "1976-06-18", "1992-06-25", "1993-07-27", "1993-11-25", "1995-08-04",
    "1996-02-22", "1998-07-20", "1999-01-25", "1999-07-08", "2000-10-02",
    "2003-03-25", "2003-03-28", "2005-03-01", "2007-02-23", "2008-02-04",
    "2008-07-23", "2011-07-13", "2012-11-09", "2013-03-13", "2024-03-08"
]

diff_dir = Path("docs/diffs")
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

print("\n✅ Tous les diffs ont été générés et nettoyés dans docs/diffs/")
print("Tu peux maintenant relancer ton serveur local et tester la comparaison.")
