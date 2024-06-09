from typing import Any

import mlflow
import xgboost as xgb
from mlflow.models.signature import ModelSignature

import game_prediction.constants as cst


# Create a new MLflow Experiment
def save_to_mlflow(
    my_model: xgb.XGBClassifier,
    model_signature: ModelSignature,
    model_report: dict[str, Any],
    model_report_random: dict[str, Any],
) -> None:
    """Save the model to MLFlow.

    Args:
        my_model (xgb.XGBClassifier): Fitted model.
        model_signature (_type_): MLFlow model signature.
        model_report (dict[str, Any]): Model results (classification report from Sklearn)
        model_report_random (dict[str, Any]): Dummy model results (classification report from Sklearn)
    """

    mlflow.set_tracking_uri(uri=cst.URI_PATH_DEFAULT)

    mlflow.set_experiment(experiment_name=cst.EXPERIMENT_NAME)

    with mlflow.start_run():  #
        for label in ["0", "1", "2"]:
            [mlflow.log_metric(f"{key}_{label}", val) for key, val in model_report[label].items()]

        for label in ["0", "1", "2"]:
            [mlflow.log_metric(f"RANDOM_{key}_{label}", val) for key, val in model_report_random[label].items()]

        clf_params = my_model.get_xgb_params()
        mlflow.log_params(clf_params)

        mlflow.xgboost.log_model(my_model, cst.MODEL_NAME, signature=model_signature)

    mlflow.end_run()
