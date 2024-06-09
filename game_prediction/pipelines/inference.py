from typing import Union

import xgboost as xgb

import game_prediction.constants as cst
from game_prediction.tasks.prepare_data import build_final_data, load_data
from game_prediction.tasks.scoring import load_run_mlflow, prepare_data_inference


def inference(
    home_team: str, away_team: str, load_model: bool = False, loaded_model: Union[None, xgb.XGBClassifier] = None
) -> str:
    """Run model (interfaced through API)

    Args:
        home_team (str): Home team of the match to predict.
        away_team (str): Away team of the match to predict.
        load_model (bool, optional): load model from mlflow registry. Defaults to False.
        loaded_model (Union[None, xgb.XGBClassifier], optional): use pre existing model. Defaults to None.

    Returns:
        str: Model prediction.
    """

    # mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

    home_team, away_team = "MARSEILLE", "NANTES"

    if load_model:
        loaded_model = load_run_mlflow()

    table_query = f"""SELECT *
                FROM game_data
                WHERE "TEAM" IN ('{home_team}', '{away_team}');
                """
    inference_data = load_data(table_query)

    inference_data = build_final_data(inference_data)

    inference_data = prepare_data_inference(inference_data, home_team, away_team)

    prediction = loaded_model.predict(inference_data.drop(["ID_GAME", "TARGET"], axis=1))[0]  # type: ignore

    return cst.LABEL_CONVERTED_INV[prediction]


if __name__ == "__main__":
    inference("MARSEILLE", "NANTES", load_model=True)
