import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from game_prediction.pipelines.inference import inference
from game_prediction.tasks.scoring import load_run_mlflow

ml_models = {}


class ModelConfig(BaseModel):  # type: ignore
    """Inputs to run model."""

    home_team: str = "MARSEILLE"
    away_team: str = "NANTES"


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Loading the model once so it's available for all API request."""
    # Load the ML model
    ml_models["xgb_model"] = load_run_mlflow()
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


@app.get("/")  # type: ignore
async def root() -> str:
    """Root endpoint."""
    return os.getcwd()


@app.post("/predict")  # type: ignore
async def get_prediction(game: ModelConfig) -> dict[str, str]:
    """Get the model prediction for the requested game.

    Args:
        game (ModelConfig): Model inputs.

    Returns:
        dict[str, str]: Model result (prediction of game's result).
    """
    result = inference(game.home_team, game.away_team, loaded_model=ml_models["xgb_model"])
    return {"PREDICTION": result}
