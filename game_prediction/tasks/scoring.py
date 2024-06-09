import os
from typing import Union

import mlflow.xgboost
import pandas as pd
import xgboost as xgb

import game_prediction.constants as cst
from game_prediction.tasks.prepare_data import prepare_data_model


def load_run_mlflow(get_metric: bool = False) -> Union[dict[str, float], xgb.XGBClassifier]:
    """Load required run from MLFlow registry to extract its metrics or the model itself.

    Args:
        get_metric (bool, optional): Extract the metrics of the run if needed. Defaults to False.

    Returns:
        Union[dict[str, float], xgb.XGBClassifier]: Extract the model artifacts of the run.
    """

    mlflow.set_tracking_uri(uri=cst.URI_PATH_DEFAULT)

    # Get latest run ID from the experiment called EXPERIMENT_NAME
    current_experiment = dict(mlflow.get_experiment_by_name(cst.EXPERIMENT_NAME))
    experiment_id = current_experiment["experiment_id"]
    run_id = mlflow.search_runs(experiment_id)

    if get_metric:
        metric_cols = [
            col
            for col in run_id.columns
            if (col.startswith("metrics.") and ("RANDOM" not in col) and ("support" not in col))
        ]

        metrics = run_id[metric_cols]

        return round(metrics, 3).to_dict(orient="index")[0]

    else:
        run_id = run_id["run_id"][0]
        # Load the model matching run ID
        model_uri = os.path.join(cst.URI_PATH_DEFAULT, f"{experiment_id}/{run_id}/artifacts/{cst.MODEL_NAME}")
        loaded_model = mlflow.xgboost.load_model(model_uri)

        return loaded_model


def prepare_data_inference(df: pd.DataFrame, home_team: str, away_team: str) -> pd.DataFrame:
    """Prepare dataset for inference by removing all rows that are not matching the last HOME and AWAY team game.

    Args:
        df (pd.DataFrame): Dataset for inference.
        home_team (str): Home team of the match to predict.
        away_team (str): Away team of the match to predict.

    Returns:
        pd.DataFrame: _description_
    """
    home_condition = (df["TEAM"] == home_team) & (df["STATUS"] == "HOME")
    away_condition = (df["TEAM"] == away_team) & (df["STATUS"] == "AWAY")

    df = df[home_condition | away_condition].drop_duplicates("TEAM", keep="last")

    df["ID_GAME"] = f"{home_team}_{away_team}"

    return prepare_data_model(df)
