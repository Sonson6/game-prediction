from typing import Any

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import classification_report


def evaluate_model(model: xgb.XGBClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> Any:
    """Build classification report from Sklearn.

    Args:
        model (xgb.XGBClassifier): Fitted model.
        X_test (pd.DataFrame): Explicative variable from test sample.
        y_test (pd.Series): Target from test sample.

    Returns:
        Any: Classification report from Sklearn.

    """
    print(classification_report(y_test, model.predict(X_test)))

    return classification_report(y_test, model.predict(X_test), output_dict=True)


# Random comparison
def evaluate_random_model(y_test: pd.Series) -> Any:
    """Use true target distribution to produce a fake random prediction,
            useful to compare our model with dummy results.

    Args:
        y_test (pd.Series): True target distribution.

    Returns:
        Any: Dummy prediction's classification report.
    """
    y_test_distrib = y_test.value_counts(True)
    y_random = np.random.choice(
        np.arange(0, 3), p=[y_test_distrib[0], y_test_distrib[1], y_test_distrib[2]], size=len(y_test)
    )

    print(classification_report(y_test, y_random))

    return classification_report(y_test, y_random, output_dict=True)
