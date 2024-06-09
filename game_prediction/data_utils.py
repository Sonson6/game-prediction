import pandas as pd
from sqlalchemy import create_engine

from game_prediction.config import TableMapping


def read_data_from_postgres(table_query: str, **kwargs) -> pd.DataFrame:  # type: ignore
    """Read dataframe from PostGreSQL.

    Args:
        table_query (str): Name of PostGreSQL table.

    Returns:
        pd.DataFrame: Dataset read from PostGreSQL.
    """

    config = TableMapping.config
    conn_string = f'postgresql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database"]}'

    db = create_engine(conn_string)
    conn = db.connect()

    data = pd.read_sql(table_query, con=conn, **kwargs)

    conn.close()

    return data
