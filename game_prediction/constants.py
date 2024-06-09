import pathlib

# MLFLOW CONFIG
FILE_ROOT = "file://"
URI_PATH_DEFAULT = FILE_ROOT + str(pathlib.Path(__file__).parent.parent.resolve() / "mlruns")

EXPERIMENT_NAME = "game-prediction"

MODEL_NAME = "game-prediction-classifier"


# MODEL CONFIG
LABEL_CONVERTED = {"DRAW": 1, "HOME_WIN": 0, "AWAY_WIN": 2}
LABEL_CONVERTED_INV = {1: "DRAW", 0: "HOME_WIN", 2: "AWAY_WIN"}
