from pdfplumber.page import Page
from tabulate import tabulate

def process_page_legacy(page: Page):
    """Process page, extract text, table (legacy).

    Flow:
        1. Lấy toàn bộ text (cả text trong table) và lấy table.
        2. Lặp toàn bộ table để xử lý.
        3. Bỏ None ra khỏi table.
        4. Replace table thủ công bằng phương thức replace().
        5. Tiếp tục bỏ khoảng trống và gom toàn bộ dòng chống.
        7. Chuyển đổi toàn bộ table thành HTML table.
        8. Thêm HTML table vào trong text.

    Args:
        page (Page): pdf page.

    Returns:
        str: processed pdf.
    """
    all_text = []

    text = page.extract_text(x_tolerance=1) or ""
    page_tables = page.extract_tables()

    # Remove table rows from text to avoid duplication
    for table in page_tables:
        if not table:
            continue

        # Normalize None → ""
        table = [[cell if cell is not None else "" for cell in row] for row in table]

        header_line = " ".join(table[0]).strip()
        if header_line in text:
            text = text.replace(header_line, "")
        for row in table[1:]:
            row_line = " ".join(row).strip()
            if row_line in text:
                text = text.replace(row_line, "")

    # Normalize whitespace: collapse multiple blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = "\n".join(lines)
    if clean_text:
        all_text.append(clean_text)

    # Append tables as aligned Markdown
    for table in page_tables:
        html_table = tabulate(table, tablefmt="html")
        if html_table:
            all_text.append(html_table)

    return "\n".join(all_text).strip()