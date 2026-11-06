# CHECKIT.AI — Carnet technique des scripts d'exploration

**Projet OpenClassrooms :** Projet 12 — Extrayez des données multimodales de sites web  
**Étape :** Étape 1 — Exploration et qualification des sources de données  
**Environnement :** Serveur Ubuntu  
**Objectif du document :** Conserver les commandes, scripts et méthodes utilisés pour inspecter et qualifier les quatre sources de données retenues pour CheckIt.AI.

---

## 1. Objectif du carnet technique

Ce document rassemble progressivement les commandes et scripts utilisés pendant l'exploration des sources de données du projet CheckIt.AI.

Il doit permettre de :

- conserver une trace reproductible des inspections réalisées ;
- comprendre le rôle de chaque commande ;
- retrouver les résultats ayant servi à qualifier les sources ;
- justifier les observations et statistiques présentées dans le rapport d'exploration ;
- préparer les futures opérations d'extraction et de transformation des données.

Les commandes seront présentées une par une, dans l'ordre de leur utilisation.

Une distinction sera faite entre :

- les commandes effectivement utilisées ;
- les commandes reconstituées à partir des résultats conservés ;
- les scripts envisagés pour les étapes ultérieures, mais pas encore exécutés.

## 2. Environnement de travail

**Serveur :** Ubuntu 24.04 LTS

**Répertoire du projet :**

\`\`\`bash
/mnt/projects/vk_oc_projet12_checkitai-multimodal-etl
\`\`\`

**Répertoire de stockage des données :**

\`\`\`bash
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl
\`\`\`

Les données sources sont conservées dans le répertoire `raw`, organisé par source.

---

# 3. Source 1 — Fakeddit

## 3.1. Inspection initiale du fichier

### Objectif

Examiner le fichier d'entraînement multimodal Fakeddit avant toute transformation.

Cette première inspection permet de vérifier :

- l'existence du fichier ;
- sa taille ;
- son type et son encodage ;
- la présence de son en-tête ;
- la structure générale de ses premières lignes.

### Fichier inspecté

\`\`\`bash
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakeddit/multimodal_train.tsv
\`\`\`

### Commandes utilisées

\`\`\`bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl

ls -lh /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakeddit/multimodal_train.tsv

file /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakeddit/multimodal_train.tsv

head -n 3 /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakeddit/multimodal_train.tsv
\`\`\`

### Explication des commandes

| Commande | Fonction |
|---|---|
| `cd` | Se positionne à la racine du projet. |
| `ls -lh` | Affiche les informations du fichier, notamment sa taille dans un format lisible. |
| `file` | Identifie le type de fichier et fournit des indications sur son encodage. |
| `head -n 3` | Affiche les trois premières lignes du fichier, sans afficher l'intégralité du corpus. |

### Résultats obtenus

L'inspection a permis de constater que :

- le fichier existe dans le répertoire `raw/fakeddit` ;
- sa taille est d'environ **149 Mo** ;
- il s'agit d'un fichier TSV (valeurs séparées par des tabulations) ;
- le fichier possède un en-tête décrivant les colonnes disponibles.

Les principaux champs identifiés sont notamment :

- `author`
- `clean_title`
- `created_utc`
- `domain`
- `hasImage`
- `id`
- `image_url`
- `linked_submission_id`
- `num_comments`
- `score`
- `subreddit`
- `title`
- `upvote_ratio`
- `2_way_label`
- `3_way_label`
- `6_way_label`

### Conclusion

Cette première inspection confirme que le fichier contient des publications textuelles accompagnées de métadonnées, de références vers des images et de plusieurs niveaux de labels.

Le fichier est donc adapté à une première analyse statistique et à une qualification de son potentiel multimodal.

**Remarque :** cette inspection ne vérifie pas encore que les images référencées sont réellement accessibles ou exploitables. Cette validation nécessite des contrôles complémentaires.

---

*Fin du premier script d'exploration. Les scripts suivants seront ajoutés dans l'ordre de leur utilisation.*

## 4.2. Analyse statistique du fichier multimodal

### Objectif

Après avoir vérifié la structure du fichier `multimodal_train.tsv`, nous avons analysé son contenu afin de mesurer :

- Le nombre total de publications ;
- Les colonnes disponibles ;
- Les valeurs manquantes ;
- La répartition des labels Fake/True ;
- La répartition des catégories à 3 et 6 classes ;
- La disponibilité des références vers les images.

Cette analyse permet d'évaluer la qualité et l'équilibre du corpus avant son utilisation pour entraîner un modèle.

### Fichier analysé

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakeddit/multimodal_train.tsv
```

### Environnement Python
L'analyse a été réalisée avec Python et la bibliothèque `pandas`, installée dans l'environnement virtuel du projet.

Pour lancer l'interpréteur Python :

\`\`\`bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl

uv run python
\`\`\`

### Script Python

\`\`\`python
import pandas as pd
from pathlib import Path

# Chemin du fichier Fakeddit
file_path = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "raw/fakeddit/multimodal_train.tsv"
)

# Chargement du fichier TSV
df = pd.read_csv(file_path, sep="\t")

# 1. Dimensions du jeu de données
print("\n--- DIMENSIONS ---")
print(f"Nombre de publications : {len(df)}")
print(f"Nombre de colonnes : {len(df.columns)}")

# 2. Liste des colonnes
print("\n--- COLONNES ---")
print(df.columns.tolist())

# 3. Valeurs manquantes
print("\n--- VALEURS MANQUANTES ---")
print(df.isna().sum())

# 4. Répartition des labels binaires
print("\n--- LABELS BINAIRES (2 classes) ---")
print(df["2_way_label"].value_counts(dropna=False))
print(
    df["2_way_label"].value_counts(normalize=True).mul(100).round(2)
)

# 5. Répartition des labels à 3 classes
print("\n--- LABELS (3 classes) ---")
print(df["3_way_label"].value_counts(dropna=False))
print(
    df["3_way_label"].value_counts(normalize=True).mul(100).round(2)
)

# 6. Répartition des labels à 6 classes
print("\n--- LABELS (6 classes) ---")
print(df["6_way_label"].value_counts(dropna=False))
print(
    df["6_way_label"].value_counts(normalize=True).mul(100).round(2)
)

# 7. Présence des références d'images
print("\n--- PRÉSENCE DES URL D'IMAGES ---")
print(f"URL d'image manquantes : {df['image_url'].isna().sum()}")
print(f"URL d'image renseignées : {df['image_url'].notna().sum()}")

print("\n--- INDICATEUR hasImage ---")
print(df["hasImage"].value_counts(dropna=False))
\`\`\`

### Explication du script

| Instruction | Fonction |
|---|---|
| `pd.read_csv(..., sep="\t")` | Charge le fichier TSV dans un DataFrame pandas. |
| `len(df)` | Compte le nombre de publications. |
| `len(df.columns)` | Compte le nombre de colonnes. |
| `df.columns.tolist()` | Affiche les noms des colonnes. |
| `df.isna().sum()` | Compte les valeurs manquantes dans chaque colonne. |
| `value_counts()` | Compte les occurrences de chaque label. |
| `value_counts(normalize=True)` | Calcule la proportion de chaque label. |
| `isna()` | Identifie les références d'images manquantes. |
| `notna()` | Identifie les références d'images renseignées. |

### Résultats obtenus

#### Dimensions du corpus

| Indicateur | Résultat |
|---|---:|
| Nombre de publications | 564 000 |
| Nombre de colonnes | 16 |
| `clean_title` manquants | 0 |
| `title` manquants | 0 |
| URL d'image manquantes | 1 534 |
| URL d'image renseignées | 562 466 |
| Publications avec `hasImage = True` | 564 000 |

#### Répartition des labels binaires (2 classes)

| Label | Signification | Nombre de publications |
|---|---|---:|
| 0 | Fake | 341 919 |
| 1 | True | 222 081 |
| **Total** | | **564 000** |

#### Répartition des labels à 3 classes

| Label | Signification | Nombre de publications |
|---|---|---:|
| 0 | Fake with false text | 222 081 |
| 1 | Fake with true text | 13 848 |
| 2 | True | 328 071 |
| **Total** | | **564 000** |

#### Répartition des labels à 6 classes

| Label | Signification | Nombre de publications |
|---|---|---:|
| 0 | True | 222 081 |
| 1 | Satire/Parody | 33 481 |
| 2 | Misleading Content | 107 221 |
| 3 | Imposter Content | 11 784 |
| 4 | False Connection | 167 857 |
| 5 | Manipulated Content | 21 576 |
| **Total** | | **564 000** |

### Interprétation des résultats

Cette analyse a mis en évidence plusieurs éléments importants.

**1. Un corpus volumineux**

Le fichier contient 564 000 publications et 16 colonnes. Il constitue une base intéressante pour une première expérimentation de détection multimodale.

**2. Un déséquilibre entre les classes**

Les catégories ne sont pas représentées dans les mêmes proportions.

Ce déséquilibre est particulièrement important dans les classifications à 3 et 6 classes.

Lors de l'entraînement et de l'évaluation des futurs modèles, il faudra donc surveiller :

- Le macro-F1 ;
- Le rappel par classe ;
- La précision par classe ;
- La matrice de confusion.

L'accuracy seule ne sera pas suffisante pour évaluer correctement les performances.

**3. Une incohérence dans les métadonnées des images**

Le champ `hasImage` vaut `True` pour les 564 000 publications.

Cependant, 1 534 publications ne possèdent aucune valeur dans le champ `image_url`.

Il faut donc distinguer :

- La présence déclarée d'une image dans les métadonnées ;
- L'existence d'une URL d'image ;
- L'accessibilité réelle du fichier image.

Une URL renseignée ne garantit pas que l'image est toujours disponible ou téléchargeable.

### Conclusion

Cette analyse confirme que Fakeddit constitue une source intéressante pour la première constitution du corpus multimodal de CheckIt.AI.

Elle fournit :

- Un volume important de publications ;
- Des textes exploitables ;
- Des références vers des images ;
- Plusieurs niveaux de classification ;
- Des métadonnées utiles pour la traçabilité.

Elle révèle également deux points de vigilance :

- Le déséquilibre des classes ;
- Les incohérences possibles entre les indicateurs de présence d'image et les URL réellement renseignées.

Un contrôle complémentaire de l'accessibilité et de la validité des images sera nécessaire avant de constituer le sous-ensemble multimodal exploitable.

---

*Fin du script 2 — Analyse statistique du fichier Fakeddit.*


# 5. Source 1 — Fakeddit

## 5.1. Contrôle des références d'images

### Objectif

Après l'analyse statistique générale du fichier Fakeddit, nous souhaitons approfondir le contrôle des références vers les images.

Cette vérification permet de déterminer :

- Combien de publications possèdent une URL d'image ;
- Combien ne possèdent pas de référence vers une image ;
- Si les URL renseignées présentent un format HTTP ou HTTPS ;
- Si le champ `hasImage` est cohérent avec la présence d'une URL dans `image_url`.

Cette étape est importante pour CheckIt.AI, car l'objectif est de constituer un corpus réellement multimodal, associant des contenus textuels à des images exploitables.

**Attention :** ce script contrôle la présence et la forme des URL. Il ne vérifie pas encore que les images sont effectivement accessibles sur Internet.

### Fichier source

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakeddit/multimodal_train.tsv
```

### Programme Python

Nom proposé pour le fichier du script :

```text
scripts/analyse_images_fakeddit.py
```

Pour créer et ouvrir ce fichier avec Vim :

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl

vim scripts/analyse_images_fakeddit.py
```

Programme Python :

```python
import pandas as pd
from pathlib import Path

# Chemin du fichier source
file_path = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "raw/fakeddit/multimodal_train.tsv"
)

# Chargement du fichier
df = pd.read_csv(file_path, sep="\t")

# Vérification de la présence des URL
url_present = df["image_url"].notna() & (
    df["image_url"].astype(str).str.strip() != ""
)

# Vérification simple du format des URL
url_http = df["image_url"].astype(str).str.startswith(
    ("http://", "https://")
)

# Statistiques générales
print("\n--- BILAN DES IMAGES FAKEDDIT ---")
print(f"Nombre total de publications : {len(df)}")
print(f"URL renseignées : {url_present.sum()}")
print(f"URL absentes : {(~url_present).sum()}")

# Cohérence de hasImage
print("\n--- COHERENCE hasImage / image_url ---")

has_image = df["hasImage"].astype(str).str.lower().eq("true")

print(
    "hasImage=True mais URL absente :",
    (has_image & ~url_present).sum()
)

print(
    "hasImage=False mais URL présente :",
    (~has_image & url_present).sum()
)

# Contrôle de la forme des URL
print("\n--- FORMAT DES URL ---")

print(
    "URL commençant par http:// ou https:// :",
    (url_present & url_http).sum()
)

print(
    "URL renseignées avec format inattendu :",
    (url_present & ~url_http).sum()
)

# Quelques exemples de publications sans URL
print("\n--- EXEMPLES DE PUBLICATIONS SANS URL ---")
print(
    df.loc[~url_present, ["id", "title", "hasImage"]].head(10)
)
```

### Explication du programme

Le programme utilise la bibliothèque `pandas` pour charger et analyser le fichier TSV.

| Instruction | Fonction |
|---|---|
| `pd.read_csv(..., sep="\t")` | Charge le fichier TSV dans un DataFrame pandas. |
| `notna()` | Identifie les valeurs qui ne sont pas nulles. |
| `str.strip()` | Supprime les espaces au début et à la fin des chaînes de caractères. |
| `astype(str)` | Convertit les valeurs en chaînes de caractères pour les contrôles. |
| `startswith()` | Vérifie si une URL commence par `http://` ou `https://`. |
| `&` | Combine deux conditions : les deux doivent être vraies. |
| `~` | Inverse une condition. |
| `df.loc[...]` | Sélectionne les publications répondant à une condition. |
| `head(10)` | Affiche au maximum dix exemples. |
| `sum()` | Compte le nombre de valeurs répondant à une condition booléenne. |

### Détail du fonctionnement

**1. Détection des URL présentes**

Le programme commence par identifier les valeurs non nulles du champ `image_url`, puis vérifie que les chaînes ne sont pas vides ou composées uniquement d'espaces.

Cela permet de ne pas confondre une valeur vide avec une URL réellement renseignée.

**2. Contrôle du format des URL**

Le programme vérifie que les URL commencent par `http://` ou `https://`.

Il s'agit d'un contrôle syntaxique simple, et non d'une vérification de l'existence de la ressource distante.

**3. Cohérence des métadonnées**

Le programme compare deux informations :

- Le champ `hasImage`, qui indique si le jeu de données déclare la présence d'une image ;
- Le champ `image_url`, qui contient la référence vers cette image.

Cette comparaison permet de détecter les publications dont les métadonnées sont incohérentes.

**4. Affichage d'exemples**

Le programme affiche jusqu'à dix publications sans URL d'image, avec leur identifiant, leur titre et leur indicateur `hasImage`.

Cela facilite une éventuelle inspection manuelle.

### Résultats déjà observés

L'analyse précédente du fichier Fakeddit avait permis d'établir les résultats suivants :

| Indicateur | Résultat |
|---|---:|
| Nombre total de publications | 564 000 |
| URL renseignées | 562 466 |
| URL absentes | 1 534 |
| `hasImage=True` mais URL absente | 1 534 |
| `hasImage=False` mais URL présente | 0 |

Le nombre exact d'URL commençant par HTTP ou HTTPS devra être confirmé par l'exécution de ce nouveau programme.

### Interprétation

Cette vérification met en évidence une incohérence dans les métadonnées du jeu de données.

Le champ `hasImage` ne suffit pas à confirmer la présence d'une référence exploitable.

Il est donc préférable de contrôler directement le champ `image_url`.

Cependant, une URL renseignée ne garantit pas que l'image est toujours accessible ou téléchargeable.

Il faudra donc distinguer trois niveaux de validation :

1. **Présence de la référence :** le champ `image_url` contient une valeur.
2. **Validité de la référence :** l'URL présente une structure HTTP ou HTTPS acceptable.
3. **Accessibilité du média :** le fichier image est effectivement récupérable et exploitable.

La troisième vérification nécessitera un contrôle HTTP et, éventuellement, une validation du fichier téléchargé avec la bibliothèque Pillow.

### Conclusion

Ce script constitue une étape complémentaire de qualification de la source Fakeddit.

Il permet de mieux identifier les publications dont les métadonnées d'images sont incomplètes et de préparer la constitution d'un sous-ensemble multimodal fiable.

Pour CheckIt.AI, seules les publications associant un texte exploitable et au moins une image explicitement associée et accessible pourront intégrer le corpus multimodal sélectionné.

**Statut :** script proposé pour une vérification complémentaire. Les résultats de son exécution restent à confirmer.

---

*Fin du script 3 — Contrôle des références d'images Fakeddit.*

# 6. Source 2 — FakeNewsNet

## 6.1. Inspection initiale des fichiers CSV

### Objectif

Examiner les quatre fichiers CSV du dépôt FakeNewsNet afin de vérifier :

- Leur présence ;
- Leur taille ;
- Leurs noms ;
- Leur structure générale ;
- Leurs premières lignes ;
- Les informations disponibles pour chaque publication.

Cette première inspection permet de comprendre comment les données sont organisées avant d'envisager leur enrichissement.

### Présentation des fichiers analysés

Le dépôt FakeNewsNet contient quatre fichiers CSV principaux :

```text
gossipcop_fake.csv
gossipcop_real.csv
politifact_fake.csv
politifact_real.csv
```

Ces fichiers sont organisés selon deux sources de vérification :

- GossipCop ;
- PolitiFact.

Chaque source distingue les publications classées comme fausses (`fake`) et celles classées comme réelles (`real`).

### Emplacement des fichiers

Répertoire local prévu :

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakenewsnet/
```

### Commandes utilisées

**1. Afficher les fichiers et leurs tailles**

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl

ls -lh /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakenewsnet/
```

**2. Examiner les premières lignes d'un fichier CSV**

```bash
head -n 5 /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakenewsnet/gossipcop_fake.csv
```

### Explication des commandes

| Commande | Fonction |
|---|---|
| `cd` | Se positionne à la racine du projet. |
| `ls -lh` | Affiche les fichiers présents et leurs tailles dans un format lisible. |
| `head -n 5` | Affiche les cinq premières lignes d'un fichier CSV, sans afficher l'intégralité de son contenu. |

### Résultats obtenus

L'exploration du dépôt a permis d'identifier quatre fichiers :

| Fichier | Source | Label indiqué par le nom |
|---|---|---|
| `gossipcop_fake.csv` | GossipCop | Fake |
| `gossipcop_real.csv` | GossipCop | Real |
| `politifact_fake.csv` | PolitiFact | Fake |
| `politifact_real.csv` | PolitiFact | Real |

Les quatre fichiers présentent la même structure générale, avec les colonnes suivantes :

| Colonne | Description | Utilité pour CheckIt.AI |
|---|---|---|
| `id` | Identifiant de la publication | Identification |
| `news_url` | URL de l'article d'origine | Accès à la publication |
| `title` | Titre de l'article | Donnée textuelle |
| `tweet_ids` | Identifiants des tweets associés | Lien avec les données sociales |

### Interprétation

FakeNewsNet ne fournit pas directement un corpus multimodal complet dans ses fichiers CSV.

Les fichiers contiennent principalement des informations de référencement :

- Un identifiant ;
- Un titre ;
- Une URL d'article ;
- Des identifiants de tweets associés.

Le texte intégral et les images doivent être recherchés sur les sites des éditeurs à partir des URL disponibles.

Les identifiants de tweets permettent également d'envisager un enrichissement social, sous réserve des conditions d'accès aux données de la plateforme.

Les labels `fake` et `real` sont déduits du nom des fichiers. Il faudra conserver cette provenance plutôt que considérer ces labels comme une vérité universelle.

### Conclusion

Cette première inspection confirme que FakeNewsNet constitue une source complémentaire intéressante pour CheckIt.AI.

Elle permet de disposer de références vers des articles et des publications sociales, mais nécessite une étape d'enrichissement pour récupérer les textes complets et les références vers les images.

Cette source sera donc utilisée comme point de départ pour rechercher des publications et compléter leurs métadonnées.

**Remarque :** les commandes présentées correspondent aux inspections réalisées sur le dépôt. Le chemin local indiqué suppose que les fichiers CSV sont présents dans `raw/fakenewsnet`. Si les fichiers sont stockés ailleurs, il faudra adapter le chemin.

---

*Fin du script 4 — Inspection initiale des fichiers CSV FakeNewsNet.*

# 7. Source 2 — FakeNewsNet

## 7.1. Analyse statistique des quatre fichiers CSV

### Objectif

Après l'inspection initiale des fichiers CSV, nous souhaitons réaliser une analyse plus détaillée afin de connaître :

- Le nombre de publications dans chaque fichier ;
- Le nombre total de publications ;
- Les colonnes disponibles ;
- Les valeurs manquantes ;
- Les éventuels doublons d'identifiants ;
- La structure des URL d'articles ;
- La présence des identifiants de tweets associés.

Cette analyse permet de déterminer quelles informations sont directement disponibles et quelles informations devront être récupérées ultérieurement.

### Fichiers analysés

Les quatre fichiers CSV sont :

```text
gossipcop_fake.csv
gossipcop_real.csv
politifact_fake.csv
politifact_real.csv
```

Répertoire local :

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakenewsnet/
```

### Environnement Python

L'analyse utilise Python et la bibliothèque `pandas`.

Pour lancer l'interpréteur Python :

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl

uv run python
```

### Programme Python

Le programme suivant permet d'analyser les quatre fichiers successivement.

```python
import pandas as pd
from pathlib import Path

# Répertoire contenant les fichiers CSV
data_dir = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "raw/fakenewsnet"
)

# Liste des fichiers à analyser
files = [
    "gossipcop_fake.csv",
    "gossipcop_real.csv",
    "politifact_fake.csv",
    "politifact_real.csv",
]

total_publications = 0

for filename in files:

    file_path = data_dir / filename

    print("\n" + "=" * 60)
    print(f"ANALYSE DU FICHIER : {filename}")
    print("=" * 60)

    # Chargement du fichier CSV
    df = pd.read_csv(file_path)

    # Nombre de publications
    nb_rows = len(df)
    total_publications += nb_rows

    print(f"Nombre de publications : {nb_rows}")
    print(f"Nombre de colonnes : {len(df.columns)}")

    # Affichage des colonnes
    print("\n--- COLONNES ---")
    print(df.columns.tolist())

    # Valeurs manquantes
    print("\n--- VALEURS MANQUANTES ---")
    print(df.isna().sum())

    # Doublons d'identifiants
    print("\n--- DOUBLONS ---")
    print("Identifiants dupliqués :", df["id"].duplicated().sum())

    # Présence des URL
    print("\n--- URL DES ARTICLES ---")
    print("URL renseignées :", df["news_url"].notna().sum())
    print("URL manquantes :", df["news_url"].isna().sum())

    # Présence des identifiants de tweets
    print("\n--- IDENTIFIANTS DE TWEETS ---")
    print("Valeurs renseignées :", df["tweet_ids"].notna().sum())
    print("Valeurs manquantes :", df["tweet_ids"].isna().sum())

    # Exemples de publications
    print("\n--- PREMIÈRES PUBLICATIONS ---")
    print(df.head(3))

print("\n" + "=" * 60)
print("BILAN GLOBAL")
print("=" * 60)

print(f"Nombre total de publications : {total_publications}")
```

### Explication du programme

| Instruction | Fonction |
|---|---|
| `Path()` | Définit le chemin du répertoire de données. |
| `pd.read_csv()` | Charge un fichier CSV dans un DataFrame pandas. |
| `for filename in files` | Parcourt successivement les quatre fichiers. |
| `len(df)` | Compte les lignes du fichier. |
| `len(df.columns)` | Compte les colonnes. |
| `df.columns.tolist()` | Affiche la liste des colonnes. |
| `df.isna().sum()` | Compte les valeurs manquantes. |
| `df["id"].duplicated().sum()` | Compte les identifiants répétés dans chaque fichier. |
| `notna()` | Identifie les valeurs renseignées. |
| `isna()` | Identifie les valeurs manquantes. |
| `df.head(3)` | Affiche les trois premières publications. |

### Résultats et observations

L'exploration des quatre fichiers a permis de confirmer qu'ils possèdent tous la même structure :

```text
id,news_url,title,tweet_ids
```

Les champs ont les significations suivantes :

| Champ | Signification |
|---|---|
| `id` | Identifiant de la publication dans le jeu de données. |
| `news_url` | Adresse de l'article original. |
| `title` | Titre de l'article. |
| `tweet_ids` | Identifiants des tweets associés à la publication. |

Les fichiers sont séparés selon la source de vérification et la catégorie attribuée à la publication.

**Important :** les volumes exacts par fichier et le nombre de valeurs manquantes doivent être repris à partir de la sortie réelle du programme. Ils ne sont pas renseignés ici afin de ne pas inventer de résultats.

### Interprétation

Cette analyse permet de dégager plusieurs points importants.

**1. Une structure homogène**

Les quatre fichiers possèdent les mêmes colonnes. Il sera donc possible de les traiter avec une méthode commune, en ajoutant des métadonnées permettant de conserver leur provenance.

**2. Des labels implicites**

Les catégories `fake` et `real` sont déduites du nom du fichier.

Il faudra créer des champs explicites lors de la transformation des données, par exemple :

- `label` : catégorie attribuée ;
- `label_source` : GossipCop ou PolitiFact ;
- `label_status` : statut de qualification.

**3. Des URL à contrôler**

La présence d'une URL dans `news_url` ne garantit pas que la page soit toujours accessible.

Certaines URL peuvent être incomplètes, anciennes ou indisponibles.

Il faudra conserver l'URL originale et, si nécessaire, créer une URL normalisée séparément.

**4. Des identifiants de tweets à interpréter**

Le champ `tweet_ids` contient des identifiants associés à la publication.

Ces identifiants peuvent être séparés par des tabulations ou des espaces. Ils devront être interprétés comme une liste et non comme une simple chaîne de caractères.

La récupération effective des tweets dépendra des possibilités d'accès aux données de la plateforme et de ses règles d'utilisation.

### Conclusion

FakeNewsNet fournit une structure de référencement homogène pour des publications issues de deux sources de vérification.

Les fichiers CSV constituent une base de départ pour rechercher les articles et leurs contenus multimodaux.

Cependant, les textes complets et les images ne sont pas directement présents dans ces fichiers.

Une étape complémentaire de collecte sur les sites éditeurs sera donc nécessaire.

---

*Fin du script 5 — Analyse statistique des fichiers CSV FakeNewsNet.*

# 8. Source 2 — FakeNewsNet

## 8.1. Analyse des URL d'articles et des identifiants de tweets

### Objectif

Après l'analyse statistique des quatre fichiers CSV, nous souhaitons examiner plus précisément deux champs :

- `news_url` : URL de l'article d'origine ;
- `tweet_ids` : identifiants des tweets associés à chaque publication.

Cette analyse permet de mieux comprendre la qualité des références disponibles et de préparer les futures opérations d'enrichissement.

Les principaux contrôles sont :

- repérer les URL manquantes ;
- identifier les URL sans protocole HTTP ou HTTPS ;
- examiner les éventuelles URL dupliquées ;
- mesurer la présence des identifiants de tweets ;
- analyser la séparation des identifiants dans le champ `tweet_ids` ;
- compter le nombre de tweets associés à chaque publication.

### Fichiers analysés

```text
gossipcop_fake.csv
gossipcop_real.csv
politifact_fake.csv
politifact_real.csv
```

Répertoire local :

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/fakenewsnet/
```

### Programme Python

Nom proposé :

```text
scripts/analyse_urls_tweets_fakenewsnet.py
```

Pour créer le fichier :

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl

vim scripts/analyse_urls_tweets_fakenewsnet.py
```

Programme Python :

```python
import pandas as pd
from pathlib import Path

# Répertoire contenant les fichiers CSV
data_dir = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "raw/fakenewsnet"
)

files = [
    "gossipcop_fake.csv",
    "gossipcop_real.csv",
    "politifact_fake.csv",
    "politifact_real.csv",
]

for filename in files:

    file_path = data_dir / filename
    df = pd.read_csv(file_path)

    print("\n" + "=" * 60)
    print(f"ANALYSE : {filename}")
    print("=" * 60)

    # 1. Nettoyage temporaire des URL
    urls = df["news_url"].fillna("").astype(str).str.strip()

    # 2. Détection des URL présentes
    url_present = urls.ne("")

    # 3. Détection des URL avec protocole HTTP ou HTTPS
    url_with_protocol = urls.str.startswith(
        ("http://", "https://"),
        na=False
    )

    print("\n--- URL DES ARTICLES ---")
    print("URL renseignées :", url_present.sum())
    print("URL absentes :", (~url_present).sum())

    print(
        "URL avec protocole HTTP/HTTPS :",
        (url_present & url_with_protocol).sum()
    )

    print(
        "URL sans protocole HTTP/HTTPS :",
        (url_present & ~url_with_protocol).sum()
    )

    # 4. Recherche des URL dupliquées
    print(
        "URL dupliquées :",
        urls[url_present].duplicated().sum()
    )

    # 5. Analyse des identifiants de tweets
    tweets = df["tweet_ids"].fillna("").astype(str).str.strip()

    print("\n--- IDENTIFIANTS DE TWEETS ---")
    print("Publications avec tweet_ids :", tweets.ne("").sum())
    print("Publications sans tweet_ids :", tweets.eq("").sum())

    # 6. Séparation des identifiants par espaces ou tabulations
    def count_tweets(value):
        if not value:
            return 0

        return len(value.split())

    tweet_counts = tweets.apply(count_tweets)

    print("\n--- NOMBRE DE TWEETS PAR PUBLICATION ---")
    print("Total des identifiants :", tweet_counts.sum())
    print("Moyenne :", round(tweet_counts.mean(), 2))
    print("Maximum :", tweet_counts.max())

    # 7. Quelques exemples d'URL sans protocole
    print("\n--- EXEMPLES D'URL SANS PROTOCOLE ---")

    print(
        df.loc[
            url_present & ~url_with_protocol,
            ["id", "news_url", "title"]
        ].head(5)
    )

    # 8. Quelques exemples de publications avec tweets
    print("\n--- EXEMPLES DE TWEET_IDS ---")

    print(
        df.loc[
            tweets.ne(""),
            ["id", "tweet_ids"]
        ].head(5)
    )
```

### Explication du programme

| Instruction | Fonction |
|---|---|
| `fillna("")` | Remplace temporairement les valeurs manquantes par une chaîne vide. |
| `astype(str)` | Convertit les valeurs en chaînes de caractères. |
| `str.strip()` | Supprime les espaces au début et à la fin. |
| `ne("")` | Identifie les valeurs différentes d'une chaîne vide. |
| `eq("")` | Identifie les chaînes vides. |
| `str.startswith()` | Vérifie le début d'une URL. |
| `duplicated()` | Identifie les valeurs répétées. |
| `split()` | Sépare une chaîne en éléments selon les espaces et tabulations. |
| `apply()` | Applique une fonction à chaque valeur d'une colonne. |
| `mean()` | Calcule la moyenne. |
| `max()` | Recherche la valeur maximale. |
| `df.loc[]` | Sélectionne les lignes répondant à une condition. |

### Détail du fonctionnement

**1. Contrôle des URL**

Le programme identifie les URL absentes et celles qui ne commencent pas par `http://` ou `https://`.

Une URL sans protocole n'est pas nécessairement invalide. Elle peut simplement nécessiter une normalisation avant son utilisation.

Il faudra conserver la valeur d'origine dans les données brutes et créer une valeur normalisée dans une étape ultérieure.

**2. Recherche des doublons**

Le programme recherche les URL répétées dans chaque fichier.

Cette opération permet de repérer plusieurs publications qui pourraient pointer vers la même adresse.

Un doublon d'URL ne signifie toutefois pas nécessairement un doublon de publication : il faudra examiner les titres et les identifiants avant toute suppression.

**3. Analyse des identifiants de tweets**

Le champ `tweet_ids` peut contenir plusieurs identifiants dans une même cellule.

La fonction `split()` permet de séparer ces identifiants lorsqu'ils sont délimités par des espaces ou des tabulations.

Le programme calcule ensuite :

- le nombre de publications avec des identifiants ;
- le nombre de publications sans identifiants ;
- le nombre total d'identifiants ;
- le nombre moyen de tweets par publication ;
- le nombre maximal de tweets associés à une publication.

### Résultats et observations déjà établis

Lors de notre inspection manuelle des quatre fichiers, nous avons observé que :

- les quatre fichiers utilisent la même structure de colonnes ;
- certaines URL ne comportent pas de protocole ;
- d'autres URL commencent directement par `https://` ;
- le champ `tweet_ids` peut contenir plusieurs identifiants ;
- les identifiants sont séparés par des espaces ou des tabulations.

Les résultats numériques détaillés de ce programme devront être confirmés par son exécution.

### Interprétation

Cette analyse met en évidence deux besoins pour la future chaîne de traitement.

**1. Normaliser les URL sans perdre leur valeur d'origine**

Il est préférable de conserver deux champs :

- `article_url_raw` : URL originale telle qu'elle apparaît dans le CSV ;
- `article_url_normalized` : URL normalisée pour les opérations de collecte.

Cela permet de garder la traçabilité et d'éviter de modifier silencieusement les données sources.

**2. Transformer les identifiants de tweets en liste**

Le champ `tweet_ids` devra être converti en une véritable liste d'identifiants lors de la transformation des données.

Cette organisation facilitera les éventuelles opérations d'enrichissement social.

La collecte effective des tweets restera soumise aux conditions d'accès de la plateforme et aux règles applicables aux données personnelles.

### Conclusion

Ce script approfondit la qualification de FakeNewsNet en examinant la qualité des références vers les articles et les données sociales associées.

Il prépare deux opérations importantes pour la suite du projet :

- la normalisation et la validation des URL ;
- la transformation des identifiants de tweets en données structurées.

Il ne télécharge pas encore les articles, les images ou les tweets.

---

*Fin du script 6 — Analyse des URL et des identifiants de tweets FakeNewsNet.*

# 9. Source 2 — FakeNewsNet

## 9.1. Inspection du mécanisme de récupération des articles

### Objectif

FakeNewsNet fournit principalement des fichiers CSV contenant les titres, les URL des articles et les identifiants des tweets associés.

Le contenu complet des articles et les références vers leurs images doivent être récupérés séparément.

Le dépôt officiel propose un mécanisme de collecte utilisant notamment la bibliothèque `newspaper`.

L'objectif de cette inspection est de comprendre :

- comment les articles sont téléchargés ;
- comment leur texte est extrait ;
- comment les URL des images sont identifiées ;
- quelles métadonnées sont récupérées ;
- quelles limites techniques peuvent affecter la collecte.

### Dépôt étudié

Dépôt officiel :

[https://github.com/KaiDMML/FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet)

Fichier étudié :

```text
news_content_collection.py
```

### Commandes d'inspection

Depuis le serveur Ubuntu :

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl
```

Si le dépôt officiel FakeNewsNet a été cloné localement, rechercher le fichier :

```bash
find /mnt/projects -type f -name "news_content_collection.py"
```

Si le dépôt n'est pas présent localement, il est possible de consulter directement le fichier sur GitHub.

### Inspection des fonctions principales

Dans le fichier `news_content_collection.py`, repérer les fonctions suivantes :

```python
crawl_link_article(url)
```

Cette fonction utilise la bibliothèque `newspaper` pour télécharger une page web et tenter d'en extraire les informations principales.

```python
crawl_news_article(news)
```

Cette fonction organise la récupération d'un article et peut utiliser une archive du site si l'URL d'origine ne fonctionne plus.

```python
collect_news_articles(news_list, ...)
```

Cette fonction organise la collecte d'une liste d'articles et l'enregistrement des résultats.

### Informations extraites

Le code utilise notamment les propriétés suivantes de l'objet `Article` :

| Propriété | Description |
|---|---|
| `article.text` | Texte principal de l'article |
| `article.title` | Titre de l'article |
| `article.top_image` | Image principale identifiée par le parseur |
| `article.images` | Ensemble des URL d'images détectées |
| `article.authors` | Auteurs identifiés |
| `article.publish_date` | Date de publication détectée |
| `article.canonical_link` | URL canonique |
| `article.keywords` | Mots-clés extraits |
| `article.summary` | Résumé généré ou extrait |
| `article.meta_data` | Métadonnées de la page |

### Fonctionnement technique

La bibliothèque `newspaper` automatise plusieurs opérations :

1. Téléchargement de la page web.
2. Analyse du HTML.
3. Identification du contenu principal.
4. Extraction du texte et des métadonnées.
5. Identification des références vers les images.
6. Préparation des informations pour leur enregistrement.

Le code historique de FakeNewsNet prévoit également une tentative de récupération à partir de la Wayback Machine lorsque l'article original n'est plus accessible.

### Points de vigilance identifiés

**1. Les images ne sont pas nécessairement téléchargées**

La propriété `article.images` fournit des URL d'images. Elle ne garantit pas que les fichiers correspondants soient effectivement téléchargés et conservés localement.

Il faudra donc prévoir une étape distincte de téléchargement et de validation des images.

**2. Les images détectées ne sont pas toutes nécessairement pertinentes**

Une page web peut contenir :

- le logo du média ;
- des icônes ;
- des publicités ;
- des images de navigation ;
- des illustrations sans rapport avec l'article.

Il faudra vérifier que l'image retenue est bien associée à la publication.

**3. Les articles peuvent être indisponibles**

Une URL peut être invalide, supprimée, bloquée ou inaccessible.

La Wayback Machine constitue une solution de secours, mais elle ne garantit pas la récupération de tous les articles.

**4. Le code historique présente des limites techniques**

L'ancien code comporte notamment des mécanismes de gestion des erreurs et des délais d'attente qui devront être réévalués avant toute réutilisation.

Il sera préférable de développer ultérieurement un collecteur indépendant, adapté à notre architecture CheckIt.AI.

### Conséquences pour notre architecture

Pour notre futur collecteur FakeNewsNet, nous distinguerons plusieurs étapes :

```text
CSV FakeNewsNet
      |
      v
Lecture des métadonnées
      |
      v
Validation de l'URL
      |
      v
Téléchargement de la page
      |
      v
Extraction du texte et des métadonnées
      |
      v
Identification des images
      |
      v
Téléchargement et validation des images
      |
      v
Enregistrement des données structurées
```

Chaque étape devra conserver son statut afin de pouvoir distinguer :

- un article récupéré correctement ;
- un article inaccessible ;
- un article récupéré avec un contenu incomplet ;
- un article sans image exploitable.

### Conclusion

L'inspection du code officiel montre que FakeNewsNet constitue une source enrichissable : les CSV fournissent les références initiales et le code historique permet de comprendre comment récupérer les contenus associés.

Toutefois, les images ne sont pas garanties et les mécanismes historiques ne seront pas repris aveuglément.

Nous privilégierons un collecteur indépendant, plus robuste et mieux adapté aux exigences du projet.

---

*Fin du script 7 — Inspection du mécanisme de récupération des articles FakeNewsNet.*

# 10. Source 4 — CIMPLE Knowledge Graph

## 10.1. Inspection du fichier RDF et de sa structure

### Objectif

CIMPLE Knowledge Graph fournit des données structurées de fact-checking au format RDF.

Contrairement aux fichiers CSV de Fakeddit et FakeNewsNet, les informations sont représentées sous forme de relations entre des ressources.

L'objectif de cette première inspection est de :

- vérifier le fichier téléchargé ;
- contrôler son intégrité avec son empreinte SHA-256 ;
- examiner sa structure N-Triples ;
- identifier les principaux types de ressources ;
- comprendre comment les affirmations et les vérifications sont reliées.

### Fichier analysé

Archive téléchargée :

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz
```

Format : N-Triples compressé avec gzip (`.nt.gz`).

### 1. Vérification de la présence et de la taille du fichier

Commande :

```bash
ls -lh /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz
```

Cette commande permet de vérifier que l'archive est présente et d'observer sa taille.

### 2. Vérification de l'intégrité SHA-256

Commande :

```bash
sha256sum /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz
```

Empreinte attendue :

```text
afcdb40a734276c50791975ffb1754e2b981decacd4cd15f585947fd5fba1da2
```

L'empreinte permet de vérifier que le fichier téléchargé correspond à l'archive annoncée pour cette version.

### 3. Vérification de la décompression

Commande :

```bash
gzip -t /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz
```

Cette commande vérifie l'intégrité du flux compressé sans créer de fichier décompressé.

### 4. Inspection des premières lignes

Commande :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz | head -n 20
```

L'option `-d` décompresse les données et `-c` envoie le résultat vers la sortie standard.

L'opérateur `|` transmet le résultat à `head`, qui affiche uniquement les premières lignes.

### 5. Comprendre la structure N-Triples

Une ligne RDF N-Triples représente une relation entre trois éléments :

```text
<sujet> <prédicat> <objet> .
```

- **Sujet** : ressource décrite.
- **Prédicat** : propriété ou relation.
- **Objet** : valeur ou autre ressource associée.

Par exemple, une relation peut indiquer qu'une vérification porte sur une affirmation.

Les URI identifient les ressources et les propriétés du graphe.

### 6. Compter les principaux types de ressources

Commande :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep -c 'rdf-syntax-ns#type.*schema.org/Rating'

gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep -c 'rdf-syntax-ns#type.*schema.org/ClaimReview'

gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep -c 'rdf-syntax-ns#type.*schema.org/Claim'

gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep -c 'rdf-syntax-ns#type.*schema.org/Organization'
```

Ces commandes comptent les lignes qui déclarent les ressources comme appartenant aux quatre types recherchés.

### Résultats observés

Pour l'archive étudiée, les comptages obtenus sont :

| Type de ressource | Nombre |
|---|---:|
| `schema:Rating` | 30 356 |
| `schema:ClaimReview` | 800 |
| `schema:Claim` | 800 |
| `schema:Organization` | 40 |

Attention : ces nombres correspondent aux ressources typées présentes dans l'archive examinée. Ils ne doivent pas être confondus avec les statistiques globales annoncées pour l'ensemble du Knowledge Graph.

### 7. Premières propriétés à rechercher

Les propriétés suivantes sont particulièrement intéressantes pour CheckIt.AI :

| Propriété | Utilité |
|---|---|
| `schema:text` | Texte de l'affirmation ou de la vérification |
| `schema:url` | URL de la publication de fact-checking |
| `schema:datePublished` | Date de publication |
| `schema:inLanguage` | Langue déclarée |
| `schema:author` | Organisation ou auteur associé |
| `schema:itemReviewed` | Affirmation examinée |
| `schema:reviewRating` | Évaluation associée à la vérification |
| `schema:ratingValue` | Valeur textuelle de l'évaluation |

Ces propriétés permettent de construire progressivement une représentation structurée des vérifications.

### Interprétation

Cette première inspection montre que CIMPLE est une source de données structurées particulièrement intéressante pour enrichir notre base avec des informations de fact-checking.

Elle fournit notamment des relations entre :

- une publication de vérification ;
- une affirmation examinée ;
- une évaluation ;
- une organisation associée.

En revanche, cette archive ne doit pas être considérée comme une source multimodale directe : les propriétés d'images recherchées lors de l'inspection initiale n'ont pas révélé de champ d'image direct parmi les propriétés examinées.

### Conclusion

Le format RDF permet de représenter les relations entre les affirmations et leurs vérifications sans perdre leur provenance.

CIMPLE sera donc principalement utilisé comme source d'enrichissement et de qualification des labels, en complément des sources fournissant directement des textes et des images.

---

*Fin du script 8 — Inspection du fichier RDF de CIMPLE Knowledge Graph.*

# 11. Source 4 — CIMPLE Knowledge Graph

## 11.1. Analyse des relations entre ClaimReview, Claim et Rating

### Objectif

Après avoir vérifié la structure du fichier RDF, nous allons examiner les relations entre les principales ressources du graphe.

Trois types de ressources sont particulièrement importants :

- `schema:ClaimReview` : publication de fact-checking ;
- `schema:Claim` : affirmation examinée ;
- `schema:Rating` : évaluation ou verdict associé.

L'objectif est de comprendre comment retrouver :

- le texte de la vérification ;
- le texte de l'affirmation examinée ;
- la source de la vérification ;
- la date de publication ;
- la langue déclarée ;
- le verdict associé.

### Fichier analysé

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz
```

### 1. Examiner les relations entre les ressources

Les principales propriétés RDF utilisées sont :

| Propriété | Rôle |
|---|---|
| `schema:itemReviewed` | Relie une vérification à l'affirmation examinée |
| `schema:reviewRating` | Relie une vérification à son évaluation |
| `schema:ratingValue` | Contient la valeur textuelle du verdict |
| `schema:text` | Contient le texte de la vérification ou de l'affirmation |
| `schema:url` | Indique l'URL de la publication |
| `schema:author` | Identifie l'organisation ou l'auteur associé |
| `schema:datePublished` | Indique la date de publication |
| `schema:inLanguage` | Indique la langue déclarée |

### 2. Rechercher les relations ClaimReview vers Claim

Commande :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep 'schema.org/itemReviewed' \
  | head -n 10
```

Cette commande affiche quelques relations entre les publications de vérification et les affirmations examinées.

La propriété `itemReviewed` permet de retrouver l'identifiant de la ressource `Claim` associée à une ressource `ClaimReview`.

### 3. Rechercher les relations ClaimReview vers Rating

Commande :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep 'schema.org/reviewRating' \
  | head -n 10
```

La propriété `reviewRating` permet de retrouver la ressource `Rating` associée à une vérification.

Cette relation est essentielle pour récupérer le verdict.

### 4. Examiner un exemple de publication de vérification

Une ressource `ClaimReview` étudiée lors de l'exploration possède l'identifiant suivant :

```text
http://data.cimple.eu/claim-review/b1c6b990c065e3d6d73f87f0b7eee24da751c5ba9cdca9fc7a4d94a5
```

Pour retrouver les relations associées à cette ressource :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep 'b1c6b990c065e3d6d73f87f0b7eee24da751c5ba9cdca9fc7a4d94a5'
```

L'examen de cette ressource a permis d'observer :

- son type `schema:ClaimReview` ;
- un texte de fact-checking ;
- une URL vers la publication originale de vérification ;
- une date de publication ;
- une langue déclarée ;
- une relation vers une affirmation ;
- une relation vers une évaluation.

### 5. Examiner l'affirmation associée

L'affirmation reliée à cet exemple possède l'identifiant :

```text
http://data.cimple.eu/claim/3e00baad74c331cb920287be8d30a856dea64b5c00df5e034e3ae829
```

Commande :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep '3e00baad74c331cb920287be8d30a856dea64b5c00df5e034e3ae829'
```

Cette ressource contient notamment :

- le texte de l'affirmation ;
- son type RDF ;
- des annotations complémentaires.

Lors de notre inspection, nous avons également observé des propriétés relatives au sentiment, à l'émotion et à l'orientation politique.

Ces annotations ne constituent pas des verdicts de véracité.

### 6. Examiner le verdict associé

La ressource `Rating` observée dans cet exemple possède l'identifiant :

```text
http://data.cimple.eu/rating/106253df3b4fcbf1973d3b0cc30bddc25220b07db3df488ad7e34b72
```

Commande :

```bash
gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
  | grep '106253df3b4fcbf1973d3b0cc30bddc25220b07db3df488ad7e34b72'
```

Dans cet exemple, la ressource contient notamment :

- `schema:ratingValue` : `False` ;
- `schema:name` : `False` ;
- `schema:sameAs` : une URI correspondant à `not_credible` ;
- des relations vers plusieurs organisations.

Cela montre que le verdict est représenté dans une ressource distincte de la publication de vérification.

### 7. Comprendre la structure relationnelle

Le modèle simplifié peut être représenté ainsi :

```text
          ClaimReview
               |
       +-------+-------+
       |               |
  itemReviewed    reviewRating
       |               |
       v               v
     Claim           Rating
       |               |
       v               v
 Texte de           Verdict
 l'affirmation
```

Cette séparation permet de conserver les différentes informations sans les confondre.

### Résultats observés

Sur l'archive étudiée :

- 800 ressources `ClaimReview` ;
- 800 ressources `Claim` ;
- 30 356 ressources `Rating` ;
- 800 relations `reviewRating` ;
- 670 relations `datePublished` ;
- 800 relations `inLanguage`.

Pour les 800 ressources `ClaimReview`, les 800 relations `reviewRating` observées indiquent que chaque publication de vérification de cet échantillon possède une relation vers une évaluation.

### Points de vigilance

**1. Le verdict n'est pas nécessairement binaire**

Les valeurs possibles ne se limitent pas à `True` et `False`.

Il faut préserver les catégories d'origine et éviter de transformer automatiquement les verdicts incertains ou non vérifiables en fausses informations.

**2. Une ressource Rating peut être partagée**

Une même ressource `Rating` peut être référencée par plusieurs publications de vérification.

Il ne faut donc pas supposer qu'une ressource `Rating` correspond toujours à une seule publication.

**3. La langue déclarée doit être contrôlée**

Lors de notre inspection, le texte d'un exemple était en marathi alors que la propriété `inLanguage` indiquait `English`.

Cette incohérence montre qu'il faudra prévoir un contrôle de langue indépendant.

**4. Les annotations complémentaires ne sont pas des labels de vérité**

Les propriétés relatives au sentiment, à l'émotion ou à l'orientation politique ne doivent pas être utilisées comme verdicts de fact-checking.

### Conséquences pour CheckIt.AI

Lors de la future transformation des données, nous conserverons des entités distinctes :

- une publication de fact-checking ;
- une affirmation examinée ;
- une évaluation ;
- une organisation source.

Nous conserverons également les identifiants RDF d'origine afin de maintenir la traçabilité des relations.

### Conclusion

Cette analyse confirme que CIMPLE permet de relier une affirmation à sa vérification et à son verdict.

Cette organisation est particulièrement intéressante pour enrichir CheckIt.AI avec des informations de vérification documentées et traçables.

CIMPLE sera donc utilisé comme source d'enrichissement des labels, et non comme source principale d'images.

---

*Fin du script 9 — Analyse des relations ClaimReview, Claim et Rating de CIMPLE.*

# 12. Source 4 — CIMPLE Knowledge Graph

## 12.1. Analyse statistique des verdicts et des langues

### Objectif

Après avoir identifié les relations entre les ressources `ClaimReview`, `Claim` et `Rating`, nous allons examiner la répartition des verdicts et des langues déclarées.

Cette analyse permet de :

- mesurer la fréquence des différentes catégories de verdicts ;
- identifier les catégories majoritaires et minoritaires ;
- connaître la diversité linguistique des publications ;
- repérer les éventuelles valeurs manquantes ;
- évaluer les précautions nécessaires avant l'utilisation de ces données pour entraîner un modèle.

### Fichier analysé

```text
/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz
```

### Méthode d'analyse

Nous allons utiliser Python avec la bibliothèque `rdflib`.

Cette bibliothèque permet de charger un graphe RDF et d'interroger ses ressources et ses propriétés.

Pour cette analyse, nous allons :

1. décompresser l'archive ;
2. charger les données RDF ;
3. identifier les ressources `ClaimReview` ;
4. récupérer leur relation `reviewRating` ;
5. retrouver la valeur du verdict ;
6. récupérer la langue déclarée ;
7. calculer les distributions et les pourcentages.

### 1. Vérifier la disponibilité de rdflib

Depuis le répertoire du projet :

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl
```

Vérifier si la bibliothèque est disponible :

```bash
uv run python -c "import rdflib; print(rdflib.__version__)"
```

Si elle n'est pas installée, ajouter la dépendance :

```bash
uv add rdflib
```

### 2. Créer le script d'analyse

Nom proposé :

```text
scripts/analyse_verdicts_langues_cimple.py
```

Créer le fichier :

```bash
vim scripts/analyse_verdicts_langues_cimple.py
```

### 3. Programme Python

```python
import gzip
from collections import Counter
from pathlib import Path

from rdflib import Graph, Namespace, RDF, URIRef


# Chemin de l'archive RDF
archive_path = Path(
    "/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/"
    "raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz"
)

# Espaces de noms RDF
SCHEMA = Namespace("https://schema.org/")
SCHEMA_HTTP = Namespace("http://schema.org/")
ONTOLOGY = Namespace("http://data.cimple.eu/ontology#")

# Chargement du graphe RDF
graph = Graph()

with gzip.open(archive_path, "rb") as archive:
    graph.parse(source=archive, format="nt")

print("\n--- INFORMATIONS GÉNÉRALES ---")
print("Nombre total de triplets RDF :", len(graph))

# Recherche des ressources ClaimReview
claim_reviews = set(
    graph.subjects(
        RDF.type,
        SCHEMA.ClaimReview
    )
)

# Compatibilité avec les données utilisant schema.org en HTTP
claim_reviews.update(
    graph.subjects(
        RDF.type,
        SCHEMA_HTTP.ClaimReview
    )
)

print("Nombre de ressources ClaimReview :", len(claim_reviews))


def get_objects(subject, predicate):
    """
    Récupère les objets associés à un sujet et un prédicat,
    en testant les deux variantes HTTP et HTTPS de schema.org.
    """
    values = set(graph.objects(subject, predicate))

    predicate_text = str(predicate)

    if predicate_text.startswith("https://"):
        alternate = URIRef(
            predicate_text.replace("https://", "http://", 1)
        )
    elif predicate_text.startswith("http://"):
        alternate = URIRef(
            predicate_text.replace("http://", "https://", 1)
        )
    else:
        return values

    values.update(graph.objects(subject, alternate))
    return values


# Comptage des verdicts et des langues
verdict_counter = Counter()
language_counter = Counter()

missing_verdicts = 0
missing_languages = 0

for review in claim_reviews:

    # Récupération de l'évaluation associée
    ratings = get_objects(
        review,
        SCHEMA.reviewRating
    )

    verdicts = set()

    for rating in ratings:

        values = get_objects(
            rating,
            SCHEMA.ratingValue
        )

        names = get_objects(
            rating,
            SCHEMA.name
        )

        for value in values | names:
            verdicts.add(str(value).strip())

    if verdicts:
        for verdict in verdicts:
            verdict_counter[verdict] += 1
    else:
        missing_verdicts += 1

    # Récupération de la langue déclarée
    languages = get_objects(
        review,
        SCHEMA.inLanguage
    )

    if languages:
        for language in languages:
            language_counter[str(language).strip()] += 1
    else:
        missing_languages += 1


# Affichage des verdicts
print("\n--- DISTRIBUTION DES VERDICTS ---")

for verdict, count in verdict_counter.most_common():

    percentage = count / len(claim_reviews) * 100

    print(
        f"{verdict}: {count} "
        f"({percentage:.2f} %)"
    )

print("Publications sans verdict :", missing_verdicts)


# Affichage des langues
print("\n--- DISTRIBUTION DES LANGUES ---")

for language, count in language_counter.most_common():

    percentage = count / len(claim_reviews) * 100

    print(
        f"{language}: {count} "
        f"({percentage:.2f} %)"
    )

print("Publications sans langue déclarée :", missing_languages)

print(
    "\nNombre de langues distinctes :",
    len(language_counter)
)
```

### 4. Exécuter le programme

```bash
uv run python scripts/analyse_verdicts_langues_cimple.py
```

### Explication du programme

| Élément | Fonction |
|---|---|
| `gzip.open()` | Ouvre l'archive compressée sans décompression manuelle préalable. |
| `Graph()` | Crée un graphe RDF. |
| `graph.parse()` | Charge les triplets N-Triples. |
| `Namespace()` | Définit les espaces de noms RDF. |
| `RDF.type` | Permet d'identifier le type d'une ressource. |
| `graph.subjects()` | Recherche les sujets correspondant à un type donné. |
| `graph.objects()` | Récupère les objets associés à une relation. |
| `Counter()` | Compte les occurrences de chaque catégorie. |
| `most_common()` | Affiche les catégories les plus fréquentes. |

### Résultats observés précédemment

Lors de notre exploration de cette archive, nous avons obtenu la distribution suivante pour les verdicts :

| Verdict | Nombre | Pourcentage approximatif |
|---|---:|---:|
| `not_credible` | 526 | 65,75 % |
| `credible` | 111 | 13,88 % |
| `uncertain` | 68 | 8,50 % |
| `not_verifiable` | 56 | 7,00 % |
| `mostly_credible` | 39 | 4,88 % |
| **Total** | **800** | **100 % environ** |

Les langues déclarées étaient réparties comme suit :

| Langue | Nombre |
|---|---:|
| English | 318 |
| Turkish | 173 |
| Slovak | 79 |
| Spanish | 72 |
| Portuguese | 38 |
| Bangla | 31 |
| Telugu | 29 |
| Russian | 19 |
| Romanian | 15 |
| Arabic | 12 |
| French | 5 |
| Filipino | 5 |
| Greek | 2 |
| Ukrainian | 1 |
| Indonesian | 1 |
| **Total** | **800** |

Ces 800 publications représentent 15 langues déclarées. La statistique globale du Knowledge Graph annonce 29 langues : les deux chiffres ne portent donc pas sur le même périmètre.

### Interprétation des résultats

**1. Une distribution des verdicts déséquilibrée**

La catégorie `not_credible` représente environ 65,75 % des publications étudiées.

Cette prédominance indique un déséquilibre important entre les catégories.

Pour les futurs entraînements, il faudra donc éviter de se limiter à l'accuracy. Des indicateurs tels que le macro-F1, le rappel par classe et la matrice de confusion seront plus informatifs.

**2. Les verdicts ne sont pas strictement binaires**

Les catégories `uncertain` et `not_verifiable` ne doivent pas être assimilées à des informations fausses.

La catégorie `mostly_credible` ne doit pas non plus être automatiquement transformée en `credible`.

Il faudra préserver les verdicts originaux et définir une stratégie de normalisation explicite.

**3. Une diversité linguistique inégale**

L'anglais et le turc représentent une part importante des publications.

Le français est très peu représenté dans cet échantillon, avec seulement cinq publications.

Il faudra tenir compte de cette distribution lors de la sélection des données et de l'évaluation des modèles multilingues.

**4. La langue déclarée doit être vérifiée**

Une langue renseignée dans le graphe ne garantit pas que le texte soit effectivement rédigé dans cette langue.

Nous avons déjà observé un exemple de texte en marathi associé à la valeur `English`.

Un contrôle indépendant de la langue sera donc nécessaire.

### Conséquences pour CheckIt.AI

Pour conserver la qualité des données, nous appliquerons les principes suivants :

- conserver le verdict original ;
- conserver la source de la vérification ;
- ne pas transformer les verdicts incertains en faux ;
- enregistrer la langue déclarée ;
- prévoir un contrôle de langue indépendant ;
- documenter les déséquilibres entre catégories.

### Conclusion

Cette analyse confirme que CIMPLE apporte des informations de fact-checking structurées, mais que leur utilisation nécessite une attention particulière à la distribution des verdicts et des langues.

La source est intéressante pour enrichir les publications avec des évaluations documentées, à condition de préserver les catégories d'origine et leur provenance.

---

*Fin du script 10 — Analyse statistique des verdicts et des langues CIMPLE.*


# 13. Source 4 — CIMPLE Knowledge Graph

## 13.1. Recherche des propriétés multimodales liées aux images

### Objectif

CIMPLE est principalement une base de connaissances structurée autour des affirmations et des publications de fact-checking.

Dans le cadre du projet CheckIt.AI, nous devons déterminer si cette source contient également des références vers des images associées aux affirmations ou aux vérifications.

L'objectif de cette analyse est de :

- rechercher les propriétés RDF couramment utilisées pour référencer des images ;
- identifier d'éventuelles URL de médias ;
- vérifier si des ressources visuelles sont directement associées aux publications ;
- déterminer la place de CIMPLE dans notre architecture multimodale.

### Fichier analysé

    /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz

### 1. Recherche des propriétés RDF courantes liées aux images

Les propriétés suivantes sont intéressantes :

| Propriété                | Signification                           |
|--------------------------|-----------------------------------------|
| `schema:image`           | Image associée à une ressource          |
| `schema:thumbnailUrl`    | URL d'une miniature                     |
| `schema:associatedMedia` | Média associé à une ressource           |
| `schema:contentUrl`      | URL du contenu média                    |
| `foaf:depiction`         | Représentation visuelle d'une ressource |

Ces propriétés peuvent être utilisées pour représenter des références vers des images ou d'autres médias.

### 2. Commande de recherche

Exécuter la commande suivante :

    gzip -dc /mnt/data/vk_oc_projet12_checkitai-multimodal-etl/raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz \
      | grep -Ei 'schema.org/(image|thumbnailUrl|associatedMedia|contentUrl)|foaf/depiction' \
      | head -n 20

### 3. Explication de la commande

| Élément      | Fonction                                                   |
|--------------|------------------------------------------------------------|
| `gzip -dc`   | Décompresse l'archive sans créer de fichier intermédiaire. |
| `grep`       | Recherche les lignes correspondant à un motif.            |
| `-E`         | Active les expressions régulières étendues.                |
| `-i`         | Ignore les différences entre majuscules et minuscules.     |
| `-n`         | Affiche les numéros de ligne si nécessaire.                |
| `head -n 20` | Limite l'affichage aux 20 premières correspondances.        |

La recherche porte sur plusieurs propriétés courantes susceptibles de référencer des images.

### 4. Résultat observé

Lors de notre exploration de l'archive, cette recherche n'a retourné aucune correspondance.

Cela signifie qu'aucune des propriétés recherchées n'a été trouvée sous les formes d'URI examinées dans le fichier.

Il faut toutefois rester prudent : cette recherche ciblée ne démontre pas l'absence absolue de toute référence visuelle dans l'ensemble du graphe.

Des propriétés spécifiques ou des relations indirectes pourraient exister sans avoir été couvertes par cette commande.

### 5. Interprétation pour CheckIt.AI

Cette observation confirme que CIMPLE ne doit pas être considéré comme notre source principale d'images.

Son intérêt réside principalement dans les informations suivantes :

- texte des affirmations ;
- texte des publications de fact-checking ;
- verdicts ;
- dates de publication ;
- langues déclarées ;
- organisations de fact-checking ;
- URL des publications originales.

Les images devront donc être recherchées et collectées prioritairement auprès des autres sources du projet.

### 6. Positionnement dans l'architecture

La répartition des rôles est la suivante :

| Source      | Texte                                   | Images                                                          | Verdicts                                    |
|-------------|-----------------------------------------|-----------------------------------------------------------------|---------------------------------------------|
| Fakeddit    | Oui                                     | Références d'images                                             | Oui                                         |
| FakeNewsNet | À extraire des pages web                | À extraire des pages web                                        | Oui, selon les fichiers et leur provenance  |
| NewsData.io | Selon l'offre et les champs disponibles | URL d'images disponibles                                        | Pas de verdict de fact-checking             |
| CIMPLE      | Oui                                     | Pas de propriété directe identifiée dans la recherche effectuée | Oui                                         |

CIMPLE pourra être utilisé pour enrichir les publications provenant d'autres sources, à condition de pouvoir établir un rapprochement fiable entre les affirmations.

Une simple similarité de titre ne suffira pas à établir une correspondance certaine.

### Conclusion

L'analyse des propriétés RDF liées aux images n'a pas révélé de référence directe dans les propriétés recherchées.

CIMPLE sera donc principalement utilisé comme source de vérification et d'enrichissement des labels, tandis que la collecte multimodale reposera sur les autres sources sélectionnées.

---

*Fin du script 11 — Recherche des propriétés multimodales liées aux images dans CIMPLE.*

# 14. Bilan technique de l'exploration des quatre sources

## 14.1. Synthèse comparative des sources

### Objectif

Après l'exploration de Fakeddit, FakeNewsNet, NewsData.io et CIMPLE Knowledge Graph, nous allons établir un bilan technique global.

Cette synthèse permet de :

- comparer les formats et les structures des données ;
- identifier les informations disponibles directement ;
- distinguer les données à extraire des données déjà structurées ;
- identifier les limites techniques de chaque source ;
- définir le rôle de chaque source dans l'architecture CheckIt.AI.

### Tableau comparatif

| Critère | Fakeddit | FakeNewsNet | NewsData.io | CIMPLE |
|---|---|---|---|---|
| Type de source | Dataset | Dataset | API REST | Knowledge Graph |
| Format | TSV | CSV et JSON après collecte | JSON | RDF N-Triples |
| Texte | Directement disponible | À extraire des articles | Selon les champs et l'offre | Directement disponible |
| Images | URL disponibles | À extraire des pages web | URL disponibles selon les articles | Aucune propriété directe identifiée dans notre recherche |
| Vidéos | Non central | Non central | URL parfois disponibles | Non identifié dans notre inspection |
| Labels | 2, 3 et 6 classes | Fake / Real selon les fichiers | Pas de verdict de fact-checking | Plusieurs catégories de verdicts |
| Langues | Principalement anglais | Selon les publications | 90+ langues annoncées | 29 langues annoncées globalement |
| Méthode d'accès | Téléchargement de fichiers | CSV et collecte web | API REST | Téléchargement RDF ou SPARQL |
| Difficulté technique | Faible à moyenne | Élevée | Faible à moyenne | Moyenne à élevée |
| Rôle retenu | Dataset multimodal initial | Enrichissement des articles | Collecte complémentaire d'actualités | Enrichissement des vérifications |

## 14.2. Synthèse des analyses techniques réalisées

### Source 1 — Fakeddit

Fichier étudié :

    raw/fakeddit/multimodal_train.tsv

Principales opérations d'exploration :

- inspection du fichier TSV ;
- vérification de ses dimensions et de ses colonnes ;
- calcul des valeurs manquantes ;
- analyse des distributions des labels ;
- vérification de la présence des URL d'images ;
- examen de la cohérence entre `hasImage` et `image_url`.

Résultats principaux :

- 564 000 publications ;
- 16 colonnes ;
- 1 534 URL d'images manquantes ;
- 562 466 URL renseignées ;
- labels disponibles en 2, 3 et 6 classes ;
- déséquilibre entre certaines catégories.

Limite principale : les labels reposent sur une méthode de supervision distante et ne constituent pas une vérification individuelle de chaque publication.

**Décision :** conserver Fakeddit comme première source de données multimodales pour les expérimentations initiales.

### Source 2 — FakeNewsNet

Fichiers étudiés :

    gossipcop_fake.csv
    gossipcop_real.csv
    politifact_fake.csv
    politifact_real.csv

Principales opérations d'exploration :

- inspection des quatre fichiers CSV ;
- analyse de leurs colonnes communes ;
- examen des URL des articles ;
- analyse du champ `tweet_ids` ;
- inspection du code officiel de récupération des articles ;
- étude des mécanismes d'extraction du texte et des images.

Structure commune observée :

    id,news_url,title,tweet_ids

Informations disponibles :

- identifiant de publication ;
- URL de l'article ;
- titre ;
- identifiants des tweets associés.

Informations à enrichir :

- texte complet de l'article ;
- URL des images ;
- métadonnées de publication ;
- informations complémentaires sur les tweets, si leur accès est autorisé.

Limites principales :

- certaines URL sont incomplètes ;
- les articles peuvent être indisponibles ;
- les images doivent être identifiées et validées ;
- l'ancien code présente des dépendances et contraintes techniques ;
- les données complètes ne peuvent pas être redistribuées librement en raison des contraintes liées aux contenus et aux données Twitter.

**Décision :** utiliser FakeNewsNet comme source d'enrichissement des publications et des données sociales, avec un collecteur indépendant.

### Source 3 — NewsData.io

Documentation étudiée :

https://newsdata.io/documentation

Principales opérations d'exploration :

- analyse de la structure JSON ;
- identification des champs textuels ;
- identification des URL d'images et de vidéos ;
- examen des langues disponibles ;
- analyse des limitations de l'offre gratuite ;
- identification des champs qui ne constituent pas des labels de véracité.

Informations disponibles selon les réponses de l'API :

- titre ;
- URL de l'article ;
- nom et domaine de la source ;
- description ;
- contenu selon l'offre ;
- date de publication ;
- langue ;
- URL d'image ;
- URL de vidéo ;
- catégories et métadonnées complémentaires.

Limites principales :

- restrictions du forfait gratuit ;
- contenu intégral non disponible dans l'offre gratuite ;
- URL d'image parfois absente ;
- absence de verdict de fact-checking ;
- conditions d'utilisation et droits de réutilisation à vérifier.

**Décision :** utiliser NewsData.io comme source complémentaire de collecte d'actualités, sous réserve des conditions du service et du budget disponible.

### Source 4 — CIMPLE Knowledge Graph

Archive étudiée :

    raw/cimplekg/data.claimreview-kg_2026_11_02.nt.gz

Principales opérations d'exploration :

- vérification de l'intégrité SHA-256 ;
- vérification de l'archive gzip ;
- inspection des premières lignes N-Triples ;
- comptage des ressources RDF ;
- analyse des relations `ClaimReview`, `Claim` et `Rating` ;
- examen des verdicts ;
- analyse des langues ;
- recherche des propriétés RDF liées aux images.

Résultats observés dans l'archive :

| Ressource ou indicateur | Nombre |
|---|---:|
| `schema:Rating` | 30 356 |
| `schema:ClaimReview` | 800 |
| `schema:Claim` | 800 |
| `schema:Organization` | 40 |
| Relations `reviewRating` | 800 |
| Relations `datePublished` | 670 |
| Relations `inLanguage` | 800 |

Limites principales :

- catégories de verdicts non strictement binaires ;
- répartition linguistique inégale ;
- incohérences possibles entre langue déclarée et langue réelle ;
- absence de propriété directe d'image identifiée dans la recherche effectuée ;
- rapprochement avec d'autres sources nécessitant une méthode fiable.

**Décision :** utiliser CIMPLE comme source d'enrichissement et de qualification des verdicts de fact-checking.

---

## 14.3. Bilan des scripts d'exploration

Les fiches techniques de ce carnet sont organisées de la manière suivante :

| N° | Script ou opération | Source | Objectif |
|---:|---|---|---|
| 1 | Inspection initiale du fichier TSV | Fakeddit | Vérifier le format et la structure |
| 2 | Statistiques descriptives | Fakeddit | Mesurer les volumes, valeurs manquantes et labels |
| 3 | Contrôle des références d'images | Fakeddit | Examiner la disponibilité des URL d'images |
| 4 | Inspection initiale des CSV | FakeNewsNet | Comprendre les fichiers et leurs colonnes |
| 5 | Statistiques descriptives | FakeNewsNet | Mesurer les volumes, valeurs manquantes et doublons |
| 6 | Analyse des URL et identifiants de tweets | FakeNewsNet | Qualifier les références et les données sociales |
| 7 | Inspection du code de collecte | FakeNewsNet | Comprendre l'extraction des articles et images |
| 8 | Inspection du fichier RDF | CIMPLE | Vérifier l'archive et les types de ressources |
| 9 | Analyse des relations RDF | CIMPLE | Comprendre les liens entre ClaimReview, Claim et Rating |
| 10 | Analyse des verdicts et des langues | CIMPLE | Mesurer les distributions |
| 11 | Recherche des propriétés liées aux images | CIMPLE | Examiner les possibilités multimodales |

Le bilan comparatif de cette présente section constitue le douzième élément de synthèse du carnet.

**Important :** les fiches 3, 5, 6 et 10 notamment contiennent des programmes proposés ou reconstruits pour reproduire les analyses. Il faut distinguer les commandes effectivement exécutées des scripts préparés pour une vérification ultérieure.

## 14.4. Architecture de collecte retenue

L'exploration conduit à retenir une architecture reposant sur quatre sources complémentaires.

    SOURCES DE DONNÉES
           |
    +------+----------------+ 
    |      |                |
    v      v                v
 Fakeddit FakeNewsNet  NewsData.io
    |      |                |
    v      v                v
 TSV    CSV + articles  API REST JSON
    |      |                |
    +------+----------------+
           |
           v
    COLLECTE ET NORMALISATION
           |
           v
    PUBLICATIONS STRUCTURÉES
           |
      +----+----+
      |         |
      v         v
 Texte et   Métadonnées
 images        |
      |         |
      +----+----+
           |
           v
    ENRICHISSEMENT CIMPLE
           |
           v
    FACT-CHECK ET VERDICTS
           |
           v
    BASE DE DONNÉES CHECKIT.AI

Cette architecture sépare la collecte des publications, l'extraction des médias et l'enrichissement par les données de fact-checking.

Elle permet également de conserver la provenance de chaque information.

## 14.5. Principes de qualité retenus

Les analyses effectuées conduisent à retenir les règles suivantes pour la future chaîne de traitement :

1. Ne jamais transformer un label absent en label `real`.
2. Conserver le label d'origine et sa source.
3. Préserver l'URL de la publication et celle du fact-checking.
4. Distinguer les contenus faux, trompeurs, incertains et non vérifiables.
5. Ne pas confondre opinion controversée et désinformation factuellement réfutable.
6. Conserver les publications même lorsque leur image ou leur label est manquant.
7. Vérifier que les images sont effectivement associées à la publication.
8. Contrôler l'accessibilité des URL d'images avant de les intégrer au corpus multimodal.
9. Conserver les données brutes sans modification.
10. Documenter les erreurs et les opérations de normalisation.

## 14.6. Recommandations pour la prochaine étape

À la suite de cette exploration, l'ordre de travail recommandé est le suivant :

| Priorité | Travail | Justification |
|---|---|---|
| 1 | Préparer le traitement de Fakeddit | Source multimodale directement exploitable |
| 2 | Concevoir le collecteur FakeNewsNet | Enrichissement nécessaire des articles et images |
| 3 | Préparer l'intégration de CIMPLE | Apport de verdicts de fact-checking |
| 4 | Étudier l'intégration de NewsData.io | Collecte complémentaire, avec contraintes de quota et de licence |
| 5 | Définir les contrôles qualité communs | Assurer la cohérence du corpus final |

Ces travaux devront respecter l'ordre des étapes officielles du projet OpenClassrooms.

Les extracteurs et les traitements de production ne doivent être développés qu'au moment prévu dans le parcours du projet.

## 14.7. Conclusion générale

L'exploration des quatre sources a permis d'identifier des ressources complémentaires pour constituer le corpus multimodal de CheckIt.AI.

Fakeddit constitue la première source multimodale, avec des publications associant texte et références d'images.

FakeNewsNet permet d'enrichir les publications avec leurs articles d'origine et leurs données sociales, sous réserve de réussir la collecte et de respecter les restrictions d'accès.

NewsData.io apporte une possibilité de collecte complémentaire d'actualités via une API structurée, mais ne fournit pas de verdict de fact-checking.

Enfin, CIMPLE Knowledge Graph apporte une structure particulièrement intéressante pour relier les affirmations aux publications de vérification et à leurs verdicts.

La complémentarité de ces sources permet d'envisager une base de données qui associe :

- les contenus textuels ;
- les images explicitement liées aux publications ;
- les métadonnées ;
- les informations de provenance ;
- les verdicts de fact-checking.

La qualité du futur corpus dépendra toutefois de la validation des images, de la fiabilité des labels, de la traçabilité des données et du respect des conditions de réutilisation.

Cette phase d'exploration fournit ainsi les bases nécessaires pour poursuivre le projet CheckIt.AI conformément aux étapes suivantes du parcours OpenClassrooms.

---

*Fin du carnet technique d'exploration des quatre sources.*
