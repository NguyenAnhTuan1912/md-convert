from ._format_row import format_row

def to_markdown_table(table: list[list[str]]) -> str:
    """Convert a 2D list (rows/columns) into a nicely aligned Markdown table.

    Args:
        table (list[list[str]]): extracted table from document.

    Returns:
        str: table as markdown (plain text).
    """
    if not table:
        return ""

    # Column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    header, *rows = table
    md = [format_row(header, col_widths)]
    md.append("| " + " | ".join("-" * w for w in col_widths) + " |")
    for row in rows:
        md.append(format_row(row, col_widths))

    return "\n".join(md)