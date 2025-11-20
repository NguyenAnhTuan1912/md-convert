import os
import sys
import time

#### Make sure this script is always in root folder (root path)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from markitdown import MarkItDown
from rich import print as rich_print

import config
from converter import MDConverter

#### Introduction & Instruction
print("\n")
rich_print("[green bold]Convert to Markdown tool[/green bold]")
print("====================")
rich_print(
    """Hiện tại thì tool này có thể dùng để convert file đơn lẻ hoặc nhiều file. Với nhiều định dạng như:

[italic]PDF, PowerPoint, Word, Excel, Images (EXIF metadata and OCR), Audio (EXIF metadata and speech transcription), HTML, Text-based formats (CSV, JSON, XML), ZIP files (iterates over contents), Youtube URLs, EPubs, ...[/italic]

Hướng dẫn dùng:

1. Kéo file hoặc folder chứa các files muốn chuyển đổi vào trong thư mục [bold]data[/bold].
2. Nếu là file đơn thì nhập tên file + phần mở rộng. Nếu là thư mục chứa nhiều file thì nhập tên thư mục.
3. Xong và chờ kết quả.

Tool này được build bằng Markitdown: https://github.com/microsoft/markitdown"""
)
print("====================")

total_of_workers = config.total_of_workers
total_of_concurrent_processed_files = config.total_of_concurrent_processed_files
ori_folder_name = config.ori_folder_name
out_folder_name = config.out_folder_name
total_converted = 0


def main():
    converter = MDConverter(
        ori_folder_name,
        out_folder_name,
        total_of_workers,
        total_of_concurrent_processed_files,
    )

    if not os.path.exists(out_folder_name):
        os.makedirs(os.path.abspath(out_folder_name), exist_ok=True)

    file_or_folder_name = input("Target name (file/folder name): ")

    target_path = os.path.abspath(os.path.join(ori_folder_name, file_or_folder_name))
    print(f"Target: {target_path}")

    md = MarkItDown(enable_plugins=False)

    if os.path.isfile(target_path):
        start = time.time()
        rich_print("[green]Processing...[/green]")
        converter.convert_file(md, file_or_folder_name)
        end = time.time()
    else:
        start = time.time()
        converter.convert_in_folder(md, file_or_folder_name)
        end = time.time()

    print("====================")
    rich_print(f"Total time: [green]{end - start:.4f}s[/green]")
    rich_print(f"Converted: [green]{total_converted} file(s)[/green]")


if __name__ == "__main__":
    main()
