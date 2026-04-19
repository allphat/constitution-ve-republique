# Évolution de la Constitution de la Ve République

Une visualisation interactive de l’évolution de la Constitution française depuis 1958 jusqu’à aujourd’hui.

Ce projet permet de :
- Explorer toutes les versions historiques de la Constitution
- Visualiser l’évolution du nombre d’articles au fil du temps
- Comparer n’importe quelles deux versions avec un diff détaillé
- Filtrer par période pour mieux comprendre les grandes réformes

## 🌐 Page en ligne

→ **[https://allphat.github.io/constitution-ve-republique/](https://allphat.github.io/constitution-ve-republique/)**

## Fonctionnalités

- **Timeline interactive** : Cliquez sur une version pour afficher le texte complet
- **Graphique d’évolution** : Nombre d’articles de 1958 à 2024
- **Comparaison détaillée** : Entre deux versions quelconques avec :
  - Articles ajoutés / supprimés / modifiés
  - Pourcentages de changement
  - Diff coloré (ajouts en vert, suppressions en rouge)
- **Filtres par période** : 1958-1970, 1971-1990, 1991-2000, 2001-2010, 2011-2024

## Données

- **25 versions** officielles de la Constitution (1958 à 2024)
- Données extraites directement de [Legifrance](https://www.legifrance.gouv.fr)
- Chaque version est versionnée dans Git avec un tag par date


## Comment ça marche ?

1. Les données sont scrapées depuis Legifrance
2. Chaque version est sauvegardée dans `clean_versions/`
3. Les diffs sont générés entre toutes les paires de versions
4. La page GitHub Pages affiche tout de manière interactive


N’hésitez pas à explorer les différentes périodes et à comparer les versions pour mieux comprendre l’histoire institutionnelle de la Ve République !
