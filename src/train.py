import hashlib
import json
import os
from io import BytesIO
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import average_precision_score, make_scorer
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

DATA_PATH = Path("data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv")
TARGET = "Machine failure"
FEATURES = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
POSITIVE_LABEL = 1


def split_dataset(data):
    target = data[TARGET]
    return train_test_split(
        data[FEATURES],
        target,
        test_size=TEST_SIZE,
        stratify=target,
        random_state=RANDOM_STATE,
    )


def main():
    csv_bytes = DATA_PATH.read_bytes()
    data = pd.read_csv(BytesIO(csv_bytes), encoding="utf-8-sig")
    X_dev, _, y_dev, _ = split_dataset(data)

    model = DummyClassifier(strategy="prior")
    folds = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    scorer = make_scorer(
        average_precision_score, response_method="predict_proba", pos_label=POSITIVE_LABEL
    )
    scores = cross_val_score(model, X_dev, y_dev, cv=folds, scoring=scorer)
    mean_ap = float(scores.mean())

    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
    mlflow.set_experiment("ai4i-failure-detection")
    with mlflow.start_run(run_name="baseline-prior") as run:
        mlflow.log_params(
            {
                "classifier": type(model).__name__,
                "strategy": model.strategy,
                "target": TARGET,
                "features": json.dumps(FEATURES),
                "positive_label": POSITIVE_LABEL,
                "random_state": RANDOM_STATE,
                "test_size": TEST_SIZE,
                "split_stratified": True,
                "cv_splitter": type(folds).__name__,
                "cv_folds": folds.n_splits,
                "cv_shuffle": folds.shuffle,
                "dataset_path": DATA_PATH.as_posix(),
                "dataset_sha256": hashlib.sha256(csv_bytes).hexdigest(),
            }
        )
        mlflow.log_metrics(
            {
                "failure_prevalence": float(data[TARGET].eq(POSITIVE_LABEL).mean()),
                "cv_average_precision_mean": mean_ap,
            }
        )

    print(f"Run MLflow {run.info.run_id} | Average Precision moyenne : {mean_ap:.6f}")


if __name__ == "__main__":
    main()
