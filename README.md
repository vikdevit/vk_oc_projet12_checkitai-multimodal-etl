
# CheckIt.AI — Pipeline ETL multimodal

**Projet OpenClassrooms — Parcours AI Engineer**
**Projet 12 : Extrayez des données multimodales de sites web**

## 1. Présentation du projet

CheckIt.AI est un projet de collecte, d'extraction et de transformation de données multimodales destiné à préparer des données exploitables pour l'analyse de contenus potentiellement faux ou trompeurs.

L'objectif est de construire un pipeline ETL automatisé capable de collecter des données textuelles, visuelles et des métadonnées provenant de plusieurs sources, de les transformer, puis de les stocker dans une base relationnelle.

Les données préparées pourront notamment servir à de futurs travaux de traitement automatique du langage (NLP), d'analyse multimodale et de classification.

## 2. Sources de données

| Source | Rôle dans le projet |
|---|---|
| Fakeddit | Publications multimodales, textes, URL d'images et labels |
| FakeNewsNet | Métadonnées d'articles et URL de publications |
| NewsData.io | Collecte complémentaire d'actualités |
| CIMPLE KG | Enrichissement avec des vérifications factuelles et des verdicts |

Les sources ne fournissent pas toutes des images ou des textes intégraux. Les données manquantes sont conservées comme telles et ne sont pas remplacées par des valeurs supposées.

Les labels d'origine doivent être interprétés selon leur provenance : ils ne représentent pas tous une vérité vérifiée indépendamment.

## 3. Architecture générale

Le pipeline est organisé en plusieurs composants :

1. **Extraction** : collecte des données auprès des quatre sources.
2. **Transformation** : nettoyage, normalisation et enrichissement des données.
3. **Orchestration** : exécution automatisée des étapes avec Apache Airflow.
4. **Stockage** : chargement des données transformées dans SQLite.
5. **Visualisation et suivi** : consultation des indicateurs avec Streamlit.

### Technologies utilisées

| Composant | Technologie |
|---|---|
| Langage | Python 3.11 |
| Gestion des dépendances | uv |
| Extraction HTTP et API | Requests |
| Manipulation des données | Pandas |
| Transformation | Python |
| Orchestration | Apache Airflow 3.4.0 |
| Stockage relationnel | SQLite |
| Dashboard | Streamlit |
| Visualisation | Plotly |
| Tests | Pytest |
| Qualité du code | Ruff |

### Organisation du dépôt

- `config/` : paramètres de configuration.
- `src/checkitai/extraction/` : connecteurs des quatre sources.
- `src/checkitai/transformation/` : pipeline de transformation.
- `src/checkitai/storage/` : stockage SQLite.
- `airflow/dags/` : DAG d'orchestration.
- `dashboard/` : application Streamlit.
- `docs/` : documentation technique et rapports.
- `diagrams/` : diagrammes conceptuels.
- `schemas/` : schémas de données.
- `scripts/` : scripts de contrôle et d'exploration.
- `tests/` : tests automatisés.

Les données et les bases générées sont stockées en dehors du dépôt Git, dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/`

## 4. Installation de l'environnement du projet

Le projet nécessite Python 3.11 ou une version compatible avec la contrainte définie dans `pyproject.toml`.

Installer les dépendances depuis la racine du dépôt :

```bash
uv sync --extra dev
```

Cette commande installe les dépendances du projet et les outils de développement.

Le fichier `uv.lock` permet de conserver une résolution cohérente des dépendances.

### Configuration des variables sensibles

Les variables sensibles sont définies dans un fichier `.env` local, qui ne doit jamais être versionné.

Pour utiliser NewsData.io, renseigner notamment :

```env
NEWSDATA_API_KEY=votre_cle_api
```

Ne jamais publier une clé API ou un secret dans le dépôt Git.

**Important :** Apache Airflow est installé dans un environnement Python indépendant de celui du projet. Sa procédure d'installation et de démarrage est décrite dans le guide dédié.

## 5. Extraction des données

Les connecteurs Python sont disponibles dans :

`src/checkitai/extraction/`

Chaque source possède son propre module :

```bash
uv run python -m checkitai.extraction.fakeddit --help
uv run python -m checkitai.extraction.fakenewsnet --help
uv run python -m checkitai.extraction.newsdata --help
uv run python -m checkitai.extraction.cimple --help
```

Les résultats intermédiaires sont enregistrés au format JSONL dans le répertoire `interim/`.

Les connecteurs produisent également des rapports d'extraction et des journaux permettant de suivre les traitements.

NewsData.io nécessite une clé API valide dans le fichier `.env`.

## 6. Transformation des données

Le pipeline de transformation est disponible dans :

`src/checkitai/transformation/pipeline.py`

Il réalise notamment :

- Le nettoyage des champs textuels.
- La normalisation des dates lorsque cela est possible.
- La détermination de la présence de texte.
- La distinction entre image téléchargée, URL seule, image absente et image invalide.
- La catégorisation des labels : binaire, fact-check ou non renseigné.
- La conservation des métadonnées et de la provenance des sources.

Les fichiers intermédiaires ne sont pas modifiés.

Exécuter la transformation :

```bash
uv run python -m checkitai.transformation.pipeline
```

Les paramètres sont définis dans `config/settings.yaml`.

Les données transformées sont enregistrées dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/processed/`

Le rapport global est disponible dans :

`reports/transformation/transformation_report.json`

Les journaux sont disponibles dans :

`logs/transformation.log`

## 7. Orchestration avec Apache Airflow

Le DAG d'orchestration est disponible dans :

`airflow/dags/checkitai_etl_dag.py`

Son identifiant est :

`checkitai_etl_pipeline`

Il comporte six tâches :

| Tâche | Fonction |
|---|---|
| `extract_fakeddit` | Extraction Fakeddit |
| `extract_fakenewsnet` | Extraction FakeNewsNet |
| `extract_newsdata` | Extraction NewsData.io |
| `extract_cimple` | Extraction CIMPLE KG |
| `transform_data` | Transformation des données |
| `load_data` | Chargement dans SQLite |

Les quatre tâches d'extraction sont indépendantes et peuvent s'exécuter en parallèle. La transformation attend leur achèvement, puis le chargement SQLite intervient en dernier.

Le DAG est déclenché manuellement dans le cadre de cette installation pédagogique.

### Démarrage et utilisation

Le guide détaillé décrit :

- La configuration de l'environnement Airflow.
- Le démarrage du service.
- L'accès à l'interface web par tunnel SSH.
- Le déclenchement du DAG.
- Le contrôle des tâches et de leurs journaux.

Consulter : [Guide de démarrage et d'utilisation d'Airflow](docs/guide_demarrage_airflow.md).

La documentation technique du DAG est disponible dans [docs/etape4_airflow.md](docs/etape4_airflow.md).

## 8. Stockage des données avec SQLite

La base métier est enregistrée dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/processed/checkitai.db`

Elle comporte quatre tables principales :

| Table | Rôle |
|---|---|
| `sources` | Référentiel des sources |
| `content_records` | Publications et métadonnées |
| `image_assets` | Informations relatives aux images |
| `label_assessments` | Labels et évaluations |

Le chargement utilise des transactions et des opérations d'insertion ou de mise à jour afin de limiter les doublons lors des exécutions successives.

Un script de contrôle est disponible :

```bash
uv run python scripts/controle_bdd_etape4.py
```

La base métier SQLite est distincte de la base interne utilisée par Airflow.

## 9. Tableau de bord Streamlit

Le tableau de bord est disponible dans :

`dashboard/app.py`

Il permet de consulter les indicateurs principaux du pipeline :

- Volumétrie des données par source.
- Présence des données textuelles.
- Disponibilité des URL d'images.
- État des images téléchargées.
- Informations relatives au stockage SQLite.
- Résultats et durées des exécutions Airflow.
- Durées des différentes tâches du DAG.
- Historique des exécutions.

### Démarrer le dashboard

Depuis la racine du projet :

```bash
uv run streamlit run dashboard/app.py \
  --server.address 127.0.0.1 \
  --server.port 8501
```

Depuis le poste local, créer un tunnel SSH vers le serveur :

```bash
ssh -N -L 8501:127.0.0.1:8501 vikenserver@ADRESSE_IP_DU_SERVEUR
```

Puis ouvrir dans le navigateur :

`http://localhost:8501`

Le dashboard utilise la base métier SQLite et la base interne d'Airflow pour afficher les indicateurs correspondants.

## 10. Tests et qualité du code

Les tests automatisés sont exécutés avec :

```bash
make test
```

Ou directement :

```bash
uv run pytest -v
```

La qualité du code peut être contrôlée avec :

```bash
make lint
```

Le formatage est disponible avec :

```bash
make format
```

Les tests couvrent notamment la validation des images et les fonctions principales du pipeline de transformation.

Dernière validation connue : **26 tests réussis**.

## 11. Monitoring et suivi du pipeline

Le plan de monitoring décrit les indicateurs, les seuils d'alerte, les fréquences de contrôle et les procédures de reprise.

Il couvre notamment :

- Les échecs des tâches Airflow.
- La durée des exécutions.
- Les taux de rejet des données.
- La complétude des champs textuels.
- L'espace disque disponible.
- L'intégrité de la base SQLite.

Consulter : [Plan de monitoring ETL](docs/etape5_plan_monitoring_etl.md).

Les indicateurs sont consultables dans le dashboard Streamlit. Les notifications externes automatiques ne sont pas configurées dans cette version.

## 12. Schéma conceptuel

Le diagramme Mermaid est disponible dans :

`diagrams/schema_conceptuel.mmd`

Sa documentation est disponible dans [docs/etape3_schema_conceptuel.md](docs/etape3_schema_conceptuel.md).

Le modèle décrit les entités `Source`, `ContentRecord`, `ImageAsset` et `LabelAssessment`, ainsi que leurs relations.

L'association entre un contenu et son image repose sur un identifiant commun `publication_id`. Une image n'est jamais associée à un contenu sur la seule base de sa proximité dans un fichier.

## 13. Limites et précautions

- Les labels des sources ne représentent pas tous une vérité vérifiée indépendamment.
- Les catégories de verdict CIMPLE restent distinctes.
- Une absence de label n'est jamais assimilée à un label positif.
- FakeNewsNet fournit principalement des métadonnées et des URL, pas le texte intégral des articles dans ses fichiers CSV.
- Une URL d'image ne signifie pas que l'image a été téléchargée et validée.
- Les volumes peuvent évoluer selon les données récupérées lors des exécutions successives.
- L'installation Airflow et le stockage SQLite sont destinés à un environnement pédagogique local, et non à un déploiement de production.
- SQLite ne fournit pas de gestion native des utilisateurs et des rôles ni de chiffrement natif.

## 14. Documentation complémentaire

| Document | Contenu |
|---|---|
| [Rapport d'exploration des sources](docs/etape1_rapport_exploration_sources.md) | Analyse et qualification des sources |
| [Carnet technique d'exploration](docs/etape1_carnet_technique_scripts_exploration.md) | Scripts et explorations |
| [Schéma conceptuel](docs/etape3_schema_conceptuel.md) | Modèle de données |
| [Documentation Airflow](docs/etape4_airflow.md) | Orchestration ETL |
| [Guide de démarrage Airflow](docs/guide_demarrage_airflow.md) | Installation et utilisation |
| [Plan de monitoring](docs/etape5_plan_monitoring_etl.md) | KPI, seuils et surveillance |

## 15. Statut du projet

Les étapes suivantes ont été réalisées :

- Préparation de l'environnement et du dépôt Git.
- Exploration et qualification des sources.
- Développement et validation des connecteurs d'extraction.
- Développement et tests du pipeline de transformation.
- Création du schéma conceptuel.
- Orchestration du pipeline avec Apache Airflow.
- Chargement des données dans SQLite.
- Création du tableau de bord KPI avec Streamlit.
- Rédaction du plan de monitoring ETL.

Le projet dispose ainsi d'un pipeline ETL multimodal fonctionnel, de son stockage, de son orchestration et d'outils de suivi.

---

**Projet :** CheckIt.AI — Pipeline ETL multimodal
**Formation :** OpenClassrooms — Parcours AI Engineer
**Projet :** 12 — Extraction de données multimodales
