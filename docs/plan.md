# Plan de travail du mini-projet AI4I et MLflow

**Binôme** · Salma SAID et Mohamed TAMZIRT

## État du dépôt

- **Réalisé.** Le CSV AI4I contient 10 000 observations, dont 339 défaillances. Le script réserve 20 % des observations au test final et applique cinq plis stratifiés avec la graine 42. Les deux runs `baseline-prior` examinés dans la base MLflow locale sont terminés et donnent **0,033875** d’Average Precision moyenne avec `DummyClassifier(strategy="prior")`. [Données](../data/README.md) · [Script d’entraînement](../src/train.py)
- **Commencé.** Le notebook compte 271 défaillances parmi les 8 000 observations de développement et relève zéro valeur manquante dans les six entrées. Le suivi MLflow local est opérationnel et son lancement est documenté. [Notebook](../exploration.ipynb) · [README](../README.md)
- **À faire.** Compléter l’analyse, entraîner et comparer les pipelines de régression logistique et de forêt aléatoire, puis évaluer, sauvegarder et recharger le pipeline retenu pour la démonstration.

## Issues GitHub proposées

| Issue GitHub | Responsable | Dépend de | Livrable vérifiable | Effort estimé |
| --- | --- | --- | --- | --- |
| 1. **Fixer le protocole commun de validation** | Binôme | — | Une fiche versionnée fixe la cible `Machine failure`, les six entrées de `FEATURES`, le découpage stratifié 80/20, les cinq plis et la graine 42. Les deux ordinateurs retrouvent les mêmes indices de plis depuis le même CSV. La fiche indique l’Average Precision moyenne comme critère de sélection, le seuil de 0,5 pour la précision et le rappel, et le format de nommage `famille-variante-initiales`. | 1 h 30 chacun |
| 2. **Compléter l’analyse des données de développement** | Salma | 1 | Le notebook s’exécute de bout en bout et présente les distributions des six entrées par classe, les effectifs et les valeurs manquantes. Salma partage une synthèse des choix de prétraitement avec Mohamed. | 2 h |
| 3. **Configurer un suivi MLflow commun** | Mohamed | 1 | Chacun enregistre un run d’essai depuis son ordinateur et voit les deux runs dans l’expérience `ai4i-failure-detection` sur le même serveur local. Mohamed fournit à Salma l’adresse de suivi et un exemple de journalisation des paramètres et métriques. | 2 h 30 |
| 4. **Construire le pipeline de régression logistique** | Salma | 1, 2 | Le pipeline encode `Type` et standardise les cinq mesures. Un essai sur un pli montre que le prétraitement est ajusté sur les observations d’entraînement du pli et que le pipeline produit les probabilités de la classe `1` sur sa partie validation. | 3 h |
| 5. **Évaluer et interpréter les forêts aléatoires** | Mohamed | 1, 3 | Au moins deux configurations de forêt, chacune avec son pipeline, sont enregistrées dans MLflow sur les cinq plis communs. Mohamed remet les identifiants des runs, les métriques par pli et une lecture des fausses alertes et des pannes manquées. | 3 h 30 |
| 6. **Évaluer et interpréter les régressions logistiques** | Salma | 3, 4 | Au moins deux configurations de régression logistique sont enregistrées dans la même expérience sur les cinq plis communs. Salma remet les identifiants des runs, les métriques par pli et sa lecture des fausses alertes et des pannes manquées. | 3 h |
| 7. **Sélectionner le modèle sur les résultats de validation** | Binôme | 5, 6 | Un tableau compare la référence et les deux familles par Average Precision moyenne et écart-type sur les cinq plis. La décision consigne le run retenu, ses paramètres et le seuil retenu, avec une lecture de la précision et du rappel. | 1 h 30 chacun |
| 8. **Réentraîner, évaluer et sauvegarder le pipeline final** | Binôme | 7 | Le pipeline retenu est réentraîné sur les 8 000 observations de développement et évalué une fois sur les 2 000 observations réservées. Le run final contient l’Average Precision, la précision, le rappel, la matrice de confusion et l’URI du pipeline sauvegardé dans MLflow. | 2 h chacun |
| 9. **Vérifier le rechargement du pipeline** | Mohamed | 8 | Depuis le second ordinateur et dans une nouvelle session Python, le script recharge le pipeline par son URI MLflow et retrouve les mêmes classes et probabilités sur cinq observations de développement, à la tolérance numérique convenue. | 2 h |
| 10. **Répéter la démonstration du binôme** | Binôme | 8, 9 | Une répétition montre les runs dans MLflow, justifie le choix à partir de la validation, présente le résultat sur le test final et se termine par une prédiction avec le pipeline rechargé. | 1 h 30 chacun |

## Résultats à échanger

Les pipelines prennent en entrée `Type` et les cinq mesures de fonctionnement. Les identifiants `UDI` et `Product ID` et les indicateurs `TWF`, `HDF`, `PWF`, `OSF` et `RNF` sont exclus de la liste `FEATURES`. [Liste des entrées](../src/train.py#L14-L22)

Salma transmet ses choix de prétraitement à Mohamed, qui lui fournit l’adresse du serveur MLflow commun et les noms de paramètres et de métriques à employer. Pour chaque configuration, chacun remet l’identifiant du run, le commit, l’empreinte du CSV, les hyperparamètres et les résultats des cinq plis dans le même ordre. L’Average Precision se calcule à partir des probabilités de la classe `1`. La précision, le rappel et les comptes de fausses alertes et de pannes manquées se rapportent au seuil convenu.

Le suivi cloud reste une extension facultative après la démonstration, si le suivi local couvre le cahier des charges.

## Démarrage et charge

Après le jalon commun **#1**, Salma commence l’analyse **#2** pendant que Mohamed configure le suivi **#3**. Ils réunissent leurs résultats dès que les issues **#5 et #6** sont terminées pour choisir le modèle au jalon **#7**, avant d’ouvrir le jeu de test.

Salma et Mohamed ont chacun **14 h 30** de travail estimé, dont **8 h individuelles** et **6 h 30 en binôme**, hors extension cloud.
