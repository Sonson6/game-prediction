from typing import Union

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import game_prediction.constants as cst
from game_prediction.config import TableMapping, Tables
from game_prediction.data_utils import read_data_from_postgres
from game_prediction.utils.preprocessing import VariableTransformer, pre_processing_game_data


def load_data(spe_query: Union[str, None] = None) -> pd.DataFrame:
    """Read main tables.

    Returns:
        tuple[pd.DataFrame, list[pd.DataFrame]]: Game aggregated data and
                                            player specific data
    """

    table = Tables.GAME_DATA
    table_mapper = TableMapping().get_table_info(table)

    if spe_query:
        game_data = read_data_from_postgres(spe_query)
    else:
        game_data = read_data_from_postgres(table.value)

    game_data = pre_processing_game_data(game_data, table_mapper)
    game_data = VariableTransformer(table_mapper, "TEAM").transform(game_data)

    return game_data


def build_final_data(game_data: pd.DataFrame) -> pd.DataFrame:
    """Add variables to model dataset.

    Args:
        game_data (pd.DataFrame): Model dataset.

    Returns:
        pd.DataFrame: Enhanced model dataset.
    """

    game_data_copy = game_data.copy()

    game_data_copy["NB_GAMES_BY_TEAM"] = game_data_copy.groupby("TEAM").cumcount() + 1
    game_data_copy = game_data_copy[game_data_copy["NB_GAMES_BY_TEAM"] > 3].drop("NB_GAMES_BY_TEAM", axis=1)

    game_data_copy["ID_GAME_TEAM"] = game_data_copy["ID_GAME"] + "_" + game_data_copy["TEAM"]

    return game_data_copy


def pivot_final_data_for_model(df_model: pd.DataFrame, groupby_var: str = "ID_GAME") -> pd.DataFrame:
    """Reshape processed dataset.

    Args:
        df_model (pd.DataFrame): Processed dataset.
        groupby_var (str, optional): Variable to use to group rows. Defaults to "ID_GAME".

    Returns:
        pd.DataFrame: Processed dataset where HOME vs AWAY team variable values are merged into a ratio.
    """

    vars_to_compare = df_model.columns.tolist()[5:]

    final_df = df_model[["ID_GAME", "TARGET"]].drop_duplicates("ID_GAME").copy()

    for check_var in vars_to_compare:
        tmp = df_model.pivot(index=groupby_var, columns="STATUS", values=check_var).reset_index()
        tmp[f"{check_var}_RATIO"] = tmp["AWAY"] / tmp["HOME"]
        tmp = tmp.drop(["HOME", "AWAY"], axis=1)

        final_df = pd.merge(final_df, tmp, on=["ID_GAME"], how="left")

    return final_df.fillna(0).replace([np.inf, -np.inf], 0)


def prepare_data_model(game_players_df: pd.DataFrame) -> pd.DataFrame:
    """Filter the last useless variables and reshape processed dataset.

    Args:
        game_players_df (pd.DataFrame): Processed dataset.

    Returns:
        pd.DataFrame: Final dataset before sample split.
    """

    # CUMU_CONCEIDED_XG is the last variable we can use
    # TODO: Find a cleaner way to filter columns to keep the final variables
    column_list = game_players_df.columns.tolist()
    last_var = column_list.index("CUMU_CONCEIDED_XG") + 1

    # Keep only one row per game
    df_model = game_players_df.drop_duplicates("ID_GAME_TEAM")[column_list[:last_var]]

    # Drop useless variables
    useless_vars_to_drop = [col for col in df_model.columns if ("CUMU_" in col) and ("%" in col)]
    useless_vars_to_drop += [
        "FINAL_RESULT_DRAW",
        "FINAL_RESULT_LOSS",
        "FINAL_RESULT_WIN",
        "FINAL_RESULT_STATUS_AWAY_WIN",
        "FINAL_RESULT_STATUS_DRAW",
        "FINAL_RESULT_STATUS_HOME_WIN",
    ]

    df_model = df_model.drop(useless_vars_to_drop, axis=1)

    df_model_final = pivot_final_data_for_model(df_model)

    return df_model_final


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split final dataset into model samples.

    Args:
        df (pd.DataFrame): Final dataset.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: Model samples.
    """
    X = df.drop(["ID_GAME", "TARGET"], axis=1)
    y = df["TARGET"].replace(cst.LABEL_CONVERTED)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    return X_train, X_test, y_train, y_test
