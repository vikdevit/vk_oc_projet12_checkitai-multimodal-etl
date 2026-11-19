# Schéma conceptuel des données — CheckIt.AI

## 1. Objectif

Le modèle conceptuel décrit les données exploitées par CheckIt.AI pour
la détection et l'analyse de contenus potentiellement trompeurs ou faux.

Il regroupe les informations issues de quatre sources :
Fakeddit, FakeNewsNet, NewsData.io et CIMPLE.

Le modèle est indépendant du système de stockage qui sera choisi
ultérieurement.

Le diagramme associé est disponible dans :
`diagrams/schema_conceptuel.mmd`.

## 2. Entités et attributs

### 2.1 SOURCE

Représente l'origine des données.

| Attribut | Type logique | Description |
|---|---|---|
| source_name | string | Identifiant du nom de la source |
| source_category | string | Catégorie ou famille de la source |
| description | string | Description de la source |

Une source peut fournir plusieurs enregistrements.

### 2.2 CONTENT_RECORD

Représente une publication, un article ou un contenu à analyser.
C'est l'entité centrale du modèle.

| Attribut | Type logique | Description |
|---|---|---|
| publication_id | string | Identifiant unique du contenu |
| source_name | string | Référence vers la source d'origine |
| title | string | Titre ou texte court du contenu |
| text_content | string | Texte intégral lorsqu'il est disponible |
| published_at | datetime | Date de publication, si connue |
| collected_at | datetime | Date de collecte |
| language | string | Langue du contenu |
| article_url | string | Adresse de l'article ou de la publication |
| has_text | boolean | Indique la présence d'un titre ou d'un texte |
| transformation_status | string | Résultat de la transformation |
| source_metadata | json | Métadonnées spécifiques à la source |

Le titre et le texte intégral sont distingués : un enregistrement
peut avoir un titre sans disposer du corps complet de l'article.

### 2.3 IMAGE_ASSET

Représente une image explicitement associée à un contenu.

| Attribut | Type logique | Description |
|---|---|---|
| publication_id | string | Référence vers le contenu associé |
| image_url | string | Adresse distante de l'image |
| image_path | string | Chemin local du fichier téléchargé |
| image_valid | boolean | Résultat de la validation de l'image |
| image_status | string | État de disponibilité de l'image |

Valeurs possibles de image_status dans le pipeline :
- downloaded : fichier image présent localement et reconnu comme téléchargé ;
- url_only : URL disponible, sans fichier local ;
- missing : aucune URL ni image locale ;
- invalid : fichier local absent ou image considérée invalide.

Une image est associée à un contenu uniquement par son
publication_id. Une proximité dans un fichier ne suffit jamais
à établir une association.

### 2.4 LABEL_ASSESSMENT

Représente une qualification ou une évaluation associée au contenu.

| Attribut | Type logique | Description |
|---|---|---|
| publication_id | string | Référence vers le contenu évalué |
| label_value | string | Valeur du label |
| label_type | string | Nature du label : binary, fact_check ou unlabeled |
| label_source | string | Origine de la qualification |
| label_status | string | Statut de disponibilité du label |
| fact_check_url | string | Adresse de la vérification factuelle |
| source_labels | json | Labels et informations originales de la source |

Les catégories de labels sont conservées sans fusion abusive.
Les valeurs incertaines et non vérifiables restent distinctes
des verdicts crédible et non crédible.

Une absence de label reste une valeur manquante :
elle n'est jamais interprétée comme une vérité.

## 3. Relations et cardinalités

- SOURCE vers CONTENT_RECORD : une source peut fournir zéro à
  plusieurs contenus ; chaque contenu provient d'une source.
- CONTENT_RECORD vers IMAGE_ASSET : un contenu peut être associé
  à zéro ou une image dans le modèle actuel.
- CONTENT_RECORD vers LABEL_ASSESSMENT : un contenu peut disposer
  de zéro ou une évaluation dans le modèle actuel.

Les associations entre entités utilisent publication_id et
source_name comme références logiques.

## 4. Alignement avec les usages de l'IA

Le modèle permet de préparer des données pour plusieurs usages :

- NLP : analyse du titre et du texte disponible.
- Analyse multimodale : mise en relation explicite du texte et
  de l'image associée.
- Classification : exploitation des labels disponibles en
  conservant leur provenance et leur nature.
- Enrichissement : utilisation des métadonnées et des
  vérifications factuelles.
- Traçabilité : conservation de la source et des informations
  de collecte.

Les contenus sans image ou sans label restent conservés.
Ils ne sont pas artificiellement complétés.

## 5. Limites et choix de modélisation

Le modèle décrit la structure logique actuelle du projet.

Il prévoit au maximum une image et une évaluation par contenu.
Cette cardinalité pourra évoluer si le projet doit gérer plusieurs
images ou plusieurs évaluations pour une même publication.

Le modèle conceptuel ne fixe pas de technologie de stockage,
de type SQL, d'index ou de stratégie physique.

Ces choix relèveront du schéma technique et physique.

## 6. Fichier du diagramme

Diagramme Mermaid : `diagrams/schema_conceptuel.mmd`.
