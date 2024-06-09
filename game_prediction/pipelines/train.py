from game_prediction.tasks.model_performance import evaluate_model, evaluate_random_model
from game_prediction.tasks.prepare_data import build_final_data, load_data, prepare_data_model, split_data
from game_prediction.tasks.saving import save_to_mlflow
from game_prediction.tasks.train_model import train_model


def train() -> None:
    """Load data from PostGresSQL, run feature engineering
    and train a XGBoost model before saving to MLFlow.
    """

    game_data = load_data()

    game_data = build_final_data(game_data)

    df_model_final = prepare_data_model(game_data)

    X_train, X_test, y_train, y_test = split_data(df_model_final)

    model_fitted, signature = train_model(X_train, y_train)

    model_report = evaluate_model(model_fitted, X_test, y_test)

    model_report_random = evaluate_random_model(y_test)

    save_to_mlflow(model_fitted, signature, model_report, model_report_random)


# mlflow server --host 127.0.0.1 --port 8080
# Set our tracking server uri for logging

if __name__ == "__main__":
    train()
