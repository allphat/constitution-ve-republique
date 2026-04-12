import subprocess
import json

with open("metadata.json", encoding="utf-8") as f:
    metadata = json.load(f)

print(f"🚀 Début du versionnage : {len(metadata)} versions trouvées\n")

for entry in metadata:
    date = entry["date"]
    desc = entry["description"]
    file_path = entry["file"]
    nb_articles = entry.get("nb_articles", "?")

    tag_name = f"v{date}"

    # Vérifier si le tag existe déjà
    result = subprocess.run(["git", "tag", "-l", tag_name], capture_output=True, text=True)
    if tag_name in result.stdout:
        print(f"⏭️  Tag {tag_name} déjà existant → on passe")
        continue

    # Ajout + commit
    subprocess.run(["git", "add", file_path], check=True)
    
    commit_message = f"Version {date} - {desc} ({nb_articles} articles)"
    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"✅ Commit créé pour {date}")
    except subprocess.CalledProcessError:
        print(f"⚠️  Rien de nouveau pour {date} (déjà commité)")

    # Création du tag
    subprocess.run(["git", "tag", "-a", tag_name, "-m", desc], check=True)
    print(f"🏷️  Tag créé : {tag_name}")

print("\n🎉 Versionnage terminé !")
print("Commandes utiles :")
print("   git tag --list | sort")
print("   git log --oneline --graph --decorate")
print("   git checkout v2008-07-23   # pour voir la version de 2008")
