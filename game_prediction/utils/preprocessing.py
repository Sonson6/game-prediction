from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from game_prediction.config import TableDefinition


def process_perc_and_abs_columns(game_data: pd.DataFrame, table_mapper: TableDefinition) -> pd.DataFrame:
    """Process columns with "%" in the name and treat columns with string in the value.

    Args:
        game_data (pd.DataFrame): General game statistics table.
        table_mapper (TableDefinition): Table variables.

    Returns:
        game_data: Preprocessed game data tabl.
    """

    # PROCESS PERCENTAGE
    perc_cols = [col for col in game_data.columns if col.endswith("%")]

    for col in perc_cols:
        game_data[col] = np.where(game_data[col] == "%", "0%", game_data[col])
        game_data[col] = game_data[col].str[:-1].astype(float) / 100

    # PROCESS ABSOLUTE STATISTICS
    abs_cols = [
        table_mapper.wk_columns()["PASS_ACC"]["name"],
        table_mapper.wk_columns()["SOT"]["name"],
        table_mapper.wk_columns()["SAVES"]["name"],
    ]

    for col in abs_cols:
        game_data[col] = game_data[col].str.split("of").str[0].str.strip()  # .astype(int)

    return game_data


def pre_processing_game_data(df: pd.DataFrame, table_mapper: TableDefinition) -> pd.DataFrame:
    """Pre process game data table, most particularly creates target.

    Args:
        df (pd.DataFrame): General game statistics table.
        table_mapper (TableDefinition): Table variables.

    Returns:
        _type_: Preprocessed game data tabl.
    """

    # SORT VALUES
    df["GAME_DATE"] = df["ID_GAME"].str[-8:]
    df = df.sort_values("GAME_DATE")

    # BUILD TARGET
    conditions = [df["HOME_GOAL"] > df["AWAY_GOAL"], df["HOME_GOAL"] < df["AWAY_GOAL"]]
    choices = ["HOME_WIN", "AWAY_WIN"]
    df["TARGET"] = np.select(conditions, choices, default="DRAW")

    # PROCESS PERCENTAGE AND ABSOLUTE STATISTICS
    df = process_perc_and_abs_columns(df, table_mapper)

    # Process Results and Results status
    column_names = table_mapper.wk_columns()
    df = pd.get_dummies(
        df, columns=[column_names["FINAL_RESULT"]["name"], column_names["FINAL_RESULT_STATUS"]["name"]], dtype="int64"
    )
    cols_to_transform = [
        col
        for col in df.columns
        if col.startswith((column_names["FINAL_RESULT"]["name"], column_names["FINAL_RESULT_STATUS"]["name"]))
    ]

    fe_transformers = FeatureEngineeringMethods(df, "TEAM")

    for col in cols_to_transform:
        df[f"CUMU_{col}"] = fe_transformers.get_cumulated_value_past(col)

    df = df.drop("GAME_DATE", axis=1)

    return df


class FeatureEngineeringMethods:
    """This class groups all the main transformation methods applied on tables."""

    def __init__(self, data: pd.DataFrame, groupby_var: str) -> None:
        self.data = data.copy()
        self.groupby_var = groupby_var

    def get_avg_value_past(self, variable: str) -> pd.Series:
        """For a listed number of variables, get their average values on the last 3 games of a team."""

        n_games_past = 3

        self.avg_var = self.data.groupby(self.groupby_var)[variable].transform(
            lambda x: x.rolling(n_games_past).mean().shift()
        )

        return self.avg_var

    def get_raw_value_past(self, variable: str) -> pd.Series:
        """For a listed number of variables, get their last absolute value."""

        n_games_past = 1

        self.last_value_var = self.data.groupby(self.groupby_var)[variable].shift(n_games_past)

        return self.last_value_var

    def get_cumulated_value_past(self, variable: str) -> pd.Series:
        """For a listed number of variables, get their cumulated value from the beginning of the season."""

        tmp_df = self.data.copy()

        tmp_df["tmp_result"] = tmp_df.groupby(self.groupby_var)[variable].cumsum()
        self.cumu_value_var = tmp_df.groupby(self.groupby_var)["tmp_result"].shift(1)

        return self.cumu_value_var

    def __call__(self, variable: str) -> pd.DataFrame:
        """Call the the other three methods in this class."""

        self.data[variable] = self.data[variable].astype(float)

        self.data[f"AVG_{variable}"] = self.get_avg_value_past(variable)
        self.data[f"LAST_{variable}"] = self.get_raw_value_past(variable)
        self.data[f"CUMU_{variable}"] = self.get_cumulated_value_past(variable)

        return self.data[[f"AVG_{variable}", f"LAST_{variable}", f"CUMU_{variable}"]]


class VariableTransformer(FeatureEngineeringMethods, BaseEstimator, TransformerMixin):  # type: ignore
    def __init__(self, table_mapper: TableDefinition, groupby_var: str) -> None:
        self.table_mapper = table_mapper

        # self._load_config()
        self._map_variables_method()

    def _map_variables_method(self) -> None:
        """get the list of variables to apply FeatureEngineeringMethods on."""
        table_columns = self.table_mapper.get_all_atributes()

        self.vars_to_transform = []

        for column in table_columns:
            column_config = self.table_mapper.wk_columns()[column]

            if column_config["transform"]:
                self.vars_to_transform.append(column_config["name"])

    def fit(self, X: pd.DataFrame, y: None = None) -> Any:
        """Empty fit."""
        return self  # The fit method typically does nothing for transformers

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the FeatureEngineeringMethods on the listed variables."""
        fe_transformer = FeatureEngineeringMethods(X, groupby_var="TEAM")

        for variable_name in self.vars_to_transform:
            X = pd.concat([X, fe_transformer(variable_name)], axis=1)

        return X.drop(self.vars_to_transform, axis=1)
