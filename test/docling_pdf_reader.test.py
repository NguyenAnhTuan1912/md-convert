import os
import sys
import time
from pathlib import Path

#### Make sure this script is always in root folder (root path)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from docling.document_converter import DocumentConverter

import config

ori_folder_name = config.ori_folder_name
out_folder_name = config.out_folder_name

ori_file_path = input("File path: ")
out_file_name = input("New file name (optional): ")
ori_file_abspath = os.path.abspath(os.path.join(ori_folder_name, ori_file_path))
converter = DocumentConverter()
result = converter.convert(ori_file_abspath)

if out_file_name != "" or out_file_name.strip() != "":
    ori_file_dir_path = os.path.dirname(ori_file_path)
    ori_file_path = os.path.join(ori_file_dir_path, out_file_name)

out_file_path = os.path.abspath(os.path.join(out_folder_name, str.format(f"{ori_file_path}.md")))

os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

example_tables = result.document.tables[0]

if example_tables:
    table_data = example_tables.data
    # table_data.table_cells
    print(table_data.model_dump_json())

# with open(out_file_path, "w", encoding="utf-8") as f:
#     content = result.document.export_to_html()
#     f.write(content)