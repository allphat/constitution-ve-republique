from pathlib import Path
import json

def extract_articles(text):
    articles = {}
    lines = text.splitlines()
    current = None
    content = []
    
    for line in lines:
        if line.strip().startswith("Article "):
            if current:
                articles[current] = "\n".join(content).strip()
            current = line.strip()
            content = []
        elif current:
            content.append(line)
    
    if current:
        articles[current] = "\n".join(content).strip()
    
    return articles

print("🔄 Génération de TOUTES les stats de comparaison...")

clean_dir = Path("clean_versions")
stats = {}

version_files = sorted(clean_dir.glob("constitution_*.md"))
versions = [f.stem.replace("constitution_", "") for f in version_files]

for i in range(len(versions)):
    for j in range(i + 1, len(versions)):
        v1 = versions[i]
        v2 = versions[j]
        
        file1 = clean_dir / f"constitution_{v1}.md"
        file2 = clean_dir / f"constitution_{v2}.md"
        
        text1 = file1.read_text(encoding="utf-8")
        text2 = file2.read_text(encoding="utf-8")
        
        art1 = extract_articles(text1)
        art2 = extract_articles(text2)
        
        added = sum(1 for a in art2 if a not in art1)
        removed = sum(1 for a in art1 if a not in art2)
        modified = sum(1 for a in art1 if a in art2 and art1[a] != art2[a])
        
        base = len(art1) or 1
        added_pct = round((added / base) * 100, 1)
        removed_pct = round((removed / base) * 100, 1)
        modified_pct = round((modified / base) * 100, 1)
        
        key = f"{v1}_vs_{v2}"
        stats[key] = {
            "added": added,
            "removed": removed,
            "modified": modified,
            "addedPercent": f"{added_pct}%",
            "removedPercent": f"{removed_pct}%",
            "modifiedPercent": f"{modified_pct}%",
            "base_articles": base
        }
        
        print(f"✓ {v1} vs {v2} → +{added} ({added_pct}%) | -{removed} ({removed_pct}%) | Δ{modified} ({modified_pct}%)")

# Sauvegarde
output_file = Path("comparison_stats.json")
output_file.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"\n✅ Fichier généré : {output_file}")
print(f"   Nombre total de comparaisons : {len(stats)}")
