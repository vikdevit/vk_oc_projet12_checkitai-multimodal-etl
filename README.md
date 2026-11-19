# CheckIt.AI — Pipeline ETL multimodal

Projet OpenClassrooms — Parcours AI Engineer
Projet 12 : Extrayez des données multimodales de sites web.

## 1. Objectif

Concevoir un pipeline automatisé de collecte, d'extraction et de
transformation de données textuelles, visuelles et de métadonnées
pour le cas d'usage CheckIt.AI : l'analyse de contenus potentiellement
faux ou trompeurs.

Le projet vise à préparer des données exploitables pour des usages
d'intelligence artificielle, notamment le traitement automatique
du langage (NLP), l'analyse multimodale et la classification.

## 2. Sources de données

| Source | Rôle dans le projet |
|---|---|
| Fakeddit | Source initiale de publications multimodales et de labels |
| FakeNewsNet | Enrichissement avec des métadonnées et des URL d'articles |
| NewsData.io | Collecte complémentaire d'actualités récentes |
| CIMPLE | Enrichissement avec des vérifications factuelles et des verdicts |

Les sources n'apportent pas toutes des images ou des textes intégraux.
Les données manquantes sont conservées comme telles et ne sont pas
remplacées par des valeurs supposées.

## 3. Architecture du projet

- `config/` : paramètres de configuration
- `docs/` : documentation et rapports
- `src/checkitai/extraction/` : connecteurs d'extraction
- `src/checkitai/transformation/` : pipeline de transformation
- `tests/` : tests automatisés
- `diagrams/` : diagrammes conceptuels et techniques
- `schemas/` : schémas de données
- `airflow/` : orchestration prévue
- `dashboard/` : tableau de bord prévu
- `scripts/` : scripts de contrôle et d'exploration
- `presentation/` : présentation finale

Les données sont stockées séparément du dépôt Git dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/`

## 4. Installation

Le projet utilise Python 3.11 et uv pour gérer l'environnement.

Depuis la racine du dépôt :

```bash
uv sync --extra dev
```

Les variables sensibles sont définies dans un fichier `.env`
local, qui n'est pas versionné.

Pour NewsData.io, renseigner notamment :

`NEWSDATA_API_KEY`

Ne jamais publier les clés API dans le dépôt.

## 5. Extraction des données

Les connecteurs Python sont disponibles dans :

`src/checkitai/extraction/`

Ils couvrent les quatre sources présentées précédemment.
Les résultats intermédiaires sont enregistrés au format JSONL
dans le répertoire `interim/`.

Les connecteurs peuvent être exécutés individuellement avec :

```bash
uv run python -m checkitai.extraction.fakeddit --help
uv run python -m checkitai.extraction.fakenewsnet --help
uv run python -m checkitai.extraction.newsdata --help
uv run python -m checkitai.extraction.cimple --help
```

Pour NewsData.io, le fichier `.env` doit contenir une clé API valide.

## 6. Transformation des données

Le pipeline de transformation est disponible dans :

`src/checkitai/transformation/pipeline.py`

Il réalise notamment :
- le nettoyage des espaces dans les champs textuels ;
- la normalisation des dates lorsque cela est possible ;
- la détermination de la présence de texte ;
- la distinction entre image téléchargée, URL seule, image absente
  et image invalide ;
- la catégorisation des labels : binaire, fact-check ou non renseigné ;
- la conservation des métadonnées et de la provenance des sources.

Les fichiers intermédiaires ne sont pas modifiés.

Pour exécuter le pipeline :

```bash
uv run python -m checkitai.transformation.pipeline
```

Les paramètres sont définis dans `config/settings.yaml`.

## 7. Résultats de transformation

Les fichiers transformés sont enregistrés dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/processed/`

Un fichier JSONL est produit pour chaque source :
- `processed/fakeddit/fakeddit_transformed.jsonl`
- `processed/fakenewsnet/fakenewsnet_transformed.jsonl`
- `processed/newsdata/newsdata_transformed.jsonl`
- `processed/cimple/cimple_transformed.jsonl`

Le rapport global est disponible dans :

`reports/transformation/transformation_report.json`

Les journaux d'exécution sont disponibles dans :

`logs/transformation.log`

## 8. Schéma conceptuel

Le diagramme Mermaid est disponible dans :

`diagrams/schema_conceptuel.mmd`

Sa documentation est disponible dans :

`docs/etape3_schema_conceptuel.md`

Le modèle décrit les entités Source, ContentRecord, ImageAsset
et LabelAssessment, ainsi que leurs relations.

L'association entre un contenu et son image repose sur un identifiant
commun `publication_id`. Une image n'est jamais associée à un contenu
sur la seule base de sa proximité dans un fichier.

## 9. Tests

Les tests automatisés sont exécutés avec :

```bash
uv run pytest -v
```

Les tests couvrent notamment la validation des images et les fonctions
principales du pipeline de transformation.

Dernière validation connue : 26 tests réussis.

## 10. Limites et précautions

- Les labels des sources ne représentent pas tous une vérité
  vérifiée indépendamment.
- Les catégories de verdict CIMPLE restent distinctes.
- Une absence de label n'est jamais assimilée à un label positif.
- FakeNewsNet fournit principalement des métadonnées et des URL,
  pas le texte intégral des articles dans ses fichiers CSV.
- Les URL d'images de NewsData.io ne signifient pas que les images
  ont été téléchargées et validées.
- Les données intermédiaires sont conservées pour assurer
  la traçabilité des transformations.

## 11. Statut du projet

Étapes réalisées :
- préparation de l'environnement et du dépôt Git ;
- exploration et qualification des sources ;
- développement et validation des connecteurs d'extraction ;
- développement et tests du pipeline de transformation ;
- création du schéma conceptuel et de sa documentation.

Les étapes suivantes portent notamment sur la modélisation technique,
l'orchestration, le stockage, le suivi des indicateurs et la
documentation finale.
