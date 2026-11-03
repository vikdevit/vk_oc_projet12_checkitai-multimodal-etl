# CHECKIT.AI
## Rapport d'exploration et de qualification des sources de données multimodales

**Projet :** OpenClassrooms – Projet 12  
**Intitulé :** Extrayez des données multimodales de sites web  
**Domaine :** Intelligence artificielle – Détection de la désinformation  
**Livrable :** Étape 1 – Exploration et qualification des sources  
**Version :** 1.0  
**Date :** 3 novembre 2026  
**Statut :** Rapport d'exploration technique et documentaire

---

# Résumé exécutif

## Contexte

CheckIt.AI est un projet de pipeline de collecte et de préparation de données destiné à contribuer à la détection de fausses informations à partir de contenus multimodaux publiés sur le Web.

La désinformation contemporaine ne se limite pas aux textes. Elle peut associer des titres trompeurs, des articles, des photographies sorties de leur contexte, des images manipulées ou des vidéos dont le contenu ne correspond pas au message diffusé.

L'objectif du projet est donc d'identifier, d'explorer et de qualifier des sources de données permettant de constituer un corpus associant, autant que possible, le texte, les médias et les informations de vérification.

## Objectifs de cette étude

Cette première étape vise à :

- identifier plusieurs sources pertinentes de données textuelles et multimodales ;
- examiner les formats et les structures des données disponibles ;
- identifier les langues représentées ;
- analyser la nature et la fiabilité des labels ;
- étudier les possibilités et les contraintes d'extraction ;
- examiner les conditions d'utilisation et de redistribution ;
- définir un modèle de données cible ;
- recommander une stratégie de collecte adaptée à CheckIt.AI.

## Sources étudiées

Quatre sources ont été retenues pour cette exploration :

| Source | Fonction principale dans CheckIt.AI |
|---|---|
| Fakeddit | Constitution d'un corpus initial de publications textuelles et visuelles annotées |
| FakeNewsNet | Enrichissement à partir d'articles de presse et de données sociales associées |
| NewsData.io | Collecte complémentaire d'actualités et de métadonnées par API |
| CIMPLE Knowledge Graph | Enrichissement des publications par des informations de fact-checking et des verdicts structurés |

Ces sources répondent à des besoins différents. Elles ne doivent donc pas être considérées comme quatre jeux de données équivalents ou directement fusionnables.

## Principaux enseignements

L'exploration met en évidence plusieurs constats :

- Fakeddit fournit un volume important de publications associant texte et références d'images, avec plusieurs niveaux d'annotation.
- FakeNewsNet permet de relier des articles à des catégories de vérification et à des identifiants de publications sociales, mais nécessite une collecte complémentaire des contenus.
- NewsData.io offre une interface API structurée pour découvrir des actualités et leurs métadonnées, avec des limitations dépendant de l'abonnement.
- CIMPLE apporte des informations de fact-checking structurées, mais ne constitue pas, dans l'archive analysée, une source directe d'images.

L'étude souligne également qu'un label disponible dans un dataset ne constitue pas nécessairement une vérité terrain indépendante. La provenance, la méthode d'annotation et le degré d'incertitude doivent être conservés.

## Orientation retenue

La stratégie recommandée consiste à combiner les sources de manière complémentaire :

- Fakeddit pour l'apprentissage multimodal initial ;
- FakeNewsNet pour l'enrichissement éditorial et social ;
- NewsData.io pour la collecte complémentaire d'actualités ;
- CIMPLE pour les informations de vérification factuelle.

La constitution du corpus devra reposer sur une architecture de conservation des données brutes, de normalisation et de qualification, afin de préserver la traçabilité de chaque publication et de ses médias.

---

# Sommaire

1. [Introduction et contexte du projet](#1-introduction-et-contexte-du-projet)
2. [Problématique de la désinformation multimodale](#2-problématique-de-la-désinformation-multimodale)
3. [Méthodologie de recherche et critères de sélection](#3-méthodologie-de-recherche-et-critères-de-sélection)
4. [Étude détaillée des sources](#4-étude-détaillée-des-sources)
   - [4.1 Fakeddit](#41-fakeddit)
   - [4.2 FakeNewsNet](#42-fakenewsnet)
   - [4.3 NewsData.io](#43-newsdataio)
   - [4.4 CIMPLE Knowledge Graph](#44-cimple-knowledge-graph)
5. [Analyse comparative des sources](#5-analyse-comparative-des-sources)
6. [Évaluation de la qualité et de la fiabilité des labels](#6-évaluation-de-la-qualité-et-de-la-fiabilité-des-labels)
7. [Formats et méthodes d'extraction envisagés](#7-formats-et-méthodes-dextraction-envisagés)
8. [Droits d'utilisation, confidentialité et conformité](#8-droits-dutilisation-confidentialité-et-conformité)
9. [Modèle de données cible](#9-modèle-de-données-cible)
10. [Architecture de collecte recommandée](#10-architecture-de-collecte-recommandée)
11. [Risques identifiés et mesures de maîtrise](#11-risques-identifiés-et-mesures-de-maîtrise)
12. [Recommandations et stratégie de mise en œuvre](#12-recommandations-et-stratégie-de-mise-en-œuvre)
13. [Conclusion générale](#13-conclusion-générale)
14. [Bibliographie et ressources documentaires](#14-bibliographie-et-ressources-documentaires)
15. [Annexes techniques](#15-annexes-techniques)

---

# 1. Introduction et contexte du projet

## 1.1 Présentation de CheckIt.AI

CheckIt.AI s'inscrit dans le domaine de la lutte contre la désinformation en ligne. Le projet vise à concevoir une chaîne de traitement de données capable de collecter, structurer et préparer des publications provenant de différentes sources Web.

La finalité est de disposer d'un corpus exploitable par des méthodes d'intelligence artificielle pour étudier les relations entre les contenus textuels, les médias associés et les informations de vérification.

Le périmètre de cette première étape est volontairement centré sur l'exploration des sources. Il ne s'agit pas encore de développer les extracteurs définitifs ni d'entraîner un modèle de classification.

## 1.2 Objectifs fonctionnels

Le futur pipeline devra notamment permettre de :

- collecter des publications depuis des sources hétérogènes ;
- récupérer les textes et les médias associés lorsqu'ils sont accessibles ;
- conserver les dates, les URL et les informations de provenance ;
- associer les labels à leur source de vérification ;
- détecter les données manquantes, invalides ou incohérentes ;
- normaliser les données dans un schéma commun ;
- conserver les éléments nécessaires à la traçabilité et à l'audit.

## 1.3 Périmètre de l'étude

L'exploration porte sur quatre sources complémentaires :

1. un dataset multimodal annoté ;
2. un corpus de publications et d'articles associés à des évaluations ;
3. une API d'actualités ;
4. un graphe de connaissances dédié au fact-checking.

Les critères d'analyse comprennent la disponibilité des textes et des images, les formats, les langues, les labels, les méthodes d'accès, les contraintes techniques et les conditions d'utilisation.

---

# 2. Problématique de la désinformation multimodale

## 2.1 Définition et enjeux

La désinformation désigne la diffusion intentionnelle d'informations fausses ou trompeuses dans le but d'induire un public en erreur. Elle doit être distinguée de la mésinformation, qui correspond à la diffusion d'une information incorrecte sans intention nécessaire de tromper.

Cette distinction est importante pour la constitution d'un corpus d'apprentissage : un contenu factuellement incorrect ne permet pas, à lui seul, de déterminer l'intention de son auteur.

De même, une opinion controversée, une interprétation politique ou une affirmation subjective ne doivent pas être automatiquement classées comme fausses.

## 2.2 Pourquoi une approche multimodale ?

Une publication en ligne peut associer plusieurs modalités :

- **Texte :** titre, description, article, légende ou commentaire.
- **Image :** photographie, illustration, capture d'écran ou infographie.
- **Vidéo :** séquence audiovisuelle, extrait ou contenu réutilisé hors contexte.
- **Métadonnées :** date, auteur, domaine, URL, langue et informations de publication.
- **Données de vérification :** verdict, organisation évaluatrice et URL du fact-check.

L'analyse d'une seule modalité peut être insuffisante. Une photographie authentique peut être associée à un texte trompeur ; inversement, un texte exact peut accompagner une image ancienne ou provenant d'un autre événement.

L'association entre les modalités constitue donc un enjeu central du projet.

## 2.3 Cas typiques à prendre en compte

| Situation | Risque identifié | Données nécessaires |
|---|---|---|
| Image authentique associée à un événement différent | Image sortie de son contexte | Texte, image, date et provenance |
| Photographie manipulée accompagnée d'une affirmation | Altération du média | Image originale, texte et vérification |
| Titre trompeur associé à un article nuancé | Discordance entre titre et contenu | Titre et texte intégral |
| Ancienne vidéo présentée comme récente | Fausse contextualisation temporelle | Vidéo, date et contexte |
| Capture d'écran d'une publication inventée | Faux contenu attribué à une source | Image, texte et source originale |

## 2.4 Conséquences sur la collecte

La collecte doit préserver les relations entre les éléments d'une même publication.

Une image ne doit pas être associée à un article uniquement parce qu'elle apparaît quelque part sur la même page Web. Son rôle et son association avec la publication doivent être vérifiés.

Chaque élément collecté devra ainsi conserver une provenance identifiable et un lien explicite avec la publication correspondante.

---

# 3. Méthodologie de recherche et critères de sélection

## 3.1 Démarche suivie

La recherche a été organisée autour de quatre familles de ressources :

- datasets académiques et communautaires ;
- dépôts de données et de code ;
- API d'actualités ;
- graphes de connaissances et ressources de fact-checking.

Les ressources étudiées ont été examinées à partir de leurs documentations officielles, de leurs fichiers descriptifs, de leurs schémas de données et, lorsque cela était possible, d'un échantillon ou d'une archive téléchargée.

L'objectif n'était pas uniquement de repérer des sources prometteuses, mais aussi d'identifier leurs limites avant toute décision d'intégration.

## 3.2 Critères de sélection

| Critère | Question d'évaluation |
|---|---|
| Pertinence fonctionnelle | La source contribue-t-elle à la détection de la désinformation ? |
| Disponibilité du texte | Le titre et le contenu de la publication sont-ils accessibles ? |
| Disponibilité des médias | Les images ou vidéos sont-elles fournies ou récupérables ? |
| Association des modalités | Le média est-il explicitement relié à la publication ? |
| Qualité des labels | Le verdict est-il documenté et traçable ? |
| Diversité linguistique | Quelles langues sont réellement disponibles ? |
| Métadonnées | Les dates, auteurs, domaines et URL sont-ils présents ? |
| Accessibilité technique | Existe-t-il une API, une archive ou une méthode de collecte documentée ? |
| Pérennité | Les ressources sont-elles maintenues et accessibles ? |
| Droits d'utilisation | Les conditions d'accès, d'utilisation et de redistribution sont-elles définies ? |

## 3.3 Méthodes de qualification

Trois niveaux de preuve sont distingués dans ce rapport :

- **Information documentaire :** caractéristique annoncée par le fournisseur ou la documentation officielle.
- **Résultat observé :** valeur effectivement mesurée lors de l'inspection d'un fichier ou d'une réponse.
- **Recommandation :** choix technique proposé pour la future architecture CheckIt.AI.

Cette distinction évite de confondre une caractéristique annoncée, une observation limitée à un échantillon et une conclusion générale.

## 3.4 Environnement d'exploration

Les opérations de vérification et de préparation ont été réalisées sur un serveur Ubuntu distant.

L'environnement permet de séparer les fichiers de code et les environnements Python des données collectées.

Les caractéristiques détaillées de l'environnement et les empreintes des archives utilisées seront documentées dans les annexes techniques.

## 3.5 Limites méthodologiques

L'exploration ne constitue pas une validation exhaustive de l'ensemble des données des quatre fournisseurs.

Les résultats quantitatifs doivent être interprétés selon leur périmètre exact : fichier téléchargé, version du dataset, échantillon étudié ou caractéristiques annoncées par le fournisseur.

L'accessibilité d'une URL ne garantit pas la disponibilité permanente d'un contenu. De même, un label fourni par une source ne garantit pas une vérité terrain indépendante.

# 4. Étude détaillée des sources

## 4.1 Fakeddit

### 4.1.1 Présentation générale

Fakeddit est un dataset de recherche consacré à la détection de fausses informations à partir de publications issues de Reddit.

Le dataset a été présenté dans l'article scientifique :

**Nakamura, K., Levy, S. et Yang Wang, W. (2020).**  
*r/Fakeddit: A New Multimodal Benchmark Dataset for Fine-grained Fake News Detection.*

Ressources officielles :

- Site du projet : https://fakeddit.netlify.app/
- Dépôt GitHub : https://github.com/entitize/Fakeddit
- Article scientifique : https://arxiv.org/abs/1911.03854

Fakeddit est particulièrement pertinent pour CheckIt.AI, car il propose des publications associant des informations textuelles, des références d'images et des annotations à plusieurs niveaux de granularité.

### 4.1.2 Nature et structure des données

Les fichiers téléchargés sont principalement au format TSV (Tab-Separated Values).

Le fichier étudié dans cette exploration est :

`multimodal_train.tsv`

Il contient 564 000 lignes de données et 16 colonnes.

Les principaux champs identifiés sont :

| Champ | Description | Utilité pour CheckIt.AI |
|---|---|---|
| `author` | Auteur de la publication | Provenance |
| `clean_title` | Titre nettoyé | Texte d'entrée |
| `created_utc` | Horodatage de publication | Temporalité |
| `domain` | Domaine d'origine | Provenance |
| `hasImage` | Indicateur de présence d'image | Contrôle multimodal |
| `id` | Identifiant de publication | Identification |
| `image_url` | URL de l'image associée | Récupération du média |
| `linked_submission_id` | Identifiant de publication liée | Relation entre données |
| `num_comments` | Nombre de commentaires | Métadonnée sociale |
| `score` | Score de la publication | Métadonnée sociale |
| `subreddit` | Communauté Reddit | Contexte |
| `title` | Titre original | Texte d'entrée |
| `upvote_ratio` | Ratio de votes positifs | Métadonnée sociale |
| `2_way_label` | Classification binaire | Annotation |
| `3_way_label` | Classification en trois catégories | Annotation |
| `6_way_label` | Classification fine en six catégories | Annotation |

### 4.1.3 Résultats de l'inspection du fichier

L'inspection du fichier `multimodal_train.tsv` a permis d'obtenir les résultats suivants.

| Indicateur | Résultat |
|---|---:|
| Nombre de publications | 564 000 |
| Nombre de colonnes | 16 |
| Titres originaux manquants | 0 |
| Titres nettoyés manquants | 0 |
| URL d'images manquantes | 1 534 |
| URL d'images renseignées | 562 466 |
| Part des URL d'images renseignées | 99,73 % |

Une incohérence a été observée : le champ `hasImage` indique `True` pour les 564 000 publications, alors que 1 534 lignes ne possèdent pas de valeur `image_url`.

Cette situation démontre qu'un indicateur de présence ne suffit pas à garantir la disponibilité effective d'un média.

Une validation complémentaire des URL et des fichiers images sera donc nécessaire lors d'une future phase d'extraction.

### 4.1.4 Analyse des labels

Fakeddit propose trois niveaux de classification.

**Classification binaire (`2_way_label`)**

| Valeur | Signification | Effectif | Part |
|---|---|---:|---:|
| 0 | Fake | 341 919 | 60,62 % |
| 1 | True | 222 081 | 39,38 % |

**Classification en trois catégories (`3_way_label`)**

| Valeur | Signification | Effectif |
|---|---|---:|
| 0 | Fake with false text | 222 081 |
| 1 | Fake with true text | 13 848 |
| 2 | True | 328 071 |

**Classification en six catégories (`6_way_label`)**

| Valeur | Signification | Effectif |
|---|---|---:|
| 0 | True | 222 081 |
| 1 | Satire/Parody | 33 481 |
| 2 | Misleading Content | 107 221 |
| 3 | Imposter Content | 11 784 |
| 4 | False Connection | 167 857 |
| 5 | Manipulated Content | 21 576 |

La classification fine permet de distinguer plusieurs formes de contenu trompeur, ce qui est particulièrement intéressant pour une approche multimodale.

Cependant, les classes sont déséquilibrées. La catégorie `Imposter Content`, par exemple, représente environ 2,09 % des observations en classification à six catégories.

Pour une future évaluation des modèles, il sera donc préférable de ne pas se limiter à l'accuracy. Des indicateurs comme le macro-F1, le rappel par classe et la matrice de confusion devront être étudiés.

### 4.1.5 Qualité et fiabilité des annotations

Les annotations de Fakeddit reposent sur une approche de supervision indirecte (*distant supervision*) utilisant notamment les catégories de communautés Reddit.

Elles ne correspondent donc pas systématiquement à une vérification factuelle individuelle de chaque publication.

L'article scientifique rapporte également une évaluation humaine sur un échantillon de 150 paires texte-image, avec un coefficient kappa de Cohen d'environ 0,54.

Ce résultat doit inciter à considérer les labels comme des annotations utiles mais potentiellement bruitées.

Ils ne permettent pas, à eux seuls, de démontrer l'intention de tromper de l'auteur.

### 4.1.6 Méthode d'extraction envisagée

La méthode recommandée repose sur les étapes suivantes :

1. Télécharger les fichiers TSV depuis les ressources officielles.
2. Lire les fichiers en conservant les valeurs et les identifiants d'origine.
3. Contrôler les champs obligatoires et les valeurs manquantes.
4. Récupérer les images à partir des URL disponibles, lorsque les conditions d'accès le permettent.
5. Vérifier le statut HTTP, le type MIME et l'intégrité des fichiers téléchargés.
6. Associer chaque image à l'identifiant de sa publication.
7. Conserver les données originales et les informations de provenance.

Outils Python envisagés :

- `pandas` pour la lecture et l'analyse des fichiers TSV ;
- `requests` pour les requêtes HTTP ;
- `Pillow` pour contrôler les fichiers images ;
- `hashlib` pour identifier les doublons éventuels.

Selenium n'est pas nécessaire pour l'accès aux fichiers TSV et aux images directement accessibles par URL.

### 4.1.7 Limites et précautions

Plusieurs limites doivent être prises en compte :

- dépendance à une plateforme communautaire ;
- labels issus d'une supervision indirecte ;
- déséquilibre des catégories ;
- disponibilité non garantie des images ;
- droits de réutilisation à vérifier ;
- absence de garantie que les images soient toujours contextualisées correctement.

La fiche de ressources LREC indique que la licence n'est pas spécifiée. Il convient donc de ne pas considérer automatiquement l'ensemble des contenus comme librement redistribuable.

Les consignes du challenge Fakeddit doivent également être distinguées des usages de recherche généraux, notamment concernant les colonnes autorisées et la recherche de labels externes.

### 4.1.8 Évaluation pour CheckIt.AI

**Décision : source retenue comme candidat principal pour le corpus multimodal initial.**

Fakeddit présente un intérêt élevé grâce à la disponibilité conjointe du texte, des références d'images et des annotations.

Son utilisation devra toutefois intégrer une validation des médias, une analyse du déséquilibre des classes et une documentation explicite de la qualité des labels.

## 4.2 FakeNewsNet

### 4.2.1 Présentation générale

FakeNewsNet est un projet de recherche consacré à l'analyse de la désinformation en combinant des informations issues de sites d'actualité et des données provenant des réseaux sociaux.

Le dépôt officiel est disponible à l'adresse suivante :

https://github.com/KaiDMML/FakeNewsNet

Le projet s'appuie notamment sur deux plateformes de vérification :

- PolitiFact ;
- GossipCop.

Les données sont réparties en catégories fake et real pour chacune de ces plateformes.

FakeNewsNet est intéressant pour CheckIt.AI, car il permet d'étudier les relations entre les articles, leurs titres, leurs URL et les publications sociales associées.

### 4.2.2 Structure des données disponibles

L'inspection du dossier `dataset/` du dépôt officiel a permis d'identifier quatre fichiers :

| Fichier | Catégorie |
|---|---|
| `gossipcop_fake.csv` | Publications classées fake par GossipCop |
| `gossipcop_real.csv` | Publications classées real par GossipCop |
| `politifact_fake.csv` | Publications classées fake par PolitiFact |
| `politifact_real.csv` | Publications classées real par PolitiFact |

Les quatre fichiers utilisent une structure commune de quatre colonnes :

| Champ | Description | Utilité pour CheckIt.AI |
|---|---|---|
| `id` | Identifiant de la publication | Identification |
| `news_url` | URL de l'article original | Collecte complémentaire |
| `title` | Titre de l'article | Donnée textuelle |
| `tweet_ids` | Identifiants des tweets associés | Données sociales et traçabilité |

Les identifiants de tweets sont stockés sous forme de valeurs séparées par des espaces ou des tabulations selon les lignes observées. Ils doivent être interprétés comme une liste d'identifiants et non comme un texte éditorial.

Une anomalie potentielle a également été observée dans certaines URL : quelques valeurs ne comportent pas de protocole explicite (`http://` ou `https://`). Il conviendra de conserver la valeur originale et de normaliser l'URL dans un champ distinct.

### 4.2.3 Disponibilité des contenus

Les fichiers CSV constituent une version minimale du dataset.

Ils ne fournissent pas directement, dans leur structure principale, le corps complet des articles ni les fichiers images.

Ces informations doivent être récupérées à partir des pages des éditeurs lorsque celles-ci sont encore accessibles.

Le dépôt propose des scripts de collecte permettant notamment de récupérer les contenus éditoriaux et les informations sociales.

Le collecteur d'articles s'appuie sur `newspaper` pour extraire plusieurs éléments :

- titre ;
- texte de l'article ;
- URL canonique ;
- auteurs ;
- date de publication ;
- URL des images ;
- métadonnées de la page ;
- résumé et mots-clés éventuels.

Les images sont principalement référencées par des URL. Leur téléchargement et leur validation constituent donc une opération complémentaire.

### 4.2.4 Structure des labels

Les catégories fake et real sont déterminées par le fichier d'origine.

La valeur du label doit donc être associée explicitement à la provenance :

| Fichier | Label conservé | Source de classification |
|---|---|---|
| `gossipcop_fake.csv` | fake | GossipCop |
| `gossipcop_real.csv` | real | GossipCop |
| `politifact_fake.csv` | fake | PolitiFact |
| `politifact_real.csv` | real | PolitiFact |

Il est recommandé de créer des champs distincts pour le label, la plateforme de vérification et l'URL de référence.

Cette approche évite de perdre l'information sur l'origine de la classification lors de la fusion des fichiers.

Ces labels constituent des évaluations issues de plateformes de fact-checking. Ils ne doivent toutefois pas être interprétés comme une mesure universelle de la vérité ou de l'intention de l'auteur.

### 4.2.5 Architecture de collecte proposée par le dépôt

L'analyse du code source a mis en évidence plusieurs composants :

- chargement des fichiers CSV ;
- construction des objets représentant les articles ;
- récupération du contenu des pages Web ;
- collecte des publications Twitter ;
- collecte éventuelle des retweets et des profils utilisateurs ;
- utilisation d'un fichier de configuration.

Le collecteur d'articles utilise notamment `newspaper.Article` pour télécharger et analyser les pages éditoriales.

Il prévoit également un recours à la Wayback Machine lorsque l'URL originale ne permet plus de récupérer le contenu.

Cette stratégie peut améliorer la récupération de contenus historiques, mais elle ne garantit pas que toutes les pages soient disponibles dans les archives.

### 4.2.6 Contraintes techniques observées

Le code historique du dépôt présente plusieurs contraintes :

- dépendances anciennes susceptibles de nécessiter une adaptation ;
- récupération des articles dépendante de la structure des sites éditeurs ;
- absence de garantie de disponibilité des URL ;
- gestion des erreurs et des délais d'attente à renforcer ;
- dépendance historique à une configuration Twitter ;
- collecte sociale soumise aux conditions d'accès de la plateforme.

L'analyse du code a notamment montré que l'initialisation de la configuration générale instancie le connecteur Twitter et nécessite un fichier de clés, même lorsque le besoin porte uniquement sur la collecte des articles.

Pour CheckIt.AI, il sera préférable de concevoir un collecteur indépendant pour les articles et les médias, sans imposer une dépendance à l'API Twitter.

### 4.2.7 Méthode d'extraction envisagée

La stratégie recommandée est la suivante :

1. Lire les quatre CSV avec `pandas` ou le module standard `csv`.
2. Déduire le label et la plateforme de vérification à partir du fichier source.
3. Conserver les identifiants, les titres et les URL d'origine.
4. Normaliser les URL sans écraser les valeurs brutes.
5. Récupérer les pages éditoriales lorsque leur accès est autorisé.
6. Extraire le texte, la date, les auteurs et les références d'images.
7. Vérifier l'association entre les images et les articles.
8. Enregistrer les erreurs de collecte et les URL indisponibles.

Outils Python envisagés :

- `pandas` pour les fichiers CSV ;
- `requests` pour les requêtes HTTP ;
- `BeautifulSoup` pour l'analyse HTML ;
- une bibliothèque d'extraction d'articles maintenue et compatible avec l'environnement du projet ;
- `Pillow` pour les contrôles des images.

Selenium ne sera envisagé que si une page nécessite réellement une interaction avec un navigateur et si cette collecte est autorisée.

### 4.2.8 Droits, confidentialité et limites

Le dépôt précise que le dataset complet ne peut pas être redistribué librement en raison notamment des politiques de confidentialité de Twitter et des droits des éditeurs de presse.

La disponibilité du code et des fichiers CSV minimaux ne signifie donc pas que l'ensemble des contenus récupérables puisse être copié ou redistribué.

Les identifiants sociaux ne doivent pas être assimilés à une autorisation d'accès aux données personnelles correspondantes.

Toute collecte complémentaire devra respecter les conditions des plateformes, les droits des éditeurs et les règles applicables à la protection des données.

### 4.2.9 Évaluation pour CheckIt.AI

**Décision : source retenue comme source complémentaire d'articles et de provenance de vérification.**

FakeNewsNet présente un intérêt pour enrichir le corpus avec des articles de presse et des données sociales associées.

Sa principale limite est l'absence de contenu multimodal complet directement disponible dans les CSV minimaux. La récupération du texte et des images dépend de l'accessibilité des pages éditoriales et des droits applicables.

La collecte devra donc être conçue de manière indépendante, robuste et traçable, en distinguant les données fournies initialement par le dataset des données récupérées ultérieurement.

## 4.3 NewsData.io

### 4.3.1 Présentation générale

NewsData.io est un service de collecte et de recherche d'actualités accessible par une API REST.

Documentation officielle :

https://newsdata.io/documentation

Cette API permet de rechercher des articles selon plusieurs critères et de récupérer des informations structurées au format JSON.

Elle constitue une source complémentaire pour CheckIt.AI, notamment pour découvrir des publications récentes provenant de différents pays, domaines et langues.

### 4.3.2 Structure des données

L'analyse de la documentation et de la réponse JSON d'exemple a permis d'identifier les principaux champs suivants :

| Champ | Description | Utilité pour CheckIt.AI |
|---|---|---|
| `article_id` | Identifiant de l'article | Identification |
| `title` | Titre | Texte |
| `link` | URL de l'article | Accès à la source |
| `source_id` | Identifiant du média | Provenance |
| `source_name` | Nom du média | Provenance |
| `source_url` | Site du média | Domaine |
| `source_priority` | Indicateur de priorité de la source | Métadonnée |
| `keywords` | Mots-clés | Indexation |
| `creator` | Auteur ou créateur | Provenance |
| `image_url` | URL de l'image associée | Média |
| `video_url` | URL de la vidéo associée | Média |
| `description` | Description de l'article | Texte |
| `pubDate` | Date de publication | Temporalité |
| `pubDateTZ` | Fuseau horaire de publication | Temporalité |
| `content` | Contenu textuel disponible | Texte |
| `country` | Pays associé | Contexte géographique |
| `category` | Catégorie de l'article | Classification thématique |
| `datatype` | Type de contenu | Qualification |
| `fetched_at` | Date de récupération | Traçabilité |
| `language` | Langue déclarée | Langue |
| `ai_tag` | Étiquettes générées par le service | Métadonnée |
| `sentiment` | Analyse de sentiment | Analyse complémentaire |
| `duplicate` | Indicateur de doublon | Déduplication |
| `ai_summary` | Résumé généré, selon l'offre | Enrichissement |

La réponse peut également contenir des informations supplémentaires selon le type de recherche et le niveau d'abonnement.

### 4.3.3 Données textuelles et multimodales

NewsData.io fournit plusieurs informations utiles à la constitution d'un corpus multimodal :

- titre ;
- description ;
- contenu textuel disponible ;
- URL de l'article ;
- URL d'image éventuelle ;
- URL de vidéo éventuelle ;
- métadonnées de publication et de provenance.

Le champ `image_url` référence une image associée à l'article. Il ne signifie pas que le fichier image est directement intégré dans la réponse JSON.

Le téléchargement, la validation et la conservation de l'image devront donc être réalisés séparément.

La présence de `image_url` n'est pas garantie pour chaque article. Le champ peut être nul.

De même, le contenu textuel disponible dépend des fonctionnalités et des limites de l'offre souscrite.

### 4.3.4 Langues et couverture

La documentation du fournisseur annonce une couverture de plus de 90 langues.

Cette diversité peut être intéressante pour CheckIt.AI, car les phénomènes de désinformation ne sont pas limités à une seule langue ou à une seule zone géographique.

La langue déclarée par l'API devra néanmoins être conservée comme métadonnée fournie par le service. Une vérification linguistique complémentaire pourra être envisagée lorsque cela sera nécessaire.

### 4.3.5 Limites de l'offre gratuite

L'offre gratuite étudiée présente notamment les caractéristiques suivantes :

| Fonctionnalité | Offre gratuite |
|---|---|
| Prix annoncé | 0 $ par mois |
| Crédits API | 200 par jour |
| Historique | 48 dernières heures |
| Actualités en temps réel | Retard annoncé de 12 heures |
| Nombre d'articles par crédit | De 1 à 10 selon les conditions de la requête |
| API d'archives | Non disponible |
| API de comptage | Non disponible |
| Contenu intégral | Non disponible |
| Images d'articles | Champ disponible dans les réponses |
| Résumés IA | Non disponibles |

Ces limitations doivent être prises en compte dans le dimensionnement de la collecte.

Le nombre d'articles récupérables dépend notamment des crédits disponibles, des paramètres de recherche et des règles de facturation du fournisseur.

Les tarifs et fonctionnalités étant susceptibles d'évoluer, ils devront être vérifiés sur la page officielle avant toute décision de souscription.

### 4.3.6 Nature des annotations et précautions

NewsData.io propose des informations telles que le sentiment, les catégories, les étiquettes générées par intelligence artificielle et la priorité de la source.

Ces informations ne constituent pas des labels de vérification factuelle.

En particulier :

- un sentiment négatif ne signifie pas qu'un article est faux ;
- une catégorie thématique ne constitue pas une preuve ;
- la priorité attribuée à un domaine ne démontre pas la véracité d'un article ;
- un indicateur de doublon ne garantit pas une déduplication parfaite.

NewsData.io sera donc utilisé pour la découverte et la collecte d'actualités, et non comme arbitre de vérité.

### 4.3.7 Méthode d'extraction envisagée

La méthode d'accès repose sur l'API REST du fournisseur.

Les étapes envisagées sont :

1. Configurer une clé API dans une variable d'environnement.
2. Construire une requête selon les filtres retenus.
3. Envoyer la requête HTTP.
4. Vérifier le statut de la réponse.
5. Interpréter le JSON reçu.
6. Contrôler les champs obligatoires et les valeurs manquantes.
7. Enregistrer les métadonnées et les références des médias.
8. Télécharger et valider séparément les médias lorsque leur utilisation est autorisée.
9. Conserver les informations de pagination et de date de collecte.

Outils Python envisagés :

- `requests` pour les appels HTTP ;
- le module `json` pour l'interprétation des réponses ;
- `pandas` pour l'analyse et la transformation des données ;
- `Pillow` pour le contrôle des images.

Une API REST structurée ne nécessite pas de scraping HTML pour récupérer les champs qu'elle expose directement.

### 4.3.8 Droits d'utilisation et contraintes

L'accès technique à une API ne vaut pas autorisation générale de réutilisation ou de redistribution de tous les contenus retournés.

Il conviendra de consulter les conditions d'utilisation de NewsData.io et, lorsque nécessaire, celles des éditeurs à l'origine des articles.

La conservation des textes complets, des images et des vidéos devra être étudiée séparément, en fonction des droits applicables et de l'offre utilisée.

La clé API devra être stockée dans une variable d'environnement et ne jamais être intégrée au dépôt Git.

### 4.3.9 Évaluation pour CheckIt.AI

**Décision : source retenue comme complément pour la découverte et la collecte d'actualités.**

NewsData.io apporte une interface structurée, une couverture linguistique annoncée importante et des références vers des contenus textuels et visuels.

Ses principales limites concernent les quotas, les restrictions de l'offre gratuite, la disponibilité variable des médias et l'absence de labels de vérification factuelle.

Son rôle dans CheckIt.AI sera donc celui d'une source d'acquisition de publications, complétée par des mécanismes indépendants de vérification et de qualification.

## 4.4 CIMPLE Knowledge Graph

### 4.4.1 Présentation générale

CIMPLE Knowledge Graph est une base de connaissances consacrée notamment aux contenus de fact-checking et aux affirmations vérifiées par des organisations spécialisées.

Ressources officielles :

- Dépôt GitHub : https://github.com/CIMPLE-project/knowledge-base
- Point d'accès SPARQL : https://data.cimple.eu/sparql
- Données ClaimReview : https://github.com/MartinoMensio/claimreview-data

Cette source présente un intérêt particulier pour CheckIt.AI : elle permet de récupérer des informations structurées sur des affirmations, leurs vérifications, les organisations responsables et les verdicts associés.

Contrairement à Fakeddit, CIMPLE n'a pas été retenu comme source principale d'images. Son rôle est principalement celui de l'enrichissement factuel et de la qualification des labels.

### 4.4.2 Version et archive étudiées

L'exploration a porté sur la publication du 2 novembre 2026.

| Élément | Valeur |
|---|---|
| Version | `2026_11_02` |
| Tag | `2026_11_02` |
| Commit | `fb4c08dff60b968ebb449723b988e1b8c5cda84b` |
| Format | N-Triples RDF |
| Archive | `data.claimreview-kg_2026_11_02.nt.gz` |
| Taille de l'archive | Environ 13 Mo |
| Nombre de claims annoncé | 336 568 |
| Nombre d'organisations annoncé | 134 |
| Nombre de langues annoncé | 29 |
| Nombre d'entités annoncé | 264 122 |

L'empreinte SHA-256 de l'archive téléchargée a été vérifiée :

`afcdb40a734276c50791975ffb1754e2b981decacd4cd15f585947fd5fba1da2`

Cette empreinte permet d'identifier précisément le fichier utilisé pendant l'exploration.

Les statistiques globales annoncées dans la publication ne doivent pas être confondues avec les décomptes réalisés sur les ressources d'un type particulier dans l'archive.

### 4.4.3 Format et modèle RDF

L'archive est fournie au format N-Triples, une représentation textuelle de données RDF.

Chaque ligne décrit une relation entre trois éléments :

- un sujet ;
- un prédicat ;
- un objet.

Cette structure permet de représenter des relations entre affirmations, vérifications, évaluations et organisations.

Les données peuvent être interrogées à l'aide de SPARQL, ou analysées localement après décompression de l'archive.

Les principaux éléments identifiés lors de l'inspection sont les suivants :

| Ressource ou propriété | Fonction |
|---|---|
| `schema:Claim` | Affirmation faisant l'objet d'une vérification |
| `schema:ClaimReview` | Publication de fact-checking |
| `schema:Rating` | Ressource décrivant une évaluation |
| `schema:text` | Contenu textuel |
| `schema:url` | URL de la publication de vérification |
| `schema:author` | Organisation associée |
| `schema:itemReviewed` | Lien entre une vérification et une affirmation |
| `schema:reviewRating` | Lien vers l'évaluation |
| `schema:ratingValue` | Valeur du verdict |
| `schema:datePublished` | Date de publication |
| `schema:inLanguage` | Langue déclarée |

Cette organisation permet de conserver séparément l'affirmation initiale, l'article de vérification et le verdict associé.

### 4.4.4 Résultats de l'inspection de l'archive

L'analyse locale de l'archive a permis d'identifier les ressources typées suivantes :

| Type de ressource | Nombre observé |
|---|---:|
| `schema:Rating` | 30 356 |
| `schema:ClaimReview` | 800 |
| `schema:Claim` | 800 |
| `schema:Organization` | 40 |

Le nombre global de claims annoncé dans les métadonnées de publication est de 336 568. Le nombre de ressources `schema:Claim` typées observé dans cette archive est de 800.

Ces valeurs correspondent à des périmètres de comptage différents et ne doivent pas être présentées comme contradictoires sans examiner la composition complète du graphe et les définitions statistiques du fournisseur.

La relation `schema:reviewRating` a été observée pour les 800 ressources `ClaimReview`.

La propriété `schema:datePublished` a été observée pour 670 ressources, tandis que `schema:inLanguage` est présente pour les 800 ressources examinées.

### 4.4.5 Structure d'une vérification

L'inspection d'une ressource `ClaimReview` a mis en évidence plusieurs informations :

- un identifiant propre à la vérification ;
- le texte de l'article de fact-checking ;
- l'URL de la publication d'origine ;
- l'organisation associée ;
- la date de publication ;
- la langue déclarée ;
- un lien vers l'affirmation examinée ;
- un lien vers une ressource décrivant le verdict.

La relation `schema:itemReviewed` permet de relier la vérification à l'affirmation concernée.

La relation `schema:reviewRating` permet de retrouver la ressource contenant l'évaluation.

Cette séparation est importante pour CheckIt.AI : une affirmation peut faire l'objet de plusieurs vérifications et les évaluations doivent conserver leur provenance.

Une incohérence a été observée dans un exemple : le texte de vérification est en marathi alors que la propriété `schema:inLanguage` indique `English`.

La langue déclarée ne devra donc pas être considérée comme une vérité absolue. Une détection linguistique complémentaire pourra être appliquée au texte récupéré.

### 4.4.6 Nature des verdicts

L'archive examinée contient cinq valeurs de verdict normalisées.

| Verdict | Effectif | Part |
|---|---:|---:|
| `not_credible` | 526 | 65,75 % |
| `credible` | 111 | 13,88 % |
| `uncertain` | 68 | 8,50 % |
| `not_verifiable` | 56 | 7,00 % |
| `mostly_credible` | 39 | 4,87 % |
| **Total** | **800** | **100 %** |

Ces catégories ne doivent pas être réduites automatiquement à une classification binaire.

En particulier :

- `not_credible` indique une évaluation défavorable ;
- `credible` indique une évaluation favorable ;
- `mostly_credible` exprime une crédibilité partielle ;
- `uncertain` exprime une incertitude ;
- `not_verifiable` indique que la vérification n'a pas permis de conclure.

Il est donc préférable de conserver les cinq valeurs originales dans le corpus brut et de définir ultérieurement, si nécessaire, une stratégie de regroupement adaptée à une tâche de classification précise.

Les catégories incertaines ou non vérifiables ne doivent jamais être transformées arbitrairement en labels fake ou real.

### 4.4.7 Langues observées

Parmi les 800 ressources `ClaimReview` inspectées, 15 langues déclarées ont été observées.

| Langue déclarée | Effectif |
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

Les statistiques globales de la publication annoncent 29 langues pour l'ensemble du knowledge graph.

La répartition observée sur les 800 ressources `ClaimReview` constitue donc un périmètre d'analyse plus restreint.

La présence de seulement cinq vérifications déclarées en français dans cet échantillon devra être prise en compte si CheckIt.AI vise prioritairement le marché francophone.

### 4.4.8 Disponibilité des images

L'inspection de l'archive a recherché plusieurs propriétés susceptibles de référencer des images ou des médias, notamment :

- `schema:image` ;
- `schema:thumbnailUrl` ;
- `schema:associatedMedia` ;
- `schema:contentUrl` ;
- `foaf:depiction`.

Aucune occurrence n'a été trouvée parmi les propriétés recherchées dans l'archive examinée.

Cette observation ne démontre pas l'absence absolue de toute référence indirecte à un média dans le knowledge graph.

Cependant, l'archive analysée ne peut pas être considérée comme une source directe d'images pour le corpus multimodal.

Les images éventuellement nécessaires devront être recherchées séparément à partir des pages de fact-checking, sous réserve de leur disponibilité et des droits applicables.

### 4.4.9 Méthode d'extraction envisagée

Deux modes d'accès sont envisageables :

**Interrogation SPARQL**

L'endpoint public permet de sélectionner les informations nécessaires sans télécharger systématiquement l'intégralité du graphe.

Cette approche est adaptée à la récupération ciblée des affirmations, vérifications, verdicts et organisations.

**Téléchargement de l'archive RDF**

L'archive N-Triples peut être téléchargée, décompressée et analysée localement.

Cette méthode permet de conserver une version datée et reproductible des données utilisées.

Pour CheckIt.AI, les outils envisagés sont :

- `requests` pour les requêtes HTTP ;
- un client SPARQL compatible ;
- `rdflib` pour l'analyse RDF ;
- `gzip` pour la décompression ;
- `hashlib` pour vérifier l'intégrité des archives.

La collecte devra préserver les identifiants RDF et les relations entre les ressources, plutôt que de réduire immédiatement les données à un tableau plat.

### 4.4.10 Limites et précautions

Les principales limites identifiées sont :

- couverture linguistique variable ;
- présence de catégories de verdict non binaires ;
- incohérences possibles entre langue déclarée et langue réelle ;
- nombre de ressources dépendant de la version et du périmètre étudiés ;
- absence de références directes aux images parmi les propriétés recherchées ;
- nécessité de conserver les relations RDF et la provenance des évaluations.

Les conditions de licence et de réutilisation devront être vérifiées à partir des informations officielles du projet avant toute redistribution des données ou de contenus associés.

### 4.4.11 Évaluation pour CheckIt.AI

**Décision : source retenue pour l'enrichissement factuel et la qualification des labels.**

CIMPLE Knowledge Graph apporte une structure particulièrement utile pour relier les affirmations, les articles de fact-checking, les organisations et les verdicts.

Il ne remplace pas une source multimodale de publications : son intérêt réside principalement dans la vérification et la traçabilité.

Son intégration devra préserver les catégories originales, les identifiants RDF, les dates, les langues déclarées et les URL de vérification.

# 5. Analyse comparative des sources

## 5.1 Tableau comparatif général

Les quatre sources étudiées répondent à des besoins complémentaires. Leur comparaison doit tenir compte de la nature des données réellement disponibles et non uniquement de leur volume ou de leur couverture annoncée.

| Critère | Fakeddit | FakeNewsNet | NewsData.io | CIMPLE Knowledge Graph |
|---|---|---|---|---|
| Nature | Dataset de recherche | Dataset de recherche | API d'actualités | Knowledge graph de fact-checking |
| Données textuelles | Oui | Titres directement disponibles ; articles à récupérer | Titres, descriptions et contenu selon l'offre | Affirmations et textes de vérification |
| Données images | URL associées aux publications | À extraire des pages éditoriales | URL d'images éventuelles | Pas de référence directe observée dans l'archive étudiée |
| Vidéos | Non établies dans le fichier étudié | Non établies dans les CSV minimaux | URL de vidéos éventuelles | Non établies |
| Métadonnées | Nombreuses | Identifiants, titres, URL, tweets | Nombreuses | Relations RDF, dates, langues, organisations |
| Labels | 2, 3 et 6 catégories | Fake / real selon la plateforme | Pas de label de véracité | Cinq catégories de verdict observées |
| Fiabilité des labels | Supervision indirecte, potentiellement bruitée | Évaluations de plateformes de fact-checking | Pas de labels de vérité | Verdicts issus de ressources de fact-checking |
| Langues | Selon les publications du dataset | Selon les articles | Plus de 90 langues annoncées | 29 langues annoncées pour le graphe |
| Format | TSV | CSV et JSON pour les collectes complémentaires | JSON | RDF N-Triples |
| Accès | Téléchargement | Dépôt et collecte complémentaire | API REST | Archive RDF et endpoint SPARQL |
| Extraction principale | Lecture TSV et téléchargement HTTP | Lecture CSV et collecte Web | Requêtes API | SPARQL ou analyse RDF |
| Rôle dans CheckIt.AI | Apprentissage multimodal initial | Enrichissement éditorial et social | Découverte d'actualités | Enrichissement factuel |

## 5.2 Complémentarité des sources

Les quatre sources ne doivent pas être considérées comme interchangeables.

Fakeddit constitue le point de départ le plus direct pour l'apprentissage multimodal, car les publications comportent des titres et des références d'images ainsi que des labels.

FakeNewsNet apporte une autre dimension : les liens entre les articles, les plateformes de vérification et les publications sociales. Il nécessite toutefois une collecte complémentaire des contenus éditoriaux.

NewsData.io permet d'élargir la collecte à des actualités récentes et multilingues grâce à une interface API structurée. En revanche, il ne fournit pas directement une vérité terrain sur la véracité des articles.

Enfin, CIMPLE permet de retrouver des informations de fact-checking structurées et de conserver les relations entre une affirmation, sa vérification et son verdict.

## 5.3 Positionnement dans le pipeline CheckIt.AI

La répartition fonctionnelle recommandée est la suivante :

| Étape du pipeline | Source privilégiée | Fonction |
|---|---|---|
| Constitution du corpus initial | Fakeddit | Publications textuelles et références d'images annotées |
| Enrichissement éditorial | FakeNewsNet | Récupération d'articles et de métadonnées |
| Collecte complémentaire | NewsData.io | Découverte d'actualités et de médias |
| Vérification factuelle | CIMPLE | Récupération de verdicts et de références de fact-checking |
| Qualification finale | Ensemble des sources | Contrôle des données, provenance et cohérence des associations |

Cette organisation permet de distinguer l'acquisition des publications de leur vérification factuelle.

Une publication collectée depuis NewsData.io, par exemple, ne doit pas être considérée comme vraie ou fausse simplement parce qu'elle provient d'un média référencé par le service.

## 5.4 Synthèse de la sélection

Les quatre sources sont retenues pour des fonctions différentes :

- **Fakeddit :** source prioritaire pour démarrer l'apprentissage multimodal.
- **FakeNewsNet :** source complémentaire pour enrichir les articles et les relations sociales.
- **NewsData.io :** source complémentaire pour découvrir et collecter des actualités.
- **CIMPLE Knowledge Graph :** source de référence pour enrichir les données par des vérifications factuelles structurées.

Cette sélection permet de couvrir les besoins principaux de CheckIt.AI tout en reconnaissant les limites propres à chaque source.

# 6. Évaluation de la qualité et de la fiabilité des labels

## 6.1 Pourquoi la qualité des labels est essentielle

La performance d'un modèle de détection de désinformation dépend fortement de la qualité des données utilisées pour son apprentissage et son évaluation.

Un modèle entraîné sur des annotations imprécises risque d'apprendre des associations erronées et de reproduire les biais présents dans les sources.

Il est donc nécessaire de distinguer la nature du label, son origine, sa méthode d'attribution et son degré de certitude.

La présence d'un label dans un fichier ne garantit pas, à elle seule, que l'information a fait l'objet d'une vérification factuelle indépendante.

## 6.2 Comparaison des méthodes d'annotation

| Source | Origine du label | Niveau de confiance à considérer | Précaution principale |
|---|---|---|---|
| Fakeddit | Catégories et règles de supervision du dataset | Annotation indirecte, potentiellement bruitée | Ne pas assimiler automatiquement le label à une vérification individuelle |
| FakeNewsNet | Plateformes GossipCop et PolitiFact | Évaluation issue d'un travail de fact-checking | Conserver la plateforme et la provenance du verdict |
| NewsData.io | Pas de label de véracité fourni dans les champs étudiés | Non applicable | Ne pas utiliser le sentiment ou les catégories comme vérité terrain |
| CIMPLE | Ressources de fact-checking structurées | Verdict documenté et traçable | Préserver les catégories nuancées et l'organisation évaluatrice |

Ces niveaux ne constituent pas une notation universelle de qualité. Ils décrivent la nature des annotations et les précautions nécessaires à leur utilisation.

## 6.3 Distinguer vérité, fausseté et incertitude

Une classification binaire fake / real peut être utile pour certaines tâches, mais elle ne représente pas toute la complexité de la vérification de l'information.

CheckIt.AI devra notamment distinguer :

- **Faux :** affirmation contredite par des éléments factuels suffisamment établis.
- **Vrai :** affirmation étayée par les éléments disponibles.
- **Partiellement vrai ou trompeur :** affirmation comportant des éléments exacts mais présentés de manière susceptible d'induire en erreur.
- **Satire ou parodie :** contenu humoristique qui ne doit pas être automatiquement assimilé à une tentative de désinformation.
- **Incertain :** éléments insuffisants ou contradictoires pour conclure.
- **Non vérifiable :** affirmation pour laquelle les éléments disponibles ne permettent pas une vérification satisfaisante.
- **Opinion :** jugement subjectif qui ne se vérifie pas de la même manière qu'une affirmation factuelle.

Une opinion controversée ne constitue donc pas automatiquement une fausse information.

La qualification de désinformation doit également tenir compte de la différence entre une erreur, une information trompeuse et une diffusion intentionnelle de fausses informations. L'intention ne peut pas être déduite du seul contenu textuel.

## 6.4 Stratégie de conservation des labels

Pour préserver la traçabilité, le pipeline devra conserver séparément :

- la valeur originale du label ;
- la source ayant fourni ce label ;
- l'identifiant de l'enregistrement d'origine ;
- l'URL de la vérification, lorsqu'elle existe ;
- la date de vérification, lorsqu'elle est disponible ;
- la catégorie normalisée éventuellement produite par CheckIt.AI ;
- le niveau de confiance ou le statut de validation, lorsqu'il est justifié.

La valeur originale ne devra jamais être écrasée par une transformation interne.

La normalisation devra être réversible ou, à défaut, documentée.

## 6.5 Règles de qualité retenues

Les règles suivantes sont adoptées pour la constitution du corpus :

1. Une publication sans label reste non labellisée. Elle ne doit jamais être considérée automatiquement comme vraie.
2. Le label d'origine et sa provenance sont conservés.
3. Les catégories incertaines et non vérifiables restent distinctes des catégories fake et real.
4. Une opinion controversée n'est pas automatiquement une désinformation.
5. Les données brutes sont conservées même si une image ou un label manque.
6. Une publication ne rejoint le sous-corpus multimodal exploitable que si elle possède un texte utilisable et au moins une image accessible explicitement associée à cette publication.

Ces règles permettent de limiter les erreurs de qualification et de conserver une trace des décisions prises pendant la préparation des données.

## 6.6 Gestion des cas incomplets

Une publication peut être exploitable pour certaines analyses sans satisfaire tous les critères du corpus multimodal final.

Les cas suivants devront être distingués :

| Situation | Conservation | Utilisation possible |
|---|---|---|
| Texte et image disponibles, label connu | Oui | Corpus multimodal annoté |
| Texte et image disponibles, label inconnu | Oui | Corpus multimodal non annoté |
| Texte disponible, image absente | Oui | Corpus textuel |
| Image référencée mais inaccessible | Oui | Donnée à contrôler, exclue du corpus multimodal validé |
| Label disponible, texte absent | Oui, si les métadonnées sont utiles | Enrichissement ou analyse de provenance |
| Vérification contradictoire | Oui | Revue complémentaire, sans fusion automatique des verdicts |

La conservation des cas incomplets évite de perdre des informations potentiellement utiles et permet de mesurer les limites de couverture des sources.

## 6.7 Conséquences pour l'entraînement et l'évaluation

Les différences de provenance et de qualité des labels devront être prises en compte lors de la constitution des jeux d'entraînement, de validation et de test.

Il sera notamment nécessaire :

- d'éviter les doublons entre les différents jeux de données ;
- de conserver les identifiants et les URL permettant de retrouver les publications originales ;
- de contrôler les déséquilibres entre catégories ;
- de séparer les données annotées des données non annotées ;
- de documenter les règles de normalisation ;
- d'éviter qu'une même publication ou une même image se retrouve dans plusieurs partitions.

Pour les classifications comportant plusieurs catégories, des métriques telles que le macro-F1, le rappel par classe et la matrice de confusion seront privilégiées en complément de l'accuracy.

La qualité des labels devra ainsi être considérée comme une dimension du projet à part entière, et non comme une simple propriété héritée des sources.

# 7. Formats et méthodes d'extraction envisagés

## 7.1 Principes généraux

Les quatre sources utilisent des formats et des modes d'accès différents. Le pipeline CheckIt.AI devra donc prévoir des mécanismes d'acquisition adaptés à chaque fournisseur, tout en produisant une représentation interne cohérente.

La stratégie retenue privilégie les interfaces officielles, les fichiers publiés par les fournisseurs et les formats structurés.

Le scraping HTML sera réservé aux situations dans lesquelles les informations nécessaires ne sont pas disponibles par un moyen plus direct et lorsque les conditions d'accès l'autorisent.

## 7.2 Méthodes par source

| Source | Format d'origine | Méthode d'acquisition | Outils envisagés |
|---|---|---|---|
| Fakeddit | TSV et fichiers images | Téléchargement des fichiers, lecture tabulaire et récupération HTTP des images | `pandas`, `requests`, `Pillow` |
| FakeNewsNet | CSV, puis pages Web et JSON complémentaires | Lecture CSV et extraction des articles accessibles | `csv`, `pandas`, `requests`, BeautifulSoup |
| NewsData.io | JSON | API REST avec pagination et authentification | `requests`, `json` |
| CIMPLE | RDF N-Triples compressé ou SPARQL | Téléchargement d'archive ou requêtes SPARQL | `gzip`, `rdflib`, client SPARQL |

Ces outils sont des choix envisagés pour la future implémentation. Leur sélection définitive pourra être adaptée selon les contraintes techniques et les versions maintenues.

## 7.3 Gestion des requêtes HTTP

Les collecteurs qui accèdent à des ressources Web devront intégrer des mécanismes communs :

- délais d'attente explicites ;
- gestion des erreurs réseau ;
- nombre limité de tentatives ;
- temporisation entre les requêtes ;
- contrôle des codes de réponse HTTP ;
- journalisation des échecs ;
- respect des conditions d'utilisation et des limites de débit.

Les requêtes ne devront pas être répétées indéfiniment en cas d'échec.

Les réponses HTTP devront être contrôlées avant d'être interprétées ou enregistrées.

## 7.4 Récupération et validation des images

La récupération d'une URL d'image ne garantit pas que le fichier correspondant soit exploitable.

Pour chaque média, le pipeline devra notamment vérifier :

- que l'URL est présente et correctement formée ;
- que la ressource est accessible ;
- que la réponse correspond à un type de contenu attendu ;
- que le fichier peut être ouvert comme une image ;
- que ses dimensions sont exploitables ;
- que le téléchargement n'est pas vide ou tronqué ;
- que l'image est bien associée à la publication concernée.

Les URL d'origine et les chemins locaux des fichiers téléchargés devront être conservés séparément.

Une empreinte du fichier pourra être calculée afin de détecter les doublons exacts.

## 7.5 Stratégie de stockage des données

Trois niveaux de conservation sont envisagés :

| Niveau | Contenu | Objectif |
|---|---|---|
| RAW | Données telles que reçues des sources | Préserver l'origine et permettre une reprise |
| INTERIM | Données extraites, contrôlées et normalisées | Faciliter les traitements et les rapprochements |
| PROCESSED | Données qualifiées et prêtes pour les usages ultérieurs | Constituer le corpus exploitable |

Les données brutes ne devront pas être modifiées pour masquer une anomalie ou une erreur de collecte.

Les transformations seront effectuées dans les niveaux intermédiaires et documentées.

## 7.6 Formats de sortie envisagés

Deux formats principaux sont envisagés pour les données tabulaires et les enregistrements :

**JSON Lines (JSONL)**

Le format JSONL stocke un objet JSON par ligne.

Il convient aux enregistrements hétérogènes et permet de représenter naturellement les listes d'images, les métadonnées et les informations de vérification.

Il est également adapté à une collecte progressive.

**Parquet**

Le format Parquet est un format colonne particulièrement intéressant pour les analyses volumineuses.

Il permet une compression efficace et facilite la lecture sélective de colonnes avec les outils d'analyse de données.

Pour CheckIt.AI, JSONL est envisagé pour la conservation des enregistrements structurés issus de la collecte, tandis que Parquet pourra être utilisé pour les jeux de données normalisés et les analyses.

Les fichiers médias seront stockés séparément. Leurs chemins, URL et métadonnées seront référencés dans les enregistrements.

## 7.7 Traçabilité des extractions

Chaque opération de collecte devra permettre de retrouver :

- la source d'origine ;
- la date et l'heure de collecte ;
- l'URL ou l'identifiant de la ressource ;
- la version du dataset ou de l'API, lorsque disponible ;
- le statut de l'extraction ;
- les éventuelles erreurs rencontrées ;
- les transformations appliquées.

Cette traçabilité facilitera le diagnostic des anomalies et la reproductibilité des traitements.

# 8. Droits d'utilisation, confidentialité et conformité

## 8.1 Principes généraux

La disponibilité technique d'une donnée ne signifie pas automatiquement que son utilisation, sa conservation ou sa redistribution sont autorisées.

Avant toute collecte, CheckIt.AI devra prendre en compte :

- les licences des datasets ;
- les conditions d'utilisation des API ;
- les droits des éditeurs sur les articles et les images ;
- les règles des plateformes sociales ;
- les obligations relatives à la protection des données personnelles.

L'utilisation à des fins de recherche ou de formation ne dispense pas de vérifier les conditions applicables.

## 8.2 Points de vigilance par source

| Source | Point de vigilance | Mesure recommandée |
|---|---|---|
| Fakeddit | Licence des données et droits sur les contenus Reddit et les images | Vérifier les conditions officielles avant redistribution |
| FakeNewsNet | Restrictions liées aux politiques de Twitter et aux droits des éditeurs | Ne pas redistribuer les contenus complets sans autorisation |
| NewsData.io | Conditions contractuelles de l'API et droits sur les contenus des éditeurs | Vérifier les conditions de l'offre et limiter la conservation aux usages autorisés |
| CIMPLE | Licence du knowledge graph et droits sur les contenus de fact-checking associés | Vérifier la licence de la version utilisée et respecter ses obligations |

Pour Fakeddit, la fiche de ressources LREC consultée indique que la licence n'est pas spécifiée. Cette absence d'information ne doit pas être interprétée comme une autorisation générale de redistribution.

Pour FakeNewsNet, le dépôt précise que le dataset complet ne peut pas être redistribué librement en raison notamment des politiques de confidentialité de Twitter et des droits des éditeurs.

Pour NewsData.io, les conditions de l'offre et les droits attachés aux contenus retournés devront être examinés avant toute conservation ou redistribution.

Pour CIMPLE, la licence applicable devra être confirmée à partir des fichiers et informations officiels associés à la version téléchargée.

## 8.3 Protection des données personnelles

Les données issues des réseaux sociaux ou des pages Web peuvent contenir des informations relatives à des personnes physiques.

Le pipeline devra appliquer un principe de minimisation :

- ne collecter que les informations nécessaires aux objectifs du projet ;
- éviter de récupérer des profils ou des informations personnelles sans besoin justifié ;
- protéger les identifiants et les éventuelles données sensibles ;
- limiter les accès aux données collectées ;
- documenter la provenance et les conditions de conservation.

Les identifiants de publications et les URL pourront être conservés lorsqu'ils sont nécessaires à la traçabilité, sous réserve des conditions applicables.

## 8.4 Sécurité des accès

Les clés API et autres secrets techniques ne devront jamais être enregistrés dans les fichiers versionnés du dépôt Git.

Ils seront fournis au moment de l'exécution par des variables d'environnement ou un mécanisme de gestion de secrets adapté.

Les fichiers de configuration versionnés ne contiendront que des paramètres non sensibles ou des valeurs d'exemple.

## 8.5 Décision de conformité avant intégration

Avant d'intégrer une nouvelle source dans le pipeline, une vérification devra être effectuée sur :

1. les conditions d'accès ;
2. la licence du dataset ou les conditions contractuelles de l'API ;
3. les droits relatifs aux textes et aux médias ;
4. les restrictions de conservation et de redistribution ;
5. les éventuelles données personnelles ;
6. les obligations d'attribution ou de citation.

En l'absence d'information suffisante, la source pourra rester utilisable pour l'exploration technique, mais sa redistribution ou son intégration dans un corpus partagé devra être suspendue jusqu'à clarification.

Cette démarche vise à rendre le projet reproductible tout en limitant les risques juridiques et opérationnels.

# 9. Modèle de données cible

## 9.1 Objectifs du modèle

Les quatre sources étudiées présentent des structures différentes. Le pipeline CheckIt.AI devra donc disposer d'un modèle commun permettant de normaliser les informations essentielles sans perdre les spécificités de chaque fournisseur.

Le modèle devra notamment permettre :

- d'identifier chaque publication ;
- de conserver son origine ;
- de stocker le texte et les références des médias ;
- de gérer les dates et les langues ;
- de rattacher les labels et les vérifications à leur source ;
- de suivre la qualité et le statut des extractions.

La normalisation ne devra pas supprimer les données originales ni les informations nécessaires à leur traçabilité.

## 9.2 Structure logique d'une publication

L'enregistrement principal représentera une publication.

| Champ | Type indicatif | Description |
|---|---|---|
| `publication_id` | Chaîne | Identifiant interne de la publication |
| `source_id` | Chaîne | Identifiant de la source |
| `source_name` | Chaîne | Nom de la source |
| `source_record_id` | Chaîne | Identifiant d'origine dans le fournisseur |
| `article_url` | Chaîne | URL de la publication |
| `title` | Texte | Titre original |
| `text_content` | Texte | Contenu textuel disponible |
| `published_at` | Date/heure | Date de publication |
| `collected_at` | Date/heure | Date de collecte |
| `language` | Chaîne | Langue déclarée ou détectée |
| `domain` | Chaîne | Domaine de publication |
| `author` | Chaîne ou liste | Auteur ou auteurs |
| `raw_label` | Chaîne | Label d'origine |
| `label` | Chaîne | Label normalisé éventuel |
| `label_source` | Chaîne | Source du label |
| `fact_check_url` | Chaîne | URL de vérification éventuelle |
| `label_status` | Chaîne | Statut de qualification du label |
| `extraction_status` | Chaîne | Résultat de la collecte |

Les champs non disponibles dans une source resteront absents ou nuls. Ils ne devront pas être remplis par des valeurs supposées.

## 9.3 Gestion des médias

Une publication pourra être associée à zéro, une ou plusieurs images ou vidéos.

Les médias devront être représentés séparément afin de conserver leurs caractéristiques propres.

| Champ | Type indicatif | Description |
|---|---|---|
| `media_id` | Chaîne | Identifiant interne du média |
| `publication_id` | Chaîne | Publication associée |
| `media_type` | Chaîne | Image ou vidéo |
| `media_url` | Chaîne | URL d'origine |
| `media_path` | Chaîne | Chemin local du fichier |
| `mime_type` | Chaîne | Type MIME détecté |
| `width` | Entier | Largeur en pixels, si disponible |
| `height` | Entier | Hauteur en pixels, si disponible |
| `content_hash` | Chaîne | Empreinte du fichier |
| `image_valid` | Booléen | Résultat du contrôle du média |

L'association entre un média et une publication devra être explicite.

Une image trouvée sur une page ne devra pas être considérée automatiquement comme représentative de l'article. Il faudra conserver sa provenance et vérifier la pertinence de son association.

## 9.4 Gestion des vérifications factuelles

Les vérifications seront représentées séparément des publications.

Une publication pourra être associée à plusieurs vérifications, provenant éventuellement d'organisations différentes.

| Champ | Type indicatif | Description |
|---|---|---|
| `fact_check_id` | Chaîne | Identifiant de la vérification |
| `publication_id` | Chaîne | Publication concernée, si le lien est établi |
| `claim_text` | Texte | Affirmation examinée |
| `review_text` | Texte | Texte de la vérification |
| `review_url` | Chaîne | URL de la vérification |
| `review_organization` | Chaîne | Organisation responsable |
| `reviewed_at` | Date/heure | Date de publication ou de vérification |
| `raw_verdict` | Chaîne | Verdict original |
| `normalized_verdict` | Chaîne | Verdict normalisé éventuel |
| `label_source` | Chaîne | Source du verdict |

Une relation entre une vérification et une publication ne sera créée que lorsque cette association est suffisamment justifiée.

Une simple similarité de titre ou de sujet ne suffira pas à établir automatiquement que deux contenus concernent la même affirmation.

## 9.5 Statuts de qualité

Le modèle devra distinguer les statuts de qualité des données des labels de véracité.

Exemples de statuts :

| Champ ou statut | Signification |
|---|---|
| `label_status = known` | Label disponible et documenté |
| `label_status = unknown` | Aucun label exploitable |
| `label_status = uncertain` | Verdict incertain |
| `label_status = not_verifiable` | Vérification impossible ou non concluante |
| `image_valid = true` | Média téléchargé et contrôlé |
| `image_valid = false` | Média absent, inaccessible ou invalide |
| `extraction_status = success` | Extraction réussie |
| `extraction_status = partial` | Extraction partielle |
| `extraction_status = failed` | Extraction échouée |

Ces statuts ne doivent pas être confondus avec une classification fake / real.

## 9.6 Relations entre les entités

Le modèle logique repose sur trois relations principales :

- une source peut fournir plusieurs publications ;
- une publication peut être associée à plusieurs médias ;
- une publication ou une affirmation peut faire l'objet de plusieurs vérifications.

Cette organisation permet de préserver la provenance de chaque élément et de gérer les relations plusieurs-à-plusieurs lorsque plusieurs sources ou vérifications concernent un même contenu.

## 9.7 Principes de normalisation

Les règles suivantes seront appliquées :

1. Conserver les identifiants d'origine des fournisseurs.
2. Générer un identifiant interne stable pour chaque publication.
3. Conserver les URL originales, même lorsqu'une version normalisée est créée.
4. Ne pas remplacer un champ manquant par une valeur inventée.
5. Conserver les labels originaux et les verdicts détaillés.
6. Stocker les médias séparément des métadonnées textuelles.
7. Conserver les liens entre publications, affirmations et vérifications.
8. Documenter toute transformation ou décision de rapprochement.

Ce modèle constituera la base de la normalisation des données collectées par les futurs extracteurs.

# 10. Architecture de collecte recommandée

## 10.1 Vue d'ensemble

L'architecture recommandée repose sur une chaîne de traitement organisée en plusieurs étapes indépendantes.

Chaque source dispose de son propre mécanisme d'acquisition. Les données collectées sont ensuite conservées dans leur format d'origine, normalisées et contrôlées avant de rejoindre le corpus exploitable.

L'architecture distingue les opérations suivantes :

1. Acquisition des données.
2. Conservation des données brutes.
3. Extraction et normalisation.
4. Validation des textes, médias et labels.
5. Enrichissement par les informations de fact-checking.
6. Production des données qualifiées.

## 10.2 Organisation des traitements

| Composant | Responsabilité |
|---|---|
| Collecteurs Fakeddit | Lecture des fichiers TSV et récupération des médias |
| Collecteurs FakeNewsNet | Lecture des CSV et récupération des articles accessibles |
| Collecteur NewsData.io | Appels à l'API REST et gestion de la pagination |
| Collecteur CIMPLE | Téléchargement RDF ou interrogation SPARQL |
| Module de normalisation | Conversion vers le modèle de données cible |
| Module de validation | Contrôle des champs, médias et relations |
| Module de stockage | Conservation des données aux différents niveaux |
| Journalisation | Suivi des opérations et des erreurs |

Cette séparation permettra de faire évoluer une source sans modifier l'ensemble du pipeline.

## 10.3 Organisation des données

L'organisation des répertoires de données retenue pour le projet est la suivante :

| Répertoire | Contenu |
|---|---|
| `raw/` | Fichiers d'origine, réponses API et archives téléchargées |
| `interim/` | Données extraites et normalisées |
| `processed/` | Corpus qualifié et prêt pour les traitements ultérieurs |
| `images/` | Médias téléchargés et contrôlés |
| `reports/` | Rapports de collecte et de qualité |
| `logs/` | Journaux d'exécution |

Les données volumineuses seront conservées sur le volume de stockage dédié du serveur, séparément du dépôt Git.

Le dépôt versionnera le code, les configurations non sensibles, la documentation et les tests, mais pas les corpus bruts ni les médias collectés.

## 10.4 Flux de traitement recommandé

Le flux logique peut être représenté ainsi :

```text
Sources externes
      |
      v
Collecteurs spécifiques
      |
      v
Conservation RAW
      |
      v
Extraction et normalisation
      |
      v
Zone INTERIM
      |
      v
Contrôle qualité
      |
      +------> Vérifications CIMPLE / fact-checking
      |
      v
Corpus PROCESSED
      |
      v
Analyses et futurs modèles multimodaux

```

Les informations de fact-checking peuvent enrichir les publications lorsque le lien entre l'affirmation et la vérification est suffisamment établi.

Elles ne doivent pas être associées automatiquement sur la seule base d'une ressemblance thématique.

## 10.5 Reprise après erreur et reproductibilité

Chaque collecteur devra pouvoir reprendre une opération interrompue sans provoquer de duplication incontrôlée.

Les mécanismes à prévoir comprennent :

- conservation des identifiants d'origine ;
- journalisation des URL traitées ;
- suivi des statuts d'extraction ;
- gestion des tentatives et des erreurs ;
- détection des doublons ;
- conservation des versions de sources ;
- vérification de l'intégrité des fichiers.

Les collectes devront être reproductibles autant que possible, avec des paramètres et des versions documentés.

## 10.6 Évolutivité

L'architecture devra permettre d'ajouter ultérieurement de nouvelles sources sans remettre en cause le modèle commun.

De nouvelles sources pourront être intégrées à condition de respecter les mêmes principes :

- provenance conservée ;
- format d'origine préservé ;
- méthode d'accès documentée ;
- données normalisées selon le modèle cible ;
- contrôles qualité appliqués ;
- droits d'utilisation vérifiés.

Cette architecture constitue une base évolutive pour les prochaines étapes de CheckIt.AI.

# 11. Risques identifiés et mesures de maîtrise

## 11.1 Risques liés à la qualité des labels

Les labels des différentes sources ne reposent pas sur les mêmes méthodes de qualification.

Fakeddit utilise une supervision distante fondée sur des catégories de publications. FakeNewsNet reprend des classifications provenant de GossipCop et PolitiFact. CIMPLE fournit des verdicts de fact-checking plus détaillés, mais ceux-ci peuvent être incertains ou non vérifiables.

Le principal risque est de considérer ces labels comme parfaitement équivalents.

**Mesures de maîtrise :**

- conserver systématiquement le label d'origine ;
- documenter la méthode de qualification ;
- distinguer les labels directement vérifiés des labels issus d'une supervision distante ;
- conserver les verdicts incertains et non vérifiables ;
- ne pas convertir automatiquement les catégories en une classification binaire.

## 11.2 Risques liés aux images

Une publication peut disposer d'une URL d'image sans que le fichier soit accessible ou exploitable.

Une page Web peut également contenir plusieurs images qui ne représentent pas toutes le contenu de l'article.

**Mesures de maîtrise :**

- vérifier la disponibilité des fichiers ;
- contrôler le type MIME et les dimensions ;
- conserver l'URL d'origine ;
- vérifier l'association entre le média et la publication ;
- calculer une empreinte pour détecter les doublons ;
- enregistrer les échecs sans supprimer la publication correspondante.

## 11.3 Risques liés aux biais et à la représentativité

Les sources étudiées présentent des biais différents :

- Fakeddit est issu de Reddit et reflète les communautés et catégories présentes dans ce réseau ;
- FakeNewsNet dépend des domaines et des plateformes couverts par GossipCop et PolitiFact ;
- NewsData.io dépend de son réseau de fournisseurs, de ses filtres et de son offre commerciale ;
- CIMPLE dépend des organisations de fact-checking intégrées à son knowledge graph.

Les langues, les pays, les sujets et les catégories de verdict peuvent être inégalement représentés.

**Mesures de maîtrise :**

- analyser la répartition des langues et des sources ;
- mesurer les déséquilibres de classes ;
- documenter les périodes couvertes ;
- éviter de considérer le corpus comme représentatif de toute l'information disponible sur Internet ;
- examiner les performances par source et par langue.

## 11.4 Risques liés à l'extraction

Les pages Web peuvent évoluer, devenir indisponibles ou modifier leur structure HTML.

Les API peuvent imposer des quotas, des délais ou des restrictions d'accès. Les formats et les champs disponibles peuvent également évoluer.

**Mesures de maîtrise :**

- privilégier les API et les fichiers officiels lorsqu'ils sont disponibles ;
- gérer les erreurs HTTP et les limitations de débit ;
- utiliser des délais d'attente et des tentatives contrôlées ;
- journaliser les échecs ;
- documenter les versions et dates de collecte ;
- prévoir une reprise des traitements interrompus.

## 11.5 Risques liés au rapprochement des publications et des fact-checks

Une même affirmation peut être reprise dans plusieurs articles. Inversement, un article peut contenir plusieurs affirmations distinctes.

Un rapprochement fondé uniquement sur le titre ou la similarité lexicale peut donc produire des associations erronées.

**Mesures de maîtrise :**

- conserver les identifiants et URL d'origine ;
- utiliser les liens explicites lorsqu'ils existent ;
- distinguer publication et affirmation ;
- conserver la provenance de chaque vérification ;
- prévoir une validation complémentaire pour les rapprochements incertains.

## 11.6 Risques liés à l'évaluation des futurs modèles

Un jeu de données déséquilibré ou contenant des doublons peut conduire à une évaluation trompeuse.

Des publications similaires provenant de plusieurs sources pourraient également se retrouver simultanément dans les ensembles d'entraînement et de test.

**Mesures de maîtrise :**

- rechercher les doublons exacts et les contenus très similaires ;
- séparer les données d'entraînement, de validation et de test de manière contrôlée ;
- éviter les fuites de données entre les ensembles ;
- suivre le macro-F1, le rappel par classe et la matrice de confusion ;
- analyser les résultats par source et par langue ;
- ne pas se limiter à l'exactitude globale.

## 11.7 Synthèse des risques prioritaires

| Risque | Niveau de vigilance | Mesure prioritaire |
|---|---|---|
| Labels hétérogènes ou bruités | Élevé | Conserver les labels originaux et leur provenance |
| Images absentes ou non pertinentes | Élevé | Contrôler l'accessibilité et l'association |
| Biais des sources et des langues | Élevé | Mesurer la représentativité du corpus |
| Pages Web indisponibles | Moyen à élevé | Prévoir journalisation et reprise |
| Quotas et restrictions API | Moyen à élevé | Contrôler les quotas et les conditions d'accès |
| Mauvais rapprochement des fact-checks | Élevé | Exiger des liens suffisamment justifiés |
| Fuite de données entre ensembles | Élevé | Contrôler les doublons et les séparations |

L'identification de ces risques permet de définir des contrôles adaptés dès la conception du pipeline, plutôt que de tenter de corriger les problèmes uniquement au moment de l'entraînement des modèles.

# 12. Recommandations et stratégie de mise en œuvre

## 12.1 Positionnement des quatre sources

Les quatre sources retenues sont complémentaires et ne doivent pas être considérées comme quatre jeux de données interchangeables.

| Source | Rôle recommandé | Priorité |
|---|---|---|
| Fakeddit | Constituer le premier corpus multimodal d'entraînement | Prioritaire |
| FakeNewsNet | Enrichir les publications avec des articles et des données sociales accessibles | Élevée |
| NewsData.io | Compléter la collecte avec des actualités récentes et des métadonnées structurées | Selon les quotas et les conditions de l'offre |
| CIMPLE | Apporter des informations de fact-checking et des verdicts documentés | Prioritaire pour l'enrichissement des labels |

Fakeddit constitue le point de départ le plus direct pour travailler sur des données associant texte et image.

FakeNewsNet apporte une possibilité d'enrichissement à partir d'articles et de publications sociales, mais nécessite des opérations supplémentaires de collecte et de vérification.

NewsData.io offre une interface structurée pour accéder à des actualités, mais son offre gratuite limite notamment l'accès temporel et au contenu intégral.

CIMPLE apporte une ressource complémentaire de vérification factuelle. Son intérêt réside dans la structuration des affirmations, des organisations et des verdicts, et non dans la fourniture directe d'un corpus d'images.

## 12.2 Ordre de mise en œuvre recommandé

La mise en œuvre devra être progressive afin de limiter les difficultés techniques et de mesurer la qualité de chaque source.

| Ordre | Action | Résultat attendu |
|---|---|---|
| 1 | Exploiter le fichier TSV Fakeddit | Premier corpus texte-image structuré |
| 2 | Analyser et enrichir FakeNewsNet | Articles récupérés et métadonnées associées |
| 3 | Interroger CIMPLE | Référentiel de vérifications et de verdicts |
| 4 | Évaluer l'intégration de NewsData.io | Flux complémentaire d'actualités |
| 5 | Normaliser et contrôler les données | Corpus commun documenté |
| 6 | Constituer un sous-ensemble multimodal qualifié | Données adaptées aux étapes suivantes |

Cet ordre distingue la disponibilité technique des données de leur valeur pour l'objectif final.

## 12.3 Contrôles qualité à mettre en place

Avant toute utilisation dans les traitements ultérieurs, les contrôles suivants devront être réalisés :

- présence des champs essentiels ;
- validité des URL ;
- cohérence des dates ;
- détection de la langue ;
- accessibilité des images ;
- correspondance entre texte et média ;
- cohérence des labels ;
- conservation de la provenance ;
- détection des doublons ;
- mesure des données manquantes.

Les résultats devront être synthétisés dans des rapports de qualité par source.

## 12.4 Constitution de deux niveaux de données

Il est recommandé de distinguer deux niveaux de conservation.

**Corpus brut :**

Il conserve les données collectées, y compris les publications incomplètes, les images absentes et les labels inconnus.

**Corpus multimodal qualifié :**

Il contient les publications disposant d'un contenu textuel exploitable et d'au moins une image accessible et explicitement associée à la publication.

Les publications sans image ne seront donc pas supprimées du corpus brut. Elles pourront rester utiles pour des analyses textuelles ou des enrichissements ultérieurs.

## 12.5 Stratégie de labellisation

La stratégie de labellisation devra préserver la diversité des verdicts disponibles.

Il est recommandé de conserver :

- le label d'origine ;
- la source du label ;
- l'URL de la vérification ;
- la date de vérification lorsqu'elle est disponible ;
- le niveau de confiance lorsqu'il peut être justifié ;
- le statut de qualification.

Une classification binaire pourra éventuellement être construite pour une expérience précise, mais uniquement après définition de règles explicites et documentées.

Les verdicts incertains ou non vérifiables devront rester distincts des contenus faux et vrais.

## 12.6 Indicateurs de suivi

Les indicateurs suivants permettront de suivre la qualité et la couverture du corpus :

| Indicateur | Objectif |
|---|---|
| Nombre de publications collectées | Mesurer le volume |
| Taux de publications avec texte exploitable | Mesurer la couverture textuelle |
| Taux de publications avec image accessible | Mesurer la couverture multimodale |
| Taux de labels connus | Mesurer la disponibilité des annotations |
| Répartition des labels | Mesurer le déséquilibre des classes |
| Répartition par langue | Mesurer la couverture linguistique |
| Taux d'échec d'extraction | Suivre la robustesse des collecteurs |
| Taux de doublons | Contrôler la qualité du corpus |
| Taux de rapprochements fact-check validés | Mesurer la qualité de l'enrichissement |

Ces indicateurs devront être calculés séparément pour chaque source avant d'être agrégés.

## 12.7 Décisions restant à confirmer

Certaines décisions ne pourront être prises qu'après les premiers essais d'intégration :

- choix définitif entre JSONL et Parquet selon les besoins des traitements ;
- définition des règles de normalisation des verdicts ;
- validation des licences et conditions d'utilisation ;
- mesure du taux réel de récupération des images ;
- évaluation du coût et de l'intérêt de l'offre NewsData.io ;
- définition des règles de rapprochement entre publications et fact-checks.

Ces décisions seront documentées à partir des résultats observés, et non uniquement sur la base des descriptions des fournisseurs.

# 13. Conclusion générale

L'exploration menée dans le cadre du projet CheckIt.AI a permis d'identifier et d'étudier quatre sources complémentaires pour la constitution d'un corpus destiné à la détection de fausses informations multimodales.

Fakeddit constitue la source de départ la plus directement adaptée à l'objectif multimodal grâce à ses publications associant texte, images et labels. Toutefois, ses annotations reposent sur une supervision distante et doivent être considérées avec prudence.

FakeNewsNet permet d'enrichir les données à partir de publications issues de GossipCop et PolitiFact. Les fichiers disponibles fournissent des titres, des URL et des identifiants de publications sociales. La récupération du contenu des articles et de leurs images nécessite cependant des traitements supplémentaires.

NewsData.io offre une API structurée permettant de collecter des actualités et leurs métadonnées, notamment des URL d'images et de vidéos. Son intérêt dépendra des limites de l'offre retenue, des droits d'utilisation et de la disponibilité effective des contenus.

Enfin, CIMPLE apporte une ressource structurée de fact-checking, avec des affirmations, des organisations et des verdicts détaillés. Cette source est particulièrement utile pour l'enrichissement et l'analyse de la qualité des labels, mais ne constitue pas directement un corpus multimodal d'images.

L'étude montre que la constitution d'un corpus fiable ne dépend pas uniquement du volume de données collectées. Elle repose également sur la qualité des annotations, la traçabilité, la pertinence des associations entre textes et images, la représentativité des sources et le respect des conditions d'utilisation.

Le modèle de données proposé permettra de conserver les informations d'origine, de distinguer les publications des médias et des vérifications factuelles, et de gérer les données incomplètes sans introduire de labels artificiels.

La prochaine étape consistera à mettre en œuvre progressivement les collecteurs, à mesurer leurs performances réelles et à produire un corpus normalisé et contrôlé. Les résultats de ces essais permettront de confirmer les choix techniques et les règles de qualification définis dans ce rapport.

Cette première étape fournit ainsi une base méthodologique et technique pour la construction du pipeline multimodal de CheckIt.AI.

# 14. Bibliographie et ressources documentaires

Les ressources suivantes ont été consultées pour identifier les sources, examiner leurs formats et comprendre leurs méthodes d'accès.

## 14.1 Fakeddit

- Nakamura, K., Levy, S. et Yang Wang, W. (2020). *r/Fakeddit: A New Multimodal Benchmark Dataset for Fine-grained Fake News Detection*. LREC 2020.
- Article scientifique : https://arxiv.org/abs/1911.03854
- Site du projet : https://fakeddit.netlify.app/
- Dépôt GitHub : https://github.com/entitize/Fakeddit
- Ressource LREC : https://aclanthology.org/2020.lrec-1.755/

## 14.2 FakeNewsNet

- Dépôt GitHub officiel : https://github.com/KaiDMML/FakeNewsNet
- Documentation du dépôt : README et fichiers de configuration.
- Sources de vérification utilisées par le projet : GossipCop et PolitiFact.

## 14.3 NewsData.io

- Documentation officielle de l'API : https://newsdata.io/documentation
- Présentation des offres et des fonctionnalités : https://newsdata.io/pricing

## 14.4 CIMPLE Knowledge Graph

- Dépôt officiel du knowledge graph : https://github.com/CIMPLE-project/knowledge-base
- Point d'accès SPARQL : https://data.cimple.eu/sparql
- Dépôt des données ClaimReview : https://github.com/MartinoMensio/claimreview-data
- Version étudiée : `2026_11_02`
- Commit associé : `fb4c08dff60b968ebb449723b988e1b8c5cda84b`

## 14.5 Ressources méthodologiques complémentaires

- Google Dataset Search : https://datasetsearch.research.google.com/
- Hugging Face Datasets : https://huggingface.co/datasets
- Kaggle Datasets : https://www.kaggle.com/datasets
- Public APIs : https://github.com/public-apis/public-apis

## 14.6 Traçabilité de la version étudiée de CIMPLE

Archive analysée :

`data.claimreview-kg_2026_11_02.nt.gz`

Empreinte SHA-256 :

`afcdb40a734276c50791975ffb1754e2b981decacd4cd15f585947fd5fba1da2`

Cette empreinte permet de vérifier que le fichier utilisé lors de l'exploration correspond bien à l'archive analysée.

Les caractéristiques des offres commerciales et des API pouvant évoluer, les informations relatives aux quotas, aux tarifs et aux fonctionnalités devront être vérifiées à nouveau au moment de l'intégration.

# 15. Annexes techniques

## Annexe A — Analyse du fichier Fakeddit

Fichier examiné :

`raw/fakeddit/multimodal_train.tsv`

Format : TSV (valeurs séparées par des tabulations).

Caractéristiques observées :

| Indicateur | Résultat |
|---|---:|
| Nombre de publications | 564 000 |
| Nombre de colonnes | 16 |
| Titres manquants (`title`) | 0 |
| Titres nettoyés manquants (`clean_title`) | 0 |
| URL d'image manquantes (`image_url`) | 1 534 |
| Publications avec URL d'image renseignée | 562 466 |
| Taux d'URL d'image renseignées | 99,73 % |

La colonne `hasImage` indique `True` pour toutes les lignes, alors que 1 534 URL d'images sont absentes. Cette incohérence devra être prise en compte lors des contrôles qualité.

### Répartition des labels

**Label binaire (`2_way_label`) :**

| Valeur | Signification | Nombre |
|---|---|---:|
| 0 | Fake | 341 919 |
| 1 | True | 222 081 |

**Label à trois classes (`3_way_label`) :**

| Valeur | Signification | Nombre |
|---|---|---:|
| 0 | Fake with false text | 222 081 |
| 1 | Fake with true text | 13 848 |
| 2 | True | 328 071 |

**Label à six classes (`6_way_label`) :**

| Valeur | Signification | Nombre |
|---|---|---:|
| 0 | True | 222 081 |
| 1 | Satire/Parody | 33 481 |
| 2 | Misleading Content | 107 221 |
| 3 | Imposter Content | 11 784 |
| 4 | False Connection | 167 857 |
| 5 | Manipulated Content | 21 576 |

Ces distributions montrent que les classes sont déséquilibrées. Les futures évaluations devront donc utiliser des métriques adaptées, notamment le macro-F1 et le rappel par classe.

## Annexe B — Analyse de FakeNewsNet

Les quatre fichiers CSV examinés sont :

- `gossipcop_fake.csv`
- `gossipcop_real.csv`
- `politifact_fake.csv`
- `politifact_real.csv`

Les quatre fichiers présentent les colonnes suivantes :

| Colonne | Description |
|---|---|
| `id` | Identifiant de la publication |
| `news_url` | URL de l'article |
| `title` | Titre de l'article |
| `tweet_ids` | Identifiants des publications sociales associées |

Le label est déduit du nom du fichier et de la source de classification. Il n'existe pas de colonne de label explicite dans ces fichiers.

Le contenu intégral des articles et les images ne sont pas directement présents dans ces CSV. Leur récupération dépend de l'accessibilité des pages Web et des possibilités d'extraction.

## Annexe C — Analyse de CIMPLE Knowledge Graph

Version examinée :

`2026_11_02`

Format : N-Triples RDF compressé en gzip.

Archive :

`data.claimreview-kg_2026_11_02.nt.gz`

Taille annoncée : environ 13 Mo.

Empreinte SHA-256 :

`afcdb40a734276c50791975ffb1754e2b981decacd4cd15f585947fd5fba1da2`

### Types de ressources observés

| Type RDF | Nombre d'instances |
|---|---:|
| `schema:Rating` | 30 356 |
| `schema:ClaimReview` | 800 |
| `schema:Claim` | 800 |
| `schema:Organization` | 40 |

Ces comptages correspondent aux ressources typées observées dans l'archive examinée. Ils ne doivent pas être confondus avec les statistiques globales annoncées pour l'ensemble du knowledge graph.

### Répartition des verdicts observés

| Verdict | Nombre | Pourcentage |
|---|---:|---:|
| `not_credible` | 526 | 65,75 % |
| `credible` | 111 | 13,88 % |
| `uncertain` | 68 | 8,50 % |
| `not_verifiable` | 56 | 7,00 % |
| `mostly_credible` | 39 | 4,88 % |
| **Total** | **800** | **100 %** |

La présence de plusieurs catégories de verdict confirme l'intérêt de conserver les annotations détaillées plutôt que de les réduire immédiatement à deux classes.

### Langues déclarées

Les 800 ressources `ClaimReview` possèdent une propriété `schema:inLanguage`. Quinze valeurs de langue distinctes ont été observées.

Les cinq langues les plus représentées sont :

| Langue déclarée | Nombre |
|---|---:|
| English | 318 |
| Turkish | 173 |
| Slovak | 79 |
| Spanish | 72 |
| Portuguese | 38 |

Une incohérence a également été observée sur un exemple : le texte de vérification est en marathi alors que la propriété `schema:inLanguage` indique `English`. La langue devra donc être contrôlée plutôt que considérée comme toujours fiable.

### Association entre les ressources

L'analyse a permis d'observer les relations suivantes :

- `schema:ClaimReview` relie une vérification à une affirmation avec `schema:itemReviewed` ;
- `schema:reviewRating` relie une vérification à une ressource de notation ;
- `schema:author` permet de retrouver les organisations associées aux notations ;
- `schema:text` contient le texte de l'affirmation ou de la vérification ;
- `schema:datePublished` et `schema:url` apportent des informations de provenance.

Aucune propriété d'image parmi les prédicats recherchés (`schema:image`, `schema:thumbnailUrl`, `schema:associatedMedia`, `schema:contentUrl` et `foaf:depiction`) n'a été observée dans cette analyse. Cette observation ne permet toutefois pas d'exclure toute référence indirecte à un média.

## Annexe D — Limites des observations

Les résultats présentés dans ces annexes correspondent aux fichiers et aux versions effectivement examinés pendant l'exploration.

Ils ne constituent pas encore les résultats d'une collecte automatisée complète.

Les contrôles suivants restent à réaliser lors des prochaines étapes :

- mesure du taux réel de téléchargement des images ;
- vérification de la correspondance entre images et publications ;
- mesure de la disponibilité des articles FakeNewsNet ;
- évaluation des quotas et des réponses réelles de NewsData.io ;
- validation des rapprochements entre les publications et les vérifications CIMPLE ;
- contrôle des licences et des conditions d'utilisation avant toute redistribution.

