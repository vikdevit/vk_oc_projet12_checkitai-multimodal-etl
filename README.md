# CheckIt.AI - Extraction de données multimodales

Projet OpenClassrooms - Parcours AI Engineer
Projet 12 : Extrayez des données multimodales de sites web.

## Objectif

Concevoir un pipeline automatisé de collecte, d'extraction,
de transformation et de contrôle qualité de données textuelles
et visuelles pour le cas d'usage CheckIt.AI.

## Architecture

Le projet s'appuie sur Python, des sources de données web,
Apache Airflow et un tableau de bord de suivi.

## Organisation

- `config/` : configuration du projet
- `docs/` : documentation et rapports
- `src/` : code source Python
- `schemas/` : schémas de données
- `airflow/` : orchestration ETL
- `dashboard/` : tableau de bord KPI
- `scripts/` : scripts d'exécution
- `tests/` : tests automatisés
- `diagrams/` : diagrammes d'architecture
- `presentation/` : présentation finale

Les données collectées sont stockées séparément dans
`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/`.

## Statut

Initialisation de l'environnement et de la structure du projet.
