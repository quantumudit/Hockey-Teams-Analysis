"""
Work in progress
"""

import pandas as pd
from rich.console import Console
from rich.table import Table


def top_n_teams(dataframe: pd.DataFrame, column_name: str,
                agg_func: str, n: int = 5) -> pd.DataFrame:
    """
    Generate a DataFrame containing the top N teams based on a specified column's aggregation.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing team statistics.
        column_name (str): The name of the column used for aggregation and ranking.
        agg_func (str): The aggregation function to apply (e.g., 'sum', 'mean', 'max').
        n (int, optional): The number of top teams to retrieve. Defaults to 5.

    Returns:
        pd.DataFrame: A DataFrame containing the top N teams based on the specified aggregation.
    """
    topn_df = (
        dataframe[["team_name", column_name]]
        .groupby("team_name")
        .agg(agg_func)
        .nlargest(n=n, columns=column_name)
        .reset_index()
    )
    return topn_df


def bottom_n_teams(dataframe: pd.DataFrame, column_name: str,
                   agg_func: str, n: int = 5) -> pd.DataFrame:
    """
    Generate a DataFrame containing the bottom N teams based on a specified column's aggregation.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing team statistics.
        column_name (str): The name of the column used for aggregation and ranking.
        agg_func (str): The aggregation function to apply (e.g., 'sum', 'mean', 'max').
        n (int, optional): The number of bottom teams to retrieve. Defaults to 5.

    Returns:
        pd.DataFrame: A DataFrame containing the top N teams based on the specified aggregation.
    """
    bottom_n_df = (
        dataframe[["team_name", column_name]]
        .groupby("team_name")
        .agg(agg_func)
        .nsmallest(n=n, columns=column_name)
        .reset_index()
    )
    return bottom_n_df


def pretty_print_topn_df(dataframe: pd.DataFrame, title: str) -> None:
    """_summary_

    Args:
        dataframe (pd.DataFrame): _description_
        title (str): _description_
    """

    # Create a Rich Console
    console = Console()

    # Create a Rich Table
    table = Table(title=title)

    # Set Index column name and style
    table.add_column("Index")

    # Set columns style
    for col_name, style in zip(dataframe.columns, ["cyan", "green"]):
        table.add_column(col_name, style=style)

    # Add rows from the DataFrame
    for i, row in dataframe.iterrows():
        table.add_row(str(i), *[str(row[col]) for col in dataframe.columns])

    # Print the table
    console.print(table)
