def format_row(row: list[str], col_widths: list[int]):
    """Format row to right size.

    Args:
        row (list[str]): row data.
        col_widths (list[int]): col widths.

    Returns:
        str: row string data.
    """
    return (
        "| "
        + " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
        + " |"
    )