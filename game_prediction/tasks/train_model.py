import pandas as pd
import xgboost as xgb
from mlflow.models import infer_signature
from mlflow.models.signature import ModelSignature


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> tuple[xgb.XGBClassifier, ModelSignature]:
    """Simple model training.

    Args:
        X_train (pd.DataFrame): Explicative variables.
        y_train (pd.Series): Target

    Returns:
        xgb.XGBClassifier: Fitted model.
    """
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)

    signature = infer_signature(X_train, model.predict(X_train))

    return model, signature
