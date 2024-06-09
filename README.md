# Football Game Result Prediction

This repository provides a solution for predicting football game results. The package leverages various tools and frameworks including Scikit-learn, MLflow, FastAPI, Streamlit, and Docker. It encompasses the entire machine learning lifecycle, from data loading and preprocessing to model training, saving, and deployment.

### Steps of the solution

* Load data from a PostgreSQL database
* Preprocess data using Pandas and Scikit-learn
* Train a model using XGBoost
* Save the trained model to MLflow registry
* Serve model inference using FastAPI
* Interface the FastAPI application with a Streamlit front-end
* Dockerized environment for seamless deployment
* Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/game-prediction.git
cd game-prediction
```

## Set up a virtual environment and install dependencies

Before running any script, you will need your own version of the required database, using another repository : https://github.com/Sonson6/football-analytics.git

Once you have it, you must create a .env file in the repository and fill the following variables :

```bash
DATABASE_USER=your_postgres_username
DATABASE_PASSWORD=your_postgres_password
DATABASE_HOST=host.docker.internal # no need to touch it if being run locally
DATABASE_NAME=your_database_name
```

Now, you can install the dependencies :

```bash
poetry install
```

Train your own model :

```bash
poetry run game_prediction/train.py
```

Finally, you can create the Docker image and run the containers :

```bash
docker compose up --build
```

Now, you can play with the Streamlit interface to get model predictions (will be accessible through http://localhost:8501).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or features.
