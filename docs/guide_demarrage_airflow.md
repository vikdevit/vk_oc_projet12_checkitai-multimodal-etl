
# Guide de démarrage et d'utilisation d'Apache Airflow

## 1. Présentation

Ce guide décrit la procédure pour démarrer Apache Airflow, accéder à son interface web et lancer le pipeline ETL du projet CheckIt.AI.

L'environnement est installé sur un serveur Ubuntu et utilise un environnement Python virtuel indépendant de celui du projet.

### Architecture utilisée

- **Apache Airflow 3.4.0** : orchestration des traitements.
- **Python 3.11** : exécution des scripts d'extraction et de transformation.
- **uv** : gestion des environnements Python.
- **SQLite** : stockage relationnel des données transformées.
- **SSH** : accès sécurisé au serveur et à l'interface Airflow.

## 2. Démarrage du serveur Airflow

### 2.1. Connexion SSH au serveur

Depuis un terminal sur le poste local :

```bash
ssh vikenserver@192.168.1.26
```

L'adresse IP peut varier selon la configuration du réseau local.

### 2.2. Accéder au répertoire du projet

Sur le serveur :

```bash
cd /mnt/projects/vk_oc_projet12_checkitai-multimodal-etl
```

### 2.3. Configurer l'environnement Airflow

Exécuter les commandes suivantes :

```bash
export AIRFLOW_HOME=/mnt/projects/envs/airflow_home

export AIRFLOW__CORE__DAGS_FOLDER=/mnt/projects/vk_oc_projet12_checkitai-multimodal-etl/airflow/dags

export PATH="/mnt/projects/envs/airflow/bin:$PATH"
```

**Explication :**

- `AIRFLOW_HOME` : définit le répertoire contenant la configuration, les journaux et la base interne d'Airflow.
- `AIRFLOW__CORE__DAGS_FOLDER` : indique à Airflow où trouver les fichiers DAG du projet.
- `PATH` : permet d'utiliser les commandes Airflow installées dans l'environnement virtuel dédié.

### 2.4. Démarrer Airflow en arrière-plan

Exécuter :

```bash
nohup env \
  AIRFLOW_HOME=/mnt/projects/envs/airflow_home \
  AIRFLOW__CORE__DAGS_FOLDER=/mnt/projects/vk_oc_projet12_checkitai-multimodal-etl/airflow/dags \
  AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_USERS="admin:admin,vikenserver:admin" \
  PATH="/mnt/projects/envs/airflow/bin:$PATH" \
  airflow standalone \
  > /mnt/projects/envs/airflow_home/standalone.log 2>&1 &
```

Cette commande démarre Airflow en arrière-plan.

Elle permet de conserver le service actif même après la fermeture de la session SSH utilisée pour son démarrage.

**Important :** cette commande réutilise la configuration d'authentification déjà créée. Elle ne modifie pas le mot de passe SSH du serveur. Le compte Airflow et le compte SSH sont indépendants.

La commande `airflow db migrate` n'a pas besoin d'être exécutée à chaque démarrage. La base interne Airflow a déjà été initialisée.

### 2.5. Vérifier le démarrage

Consulter les dernières lignes du journal :

```bash
tail -n 30 /mnt/projects/envs/airflow_home/standalone.log
```

Vérifier que le serveur répond :

```bash
curl -s http://127.0.0.1:8080/ | head -c 300
```

Vérifier que le DAG est reconnu :

```bash
airflow dags list
```

Le DAG attendu est :

`checkitai_etl_pipeline`

## 3. Accéder à l'interface web depuis le poste local

### 3.1. Créer le tunnel SSH

Depuis un deuxième terminal sur le poste local, et non depuis le terminal du serveur :

```bash
ssh -N -L 8080:127.0.0.1:8080 vikenserver@192.168.1.26
```

**Important :** conserver ce terminal ouvert pendant toute l'utilisation de l'interface Airflow.

Le tunnel SSH permet d'accéder au service Airflow du serveur à travers une connexion sécurisée.

### 3.2. Ouvrir l'interface web

Dans le navigateur du poste local, ouvrir :

[http://localhost:8080](http://localhost:8080)

Se connecter avec le compte Airflow :

- **Utilisateur :** `vikenserver`
- **Mot de passe :** celui généré lors de la configuration initiale d'Airflow.

Ce mot de passe est distinct du mot de passe SSH.

## 4. Lancer le pipeline ETL CheckIt.AI

### 4.1. Identifier le DAG

Dans l'interface Airflow, rechercher :

`checkitai_etl_pipeline`

Vérifier que le DAG est activé.

### 4.2. Déclencher une exécution

1. Cliquer sur le nom du DAG.
2. Cliquer sur **Trigger DAG**.
3. Confirmer le déclenchement si une fenêtre apparaît.
4. Accéder à la vue **Grid** pour suivre l'exécution.

### 4.3. Déroulement du pipeline

Le DAG comporte six tâches :

| Tâche | Fonction |
|---|---|
| `extract_fakeddit` | Extraction des données Fakeddit |
| `extract_fakenewsnet` | Extraction des données FakeNewsNet |
| `extract_newsdata` | Extraction des articles NewsData.io |
| `extract_cimple` | Extraction des vérifications CIMPLE KG |
| `transform_data` | Transformation et normalisation |
| `load_data` | Chargement dans SQLite |

Les quatre extractions sont indépendantes et peuvent s'exécuter en parallèle.

La transformation attend la fin des quatre extractions.

Le chargement dans SQLite intervient ensuite.

### 4.4. Vérifier le succès de l'exécution

Dans la vue **Grid**, vérifier que les six tâches apparaissent en vert.

Un état vert correspond à une tâche terminée avec succès.

En cas d'échec, cliquer sur la tâche concernée pour consulter ses journaux d'exécution.

**Attention :** chaque nouveau déclenchement relance les extractions et peut consommer des crédits de l'API NewsData.io.

## 5. Vérifier les données chargées dans SQLite

### 5.1. Emplacement de la base

La base de données métier est enregistrée dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/processed/checkitai.db`

### 5.2. Lancer le contrôle de la base

Depuis la racine du projet :

```bash
uv run python scripts/controle_bdd_etape4.py
```

### 5.3. Résultats de référence

Lors de la première exécution validée du DAG, les résultats étaient :

| Source | Publications |
|---|---:|
| Fakeddit | 100 |
| FakeNewsNet | 40 |
| NewsData.io | 20 |
| CIMPLE KG | 800 |
| **Total** | **960** |

Les contrôles ont confirmé :

- Intégrité SQLite : `ok`.
- Aucune erreur de clé étrangère.
- 4 sources enregistrées.
- 960 publications chargées.
- 960 enregistrements dans `image_assets`.
- 960 enregistrements dans `label_assessments`.

Les volumes peuvent évoluer lors des exécutions suivantes selon les données récupérées par les connecteurs.

## 6. Comprendre le rôle de SQLite dans CheckIt.AI

SQLite est la base de données relationnelle de destination du pipeline ETL.

Elle conserve les données après leur extraction et leur transformation.

Elle comporte quatre tables principales :

| Table | Rôle |
|---|---|
| `sources` | Référentiel des sources |
| `content_records` | Publications et métadonnées |
| `image_assets` | Informations relatives aux images |
| `label_assessments` | Labels et évaluations |

Les relations sont assurées par des clés primaires et étrangères.

SQLite permet notamment :

- De conserver les données transformées.
- De rechercher les publications.
- De compter les données par source.
- De réaliser des jointures entre les tables.
- De préparer les données pour un futur tableau de bord Streamlit.

**Différence entre Airflow et SQLite :**

- Airflow orchestre les traitements et contrôle leur exécution.
- Python exécute les opérations d'extraction et de transformation.
- SQLite conserve les résultats du pipeline.

Airflow dispose également de sa propre base interne, distincte de la base métier `checkitai.db`.

## 7. Arrêter Airflow

Lorsque le travail est terminé, le service peut être arrêté depuis le serveur.

```bash
pkill -f 'airflow standalone'
```

Cette commande arrête le processus Airflow.

La fermeture du navigateur ou du tunnel SSH ne suffit pas à arrêter le service.

**Attention :** ne pas utiliser cette commande si une exécution du DAG est encore en cours.

## 8. Informations importantes

- L'environnement Airflow est indépendant de l'environnement Python du projet.
- Les fichiers de données et la base SQLite sont stockés dans `/mnt/data`.
- Le code source et l'environnement virtuel sont stockés dans `/mnt/projects`.
- Les clés API sont conservées dans le fichier `.env`, qui ne doit jamais être versionné.
- La base SQLite est protégée par des permissions Unix `600`.
- SQLite ne fournit pas de gestion native des utilisateurs et des rôles ni de chiffrement natif.
- Cette installation est destinée à une utilisation locale et pédagogique, pas à un déploiement de production.

---

**Projet :** CheckIt.AI — Détection de fausses informations à partir de données multimodales.

**Orchestration :** Apache Airflow 3.4.0.

**Stockage :** SQLite.

**Étape OpenClassrooms :** Étape 4 — Orchestrez le pipeline avec Airflow.

