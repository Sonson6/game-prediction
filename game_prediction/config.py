import os
from enum import Enum
from typing import Any, Union


def load_postgres_config() -> dict[str, Union[str, None]]:
    """Read configuration file with credentials.

    Args:
        filename (str, optional): Name of the file containing PostGreSQL credentials. Defaults to "database.ini".
        section (str, optional): Defaults to "postgresql".

    Raises:
        Exception: Raised when no config found.

    Returns:
        dict[str, str]: Configuration information.
    """

    in_docker_or_not = os.getenv("IN_DOCKER", False)
    if in_docker_or_not:
        adaptable_host = os.getenv("DATABASE_HOST")
    else:
        adaptable_host = "localhost"

    return {
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "host": adaptable_host,
        "database": os.getenv("DATABASE_NAME"),
    }


class AttributeDictMixin:
    """This will be the parent class of each XCols class. Helps to automatically
    fills some contextual values when declaring those class attributes  :
        - Variable name
        - does this variable should be transformed through FE or not
        - Does this transformed value should be interpreted as greater is better or not

    This class gives flexibility, a class attribute declared in a XCols class could be either :
        - Associated with a string that will be considered as name of the variable
            (in this case, this class will fill "transform" and "greater_is_better" as True by default).
        - Associated with a dictionary, therefore it expect "name", "transform" and "greater_is_better", if
            "transform" or "greater_is_better is missing", it will be automatically filled with default value (True).
    """

    _values = {}  # type: ignore

    def __init_subclass__(cls, **kwargs) -> None:  # type: ignore
        super().__init_subclass__(**kwargs)
        cls._values = {
            attr: getattr(cls, attr)
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        }

    def __getitem__(self, key):  # type: ignore
        if isinstance(self._values[key], str):
            return {"name": self._values[key], "transform": True, "greater_is_better": True}

        elif isinstance(self._values[key], dict):
            expected_keys = ["name", "transform", "greater_is_better"]
            missing_tags = [exp_key for exp_key in expected_keys if exp_key not in self._values[key].keys()]
            for missing_tag in missing_tags:
                self._values[key][missing_tag] = True
            return self._values[key]

        else:
            raise ValueError("Invalid parameter type. You class attribute should either be a string or a dictionary.")


class Perimeter(Enum):
    """Table perimeter."""

    GAME = "GAME"
    PLAYER = "PLAYER"


class Tables(Enum):
    """SQL tables."""

    GAME_DATA = "game_data"
    PLAYER_GENERAL_INFO = "player_general_info"
    PLAYER_GAME_INFO_EXTEND = "player_game_info_extend"
    PLAYER_GAME_SUMMARY = "player_game_summary"
    PLAYER_GAME_PASSING_INFO = "passing_table"
    PLAYER_GAME_PASSING_TYPE_INFO = "passing_type_table"
    PLAYER_GAME_DEFENSIVE_INFO = "defensive_table"
    PLAYER_GAME_POSSESSION_INFO = "possession_table"
    PLAYER_GAME_MISSES_INFO = "misses_table"
    PLAYER_GAME_GOALKEEPER_INFO = "goalkeeper_table"


class MatchCols(AttributeDictMixin):
    """MatchCols"""

    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    SEASON = {"name": "SEASON", "transform": False, "greater_is_better": False}
    TEAM = {"name": "TEAM", "transform": False, "greater_is_better": False}
    STATUS = {"name": "STATUS", "transform": False, "greater_is_better": False}
    POSSESSION_PERC = "possession%"
    PASS_ACC_PERC = "pass_acc%"
    SOT_PERC = "SoT%"
    SAVES_PERC = "saves%"
    Y_R_CARDS = {"name": "yellow_or_red_card", "greater_is_better": False}
    PASS_ACC = "pass_acc"
    SOT = "SoT"
    SAVES = "saves"
    HOME_GOAL = "HOME_GOAL"
    AWAY_GOAL = "AWAY_GOAL"
    HOME_GOAL_XG = "HOME_GOAL_XG"
    AWAY_GOAL_XG = "AWAY_GOAL_XG"
    SCORED = "SCORED"
    CONCEIDED = "CONCEIDED"
    SCORED_XG = "SCORED_XG"
    CONCEIDED_XG = "CONCEIDED_XG"
    FINAL_RESULT = {"name": "FINAL_RESULT", "transform": False}
    FINAL_RESULT_STATUS = {"name": "FINAL_RESULT_STATUS", "transform": False}


class PlayerGeneralCols(AttributeDictMixin):
    """PlayerGeneralCols"""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    NATION = {"name": "NATION", "transform": False, "greater_is_better": False}
    AGE = {"name": "AGE", "transform": False, "greater_is_better": False}


class PlayerExtendCols(AttributeDictMixin):
    """PlayerExtendCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    TEAM = {"name": "TEAM", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    NUMBER = {"name": "NUMBER", "transform": False, "greater_is_better": False}
    POS = {"name": "POS", "transform": False, "greater_is_better": False}
    MIN = "MIN"


class PlayerGameSummaryCols(AttributeDictMixin):
    """PlayerGameSummaryCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    PERFORMANCE_GLS = "PERFORMANCE_GLS"
    PERFORMANCE_AST = "PERFORMANCE_AST"
    PERFORMANCE_PK = "PERFORMANCE_PK"
    PERFORMANCE_PKATT = "PERFORMANCE_PKATT"
    PERFORMANCE_SH = "PERFORMANCE_SH"
    PERFORMANCE_SOT = "PERFORMANCE_SOT"
    PERFORMANCE_TOUCHES = "PERFORMANCE_TOUCHES"
    PERFORMANCE_TKL = "PERFORMANCE_TKL"
    PERFORMANCE_INT = "PERFORMANCE_INT"
    PERFORMANCE_BLOCKS = "PERFORMANCE_BLOCKS"
    EXPECTED_XG = "EXPECTED_XG"
    EXPECTED_NPXG = "EXPECTED_NPXG"
    EXPECTED_XAG = "EXPECTED_XAG"
    SCA_SCA = "SCA_SCA"
    SCA_GCA = "SCA_GCA"
    PASSES_CMP = "PASSES_CMP"
    PASSES_ATT = "PASSES_ATT"
    PASSES_CMP_PERC = "PASSES_CMP%"
    PASSES_PRGP = "PASSES_PRGP"
    CARRIES_CARRIES = "CARRIES_CARRIES"
    CARRIES_PRGC = "CARRIES_PRGC"
    TAKE_ONS_ATT = "TAKE-ONS_ATT"
    TAKE_ONS_SUCC = "TAKE-ONS_SUCC"


class PlayerGamePassingCols(AttributeDictMixin):
    """PlayerGamePassingCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    TOTAL_CMP = "TOTAL_CMP"
    TOTAL_ATT = "TOTAL_ATT"
    TOTAL_CMP_PERC = "TOTAL_CMP%"
    TOTAL_TOTDIST = "TOTAL_TOTDIST"
    TOTAL_PRGDIST = "TOTAL_PRGDIST"
    SHORT_CMP = "SHORT_CMP"
    SHORT_ATT = "SHORT_ATT"
    SHORT_CMP_PERC = "SHORT_CMP%"
    MEDIUM_CMP = "MEDIUM_CMP"
    MEDIUM_ATT = "MEDIUM_ATT"
    MEDIUM_CMP_PERC = "MEDIUM_CMP%"
    LONG_CMP = "LONG_CMP"
    LONG_ATT = "LONG_ATT"
    LONG_CMP_PERC = "LONG_CMP%"
    AST = "AST"
    XAG = "XAG"
    XA = "XA"
    KP = "KP"
    ONE_THIRD = "1/3"
    PPA = "PPA"
    CRSPA = "CRSPA"
    PRGP = "PRGP"


class PlayerGamePassingTypeCols(AttributeDictMixin):
    """PlayerGamePassingTypeCols"""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    ATT = "ATT"
    PASS_TYPES_LIVE = "PASS TYPES_LIVE"
    PASS_TYPES_DEAD = "PASS TYPES_DEAD"
    PASS_TYPES_FK = "PASS TYPES_FK"
    PASS_TYPES_TB = "PASS TYPES_TB"
    PASS_TYPES_SW = "PASS TYPES_SW"
    PASS_TYPES_CRS = "PASS TYPES_CRS"
    PASS_TYPES_TI = "PASS TYPES_TI"
    PASS_TYPES_CK = "PASS TYPES_CK"
    CORNER_KICKS_IN = "CORNER KICKS_IN"
    CORNER_KICKS_OUT = "CORNER KICKS_OUT"
    CORNER_KICKS_STR = "CORNER KICKS_STR"
    OUTCOMES_CMP = "OUTCOMES_CMP"
    OUTCOMES_OFF = "OUTCOMES_OFF"
    OUTCOMES_BLOCKS = "OUTCOMES_BLOCKS"


class PlayerGameDefensiveCols(AttributeDictMixin):
    """PlayerGameDefensiveCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    TACKLES_TKL = "TACKLES_TKL"
    TACKLES_TKLW = "TACKLES_TKLW"
    TACKLES_DEF_THIRD = "TACKLES_DEF 3RD"
    TACKLES_MID_THIRD = "TACKLES_MID 3RD"
    TACKLES_ATT_THIRD = "TACKLES_ATT 3RD"
    CHALLENGES_TKL = "CHALLENGES_TKL"
    CHALLENGES_ATT = "CHALLENGES_ATT"
    CHALLENGES_TKL_PERC = "CHALLENGES_TKL%"
    CHALLENGES_LOST = "CHALLENGES_LOST"
    BLOCKS_BLOCKS = "BLOCKS_BLOCKS"
    BLOCKS_SH = "BLOCKS_SH"
    BLOCKS_PASS = "BLOCKS_PASS"
    INT = "INT"
    TKL_AND_INT = "TKL+INT"
    CLR = "CLR"
    ERR = "ERR"


class PlayerGamePossessionCols(AttributeDictMixin):
    """PlayerGamePossessionCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    TOUCHES_TOUCHES = "TOUCHES_TOUCHES"
    TOUCHES_DEF_PEN = "TOUCHES_DEF PEN"
    TOUCHES_DEF_THIRD = "TOUCHES_DEF 3RD"
    TOUCHES_MID_THIRD = "TOUCHES_MID 3RD"
    TOUCHES_ATT_THIRD = "TOUCHES_ATT 3RD"
    TOUCHES_ATT_PEN = "TOUCHES_ATT PEN"
    TOUCHES_LIVE = "TOUCHES_LIVE"
    TAKE_ONS_SUCC_PERC = "TAKE-ONS_SUCC%"
    TAKE_ONS_TKLD = "TAKE-ONS_TKLD"
    TAKE_ONS_TKLD_PERC = "TAKE-ONS_TKLD%"
    CARRIES_TOTDIST = "CARRIES_TOTDIST"
    CARRIES_PRGDIST = "CARRIES_PRGDIST"
    CARRIES_ONE_THIRD = "CARRIES_1/3"
    CARRIES_CPA = "CARRIES_CPA"
    CARRIES_MIS = "CARRIES_MIS"
    CARRIES_DIS = "CARRIES_DIS"
    RECEIVING_REC = "RECEIVING_REC"
    RECEIVING_PRGR = "RECEIVING_PRGR"


class PlayerGameMissesCols(AttributeDictMixin):
    """PlayerGameMissesCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    PERFORMANCE_CRDY = "PERFORMANCE_CRDY"
    PERFORMANCE_CRDR = "PERFORMANCE_CRDR"
    PERFORMANCE_2CRDY = "PERFORMANCE_2CRDY"
    PERFORMANCE_FLS = "PERFORMANCE_FLS"
    PERFORMANCE_FLD = "PERFORMANCE_FLD"
    PERFORMANCE_OFF = "PERFORMANCE_OFF"
    PERFORMANCE_CRS = "PERFORMANCE_CRS"
    PERFORMANCE_TKLW = "PERFORMANCE_TKLW"
    PERFORMANCE_PKWON = "PERFORMANCE_PKWON"
    PERFORMANCE_PKCON = "PERFORMANCE_PKCON"
    PERFORMANCE_OG = "PERFORMANCE_OG"
    PERFORMANCE_RECOV = "PERFORMANCE_RECOV"
    AERIAL_DUELS_WON = "AERIAL DUELS_WON"
    AERIAL_DUELS_LOST = "AERIAL DUELS_LOST"
    AERIAL_DUELS_WON_PERC = "AERIAL DUELS_WON%"


class PlayerGameGoalkeeperCols(AttributeDictMixin):
    """PlayerGameGoalkeeperCols."""

    PLAYER = {"name": "PLAYER", "transform": False, "greater_is_better": False}
    ID_GAME = {"name": "ID_GAME", "transform": False, "greater_is_better": False}
    SHOT_STOPPING_SOTA = "SHOT STOPPING_SOTA"
    SHOT_STOPPING_GA = "SHOT STOPPING_GA"
    SHOT_STOPPING_SAVES = "SHOT STOPPING_SAVES"
    SHOT_STOPPING_SAVE_PERC = "SHOT STOPPING_SAVE%"
    SHOT_STOPPING_PSXG = "SHOT STOPPING_PSXG"
    LAUNCHED_CMP = "LAUNCHED_CMP"
    LAUNCHED_ATT = "LAUNCHED_ATT"
    LAUNCHED_CMP_PERC = "LAUNCHED_CMP%"
    PASSES_THR = "PASSES_THR"
    PASSES_LAUNCH_PERC = "PASSES_LAUNCH%"
    PASSES_AVGLEN = "PASSES_AVGLEN"
    GOAL_KICKS_ATT = "GOAL KICKS_ATT"
    GOAL_KICKS_LAUNCH_PERC = "GOAL KICKS_LAUNCH%"
    GOAL_KICKS_AVGLEN = "GOAL KICKS_AVGLEN"
    CROSSES_OPP = "CROSSES_OPP"
    CROSSES_STP = "CROSSES_STP"
    CROSSES_STP_PERC = "CROSSES_STP%"
    SWEEPER_OPA = "SWEEPER_#OPA"
    SWEEPER_AVGDIST = "SWEEPER_AVGDIST"


class TableDefinition:
    """Aggregate main SQL tables informations, among which the perimeter of the table,
    the query to create it if needed and of course the variables.
    """

    def __init__(
        self,
        perimeter: Perimeter,
        wk_columns: Any,
        primary_key: list[str],
    ):
        """Class instantiation.

        Args:
            perimeter (Perimeter): Says if table is related to the game itself or player statistics.
            creation_query (str): SQL request to create the table if not existing already.
            wk_columns (): Columns related to the SQL table.
            primary_key (list[str]): primary key(s) for a table.

        Precision on wk_columns : careful, with the AttributeDictMixin parent class,
        calling TableDefinition.wk_columns.var_name isn't the same as
        TableDefinition.wk_columns().var_name With the first one, you get the
        traditional behavior of the Xcols classes, with the second you get a config dictionary.
        """
        self.perimeter = perimeter
        self.wk_columns = wk_columns
        self.primary_key = primary_key

    def get_all_atributes(self) -> list[str]:
        """As columns are declared in class attributes,  we use this function to list them.

        Returns:
            list[str]: Columns from the SQL table in the format used in the Python script.
        """
        return [
            attr
            for attr in self.wk_columns.__dict__.keys()
            if not callable(getattr(self.wk_columns, attr)) and not attr.startswith(("_", "__"))
        ]


# TableDefinition("GAME", TableCreations.GAME_DATA_TABLE, MatchCols).get_all_columns()


class TableMapping:
    """Class to map main SQL table informations in a dictionary that can
    be used anywhere on the script.
    """

    config = load_postgres_config()

    def __init__(self) -> None:
        """Class Instantiation."""
        self.TableConfig = {}
        self.TableConfig[Tables.GAME_DATA] = TableDefinition(Perimeter.GAME, MatchCols, ["ID_GAME", "TEAM"])
        self.TableConfig[Tables.PLAYER_GAME_SUMMARY] = TableDefinition(
            Perimeter.PLAYER, PlayerGameSummaryCols, ["PLAYER", "ID_GAME"]
        )
        self.TableConfig[Tables.PLAYER_GENERAL_INFO] = TableDefinition(Perimeter.PLAYER, PlayerGeneralCols, ["PLAYER"])
        self.TableConfig[Tables.PLAYER_GAME_INFO_EXTEND] = TableDefinition(
            Perimeter.PLAYER,
            PlayerExtendCols,
            ["PLAYER", "TEAM", "ID_GAME"],
        )
        self.TableConfig[Tables.PLAYER_GAME_PASSING_INFO] = TableDefinition(
            Perimeter.PLAYER,
            PlayerGamePassingCols,
            ["PLAYER", "ID_GAME"],
        )

        self.TableConfig[Tables.PLAYER_GAME_PASSING_TYPE_INFO] = TableDefinition(
            Perimeter.PLAYER,
            PlayerGamePassingTypeCols,
            ["PLAYER", "ID_GAME"],
        )

        self.TableConfig[Tables.PLAYER_GAME_DEFENSIVE_INFO] = TableDefinition(
            Perimeter.PLAYER,
            PlayerGameDefensiveCols,
            ["PLAYER", "ID_GAME"],
        )

        self.TableConfig[Tables.PLAYER_GAME_POSSESSION_INFO] = TableDefinition(
            Perimeter.PLAYER,
            PlayerGamePossessionCols,
            ["PLAYER", "ID_GAME"],
        )

        self.TableConfig[Tables.PLAYER_GAME_MISSES_INFO] = TableDefinition(
            Perimeter.PLAYER, PlayerGameMissesCols, ["PLAYER", "ID_GAME"]
        )

        self.TableConfig[Tables.PLAYER_GAME_GOALKEEPER_INFO] = TableDefinition(
            Perimeter.PLAYER,
            PlayerGameGoalkeeperCols,
            ["PLAYER", "ID_GAME"],
        )

    def get_table_info(self, table: Tables) -> TableDefinition:
        """Get the TableDefinition object related to the SQL table we want.

        Args:
            table (Tables): SQL table

        Returns:
            TableDefinition: Dcitionary with main information (perimeter, creation query and columns)
        """
        return self.TableConfig[table]


# TableMapping().get_table_info(Tables.GAME_DATA).perimeter
# TableMapping().get_table_info(Tables.GAME_DATA).creation_query.value
# TableMapping().TableConfig[Tables.GAME_DATA].creation_query
