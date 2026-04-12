import subprocess
import json
import os

# Chargement des métadonnées (créé par le scraper)
with open("metadata.json", encoding="utf-8") as f:
    metadata = json.load(f)

print("🚀 Début du versionnage Git...\n")

for entry in metadata:
    date = entry["date"]
    desc = entry["description"]
    file_path = entry["file"]
    nb_articles = entry.get("nb_articles", "?")
    
    # Ajout du fichier
    subprocess.run(["git", "add", file_path], check=True)
    
    # Commit
    commit_message = f"Version {date} - {desc} ({nb_articles} articles)"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    
    # Tag
    tag_name = f"v{date}"
    subprocess.run(["git", "tag", "-a", tag_name, "-m", desc], check=True)
    
    print(f"✅ Tag créé : {tag_name} | {desc}")

print("\n🎉 Versionnage terminé !")
print(f"Tu as maintenant {len(metadata)} versions commitées et taggées.")
print("\nCommandes utiles :")
print("   git tag --list          # voir tous les tags")
print("   git checkout v2008-07-23 # voir la Constitution à cette date")
print("   git log --oneline --graph")
