import pandas as pd
from pdfplumber.page import Page
from pdfplumber.utils import extract_text, get_bbox_overlap, obj_to_bbox

def process_page(page: Page):
    """Process page, extract text, table and replace table to right place.

    Flow:
        1. Lấy toàn bộ ký tự trong page.
        2. Tìm toàn bộ tables có ở trong page đó.
        3. Trong mỗi table, mình sẽ lấy ký tự đầu tiên trong table đó (có thể là word).
        4. Trong page mình sẽ filter các nội dung, chỉ lấy các phần không bị trùng lặp (trùng lặp thì có nghĩa là
        ở đó đã có table => cần phải xoá).
        5. Extract table và chuyển về data frame.
        6. Chuyển data frame thành markdown (bỏ dòng đầu).
        7. Thêm markdown mới chuyển vào trong chars (các ký tự còn lại sau khi filter ở bước trên).

    Args:
        page (Page): pdf page.

    Returns:
        str: processed pdf.
    """
    all_text = []
    
    filtered_page = page
    chars = filtered_page.chars

    for table in page.find_tables():
        first_table_char = page.crop(table.bbox).chars[0]
        filtered_page = filtered_page.filter(lambda obj:
            get_bbox_overlap(obj_to_bbox(obj), table.bbox) is None
        )
        chars = filtered_page.chars
        df = pd.DataFrame(table.extract())
        df.columns = df.iloc[0]
        markdown = df.drop(0).to_html(index=False)
        chars.append(first_table_char | {"text": markdown})

    page_text = extract_text(chars, layout=True)
    all_text.append(page_text)

    return "\n".join(all_text).strip()