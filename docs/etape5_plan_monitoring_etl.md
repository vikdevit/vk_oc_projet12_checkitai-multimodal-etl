# Plan de monitoring et de supervision du pipeline ETL CheckIt.AI

## 1. Objectifs

Ce plan définit les modalités de surveillance du pipeline ETL multimodal CheckIt.AI.
Il vise à garantir :

- la fiabilité des extractions depuis les différentes sources ;
- la qualité et la complétude des données transformées ;
- la bonne exécution des traitements Airflow ;
- la disponibilité et l'intégrité de la base SQLite ;
- la maîtrise des ressources de stockage et des temps de traitement.

Le tableau de bord Streamlit (`dashboard/app.py`) centralise les principaux indicateurs de qualité, de volume, de stockage et de performance.

## 2. Architecture supervisée

Le périmètre de supervision comprend :

1. **Extraction** : connecteurs Fakeddit, FakeNewsNet, NewsData.io et CIMPLE Knowledge Graph.
2. **Transformation** : nettoyage, normalisation et validation des données.
3. **Orchestration** : DAG Airflow `checkitai_etl_pipeline`.
4. **Stockage** : base SQLite `checkitai.db`.
5. **Visualisation** : tableau de bord Streamlit.

Les journaux et rapports sont conservés dans le répertoire de données du projet :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/logs/`

Les rapports de contrôle sont stockés dans :

`/mnt/data/vk_oc_projet12_checkitai-multimodal-etl/reports/`

## 3. Indicateurs et seuils d'alerte

Les seuils ci-dessous constituent une première politique de surveillance. Ils devront être ajustés à partir de l'historique des exécutions et des volumes habituels.

| Domaine | Indicateur | Seuil | Niveau |
|---|---|---|---|
| Orchestration | Échec d'une tâche Airflow | Toute tâche en échec | Critique |
| Orchestration | Durée totale du DAG | Plus de 15 minutes | Avertissement |
| Qualité | Taux d'enregistrements rejetés | Supérieur à 1 % | Avertissement |
| Complétude | Publications avec texte | Inférieur à 98 % | Avertissement |
| Extraction | Source attendue sans nouvel enregistrement | Sur une exécution | Avertissement |
| Stockage | Espace disque disponible | Inférieur à 15 % | Avertissement |
| Stockage | Espace disque disponible | Inférieur à 10 % | Critique |
| Base de données | Résultat du contrôle d'intégrité SQLite | Différent de `ok` | Critique |

### Précisions sur l'interprétation des indicateurs

- Une URL d'image ne signifie pas que l'image a été téléchargée ou validée.
- L'absence d'image est attendue pour certaines sources, notamment FakeNewsNet et CIMPLE. Elle ne doit donc pas déclencher seule une alerte globale.
- NewsData.io ne fournit pas nécessairement de label de véracité. Une donnée sans label n'est pas automatiquement une donnée invalide.
- Les labels issus des sources ne constituent pas une mesure de vérité universelle. La qualité technique des données doit être distinguée de l'exactitude factuelle.
- Le projet est exécuté sur une infrastructure locale : aucun coût cloud réel n'est calculé. La taille de la base, l'espace disque et les durées de traitement servent d'indicateurs indirects de consommation des ressources.

## 4. Fréquence des contrôles

| Contrôle | Fréquence | Moyen de contrôle |
|---|---|---|
| État des tâches et du DAG | À chaque exécution | Interface Airflow et historique des exécutions |
| Journaux d'extraction | À chaque exécution | Fichiers de logs des connecteurs |
| Enregistrements transformés et rejetés | À chaque exécution | Rapport de transformation JSON |
| Complétude et disponibilité des images | À chaque actualisation du tableau de bord | Dashboard Streamlit et base SQLite |
| Performance du pipeline | À chaque exécution | Historique Airflow et dashboard |
| Intégrité SQLite | Quotidienne et après incident de chargement | `PRAGMA integrity_check` |
| Espace disque | Quotidienne | Surveillance du système hôte |
| Revue globale des KPI | Hebdomadaire | Dashboard et rapports historiques |

Le tableau de bord Streamlit actualise ses données toutes les 60 secondes lorsque l'application est ouverte.

## 5. Gestion des erreurs et procédure de reprise

### 5.1 Échec d'une extraction

1. Identifier le connecteur concerné dans l'interface Airflow.
2. Consulter les logs de la tâche correspondante.
3. Vérifier la disponibilité de la source distante, les paramètres de connexion et les éventuelles limitations d'API.
4. Corriger la cause de l'incident.
5. Relancer la tâche ou l'exécution depuis Airflow.
6. Vérifier la présence des fichiers attendus et du rapport d'extraction.

Pour NewsData.io, contrôler également la disponibilité du service et le quota de crédits API.

### 5.2 Échec de transformation

1. Consulter le log de transformation.
2. Identifier les données ou les champs à l'origine de l'erreur.
3. Vérifier les règles de normalisation et de validation.
4. Corriger le traitement si nécessaire.
5. Relancer la transformation.
6. Contrôler les volumes transformés et rejetés ainsi que le rapport JSON.

### 5.3 Échec du chargement SQLite

1. Consulter les logs de la tâche `load_data`.
2. Vérifier l'accès au fichier de base de données et l'espace disque disponible.
3. Contrôler les contraintes et la cohérence des données.
4. Exécuter un contrôle d'intégrité SQLite.
5. Ne pas supprimer ou remplacer la base existante sans sauvegarde préalable.
6. Après correction, relancer le chargement et vérifier les volumes enregistrés.

### 5.4 Dépassement des seuils de ressources

En cas de manque d'espace disque :

1. Identifier le système de fichiers concerné.
2. Identifier les fichiers volumineux et les journaux anciens.
3. Vérifier les possibilités d'archivage ou de nettoyage des fichiers temporaires.
4. Ne supprimer aucune donnée métier ni base active sans sauvegarde et validation.

## 6. Journalisation et traçabilité

Chaque composant doit produire des informations permettant de comprendre le déroulement du traitement :

- date et heure de l'opération ;
- nom de la source ou de la tâche ;
- nombre d'enregistrements traités ;
- nombre d'enregistrements rejetés, le cas échéant ;
- statut de l'opération ;
- message d'erreur en cas d'échec.

Les journaux applicatifs et rapports JSON permettent de diagnostiquer les incidents et de comparer les exécutions.

Les informations sensibles, notamment les clés API, ne doivent jamais être écrites dans les logs.

Les bases de données et fichiers de rapports doivent faire l'objet de sauvegardes régulières adaptées à leur criticité.

## 7. Alertes et communication

Dans la configuration actuelle du projet, Airflow conserve l'état des tâches et leurs journaux, tandis que Streamlit présente les indicateurs de suivi.

Les alertes sont identifiées par consultation de l'interface Airflow, du tableau de bord et des journaux. L'envoi automatique de notifications externes (courriel ou messagerie) n'est pas encore configuré.

Pour une mise en production, il est recommandé de compléter le dispositif par :

- des notifications automatiques en cas d'échec du DAG ;
- des alertes en cas de dépassement des seuils de qualité ou de ressources ;
- une centralisation des journaux ;
- une procédure d'escalade et une personne responsable de la résolution.

## 8. Sécurité et continuité

- Limiter les accès aux fichiers de données et à la base SQLite.
- Conserver les secrets dans le fichier d'environnement non versionné.
- Ne pas exposer directement les interfaces Airflow et Streamlit sur Internet sans authentification et protection adaptées.
- Sauvegarder régulièrement la base SQLite et les rapports importants.
- Vérifier périodiquement la capacité de restauration des sauvegardes.

## 9. Limites et évolutions possibles

Le dispositif actuel constitue une supervision adaptée au prototype CheckIt.AI et à son infrastructure locale.

Les évolutions recommandées pour une exploitation à plus grande échelle sont :

- automatiser les alertes et notifications ;
- enrichir l'historique des KPI pour identifier les tendances ;
- mesurer la consommation CPU, mémoire et espace disque ;
- suivre les quotas et coûts des services externes ;
- mettre en place une sauvegarde automatisée et tester les restaurations ;
- définir des objectifs de disponibilité et de temps de reprise.

## 10. Conclusion

Le dispositif associe l'orchestration Airflow, les journaux applicatifs, les rapports de transformation, les contrôles SQLite et le tableau de bord Streamlit.

Il permet de suivre la qualité des données, la fiabilité des traitements, les performances et les ressources de stockage. Les seuils définis fournissent une première base opérationnelle pour détecter les anomalies et organiser leur résolution.

