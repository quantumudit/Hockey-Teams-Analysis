from tabulate import tabulate


def dict_to_table(input_dict: dict, column_headers: list) -> str:
    """
    Convert a dictionary into a tabulated string.

    Args:
        input_dict (dict): The input dictionary to be converted into a table.
        column_headers (list): List of column headers for the table.

    Returns:
        str: A tabulated representation of the dictionary as a string.
    """

    table_vw = tabulate(input_dict.items(),
                        headers=column_headers,
                        tablefmt="pretty",
                        stralign='left')

    return table_vw
