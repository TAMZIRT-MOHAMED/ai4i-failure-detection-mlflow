# Détection de défaillances industrielles avec suivi des expériences MLflow

**Auteurs · Salma SAID et Mohamed TAMZIRT**

Le mini-projet vise à détecter une défaillance au moment de l’observation. Nous comparerons plusieurs classifieurs, suivrons leurs paramètres et leurs métriques dans MLflow, puis sauvegarderons le pipeline retenu.

Le jeu de données synthétique UCI AI4I 2020 contient 10 000 observations, dont 339 défaillances. La cible binaire est `Machine failure`. Les six entrées sont le type de produit, les températures de l’air et du procédé, la vitesse de rotation, le couple et l’usure de l’outil. Les identifiants et les indicateurs `TWF`, `HDF`, `PWF`, `OSF` et `RNF` sont exclus des entrées. Le CSV, son empreinte et sa licence sont décrits dans la [documentation des données](data/README.md).

## Reproduire l’expérience sous Ubuntu

Utiliser **Python 3.12** (fourni par Ubuntu 24.04). Si Python ou le module `venv` manque sur Ubuntu 24.04, installer les paquets avec `sudo apt install python3.12 python3.12-venv`. Depuis la racine du dépôt cloné, créer l’environnement et installer les dépendances épinglées. Les commandes ci-dessous fonctionnent dans Bash et fish en appelant directement les exécutables de l’environnement.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Pour activer l’environnement dans le terminal, utiliser `source .venv/bin/activate.fish` sous fish ou `source .venv/bin/activate` sous Bash.

Dans ce terminal, démarrer le serveur MLflow local.

```bash
.venv/bin/mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5001
```

Dans un deuxième terminal, depuis la racine du dépôt, lancer la référence.

```bash
env MLFLOW_TRACKING_URI=http://127.0.0.1:5001 .venv/bin/python -m src.train
```

Ouvrir l’expérience `ai4i-failure-detection`, puis le run `baseline-prior`. Sa fiche affiche `cv_average_precision_mean`, `failure_prevalence` et les paramètres, dont `dataset_sha256`. [Interface MLflow](http://127.0.0.1:5001)

La commande `.venv/bin/python -m src.train` utilise directement la base SQLite locale `mlflow.db` lorsque `MLFLOW_TRACKING_URI` est absente. Pour utiliser un serveur partagé, remplacer l’URL de `MLFLOW_TRACKING_URI` par celle du serveur.

Pour explorer les données de développement, ouvrir le notebook depuis la racine.

```bash
.venv/bin/python -m notebook exploration.ipynb
```

## Résultat obtenu

La séparation stratifiée avec `random_state=42` réserve 2 000 observations (20 %) au test final. Sur les 8 000 observations de développement, `DummyClassifier(strategy="prior")` est évalué avec cinq plis stratifiés, mélangés avec la même graine. Le calcul de l’Average Precision utilise les probabilités de la classe `1` (défaillance).

Le run `baseline-prior` a obtenu une Average Precision moyenne de **0,033875** sur les cinq plis. La proportion de défaillances est de **3,39 %** sur l’ensemble du CSV.

## Travaux prévus

Comparer une régression logistique et une forêt aléatoire sur les mêmes plis de développement, puis sélectionner le modèle selon l’Average Precision moyenne. Évaluer le pipeline retenu sur le jeu de test réservé, le sauvegarder dans MLflow et vérifier son rechargement.

## Première publication sur GitHub

La création du dépôt utilise GitHub CLI, dont l’exécutable est `gh`. Sous Ubuntu, installer l’outil avec `sudo apt install gh` si nécessaire. Authentifier le compte dans le navigateur.

```bash
gh auth login --hostname github.com --git-protocol https --web
```

Lorsque le dépôt local est prêt et sans remote `origin`, créer le dépôt privé sur le compte authentifié et pousser les commits depuis la racine.

```bash
gh repo create ai4i-failure-detection-mlflow --private --source=. --remote=origin --push
```

Consulter l’URL et la visibilité avec `gh repo view --json url,visibility`. [Documentation GitHub CLI](https://cli.github.com/manual/gh_repo_create)
