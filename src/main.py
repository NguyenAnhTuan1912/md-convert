import os
import sys
import time
import threading
from pathlib import Path

#### Make sure this script is always in root folder (root path)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from markitdown import MarkItDown
from rich import print as rich_print

import config

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

def to_chunks(arr: list, size: int):
    """Convert array to list of chunks

    Args:
        arr (list): original array
        size (int): _description_

    Returns:
        (list, int): list of chunks and total items count
    """
    count = 0
    result = []
    chunk = []
    total_item_count = 0

    for item in arr:
        if count == size:
            result.append(chunk)
            chunk = []
            count = 0

        chunk.append(item)
        count += 1
        total_item_count += 1

    if len(chunk) > 1:
        result.append(chunk)

    return result


def convert_file(md: MarkItDown, file_or_folder_path: str):
    global total_converted, out_folder_name

    try:
        result = md.convert(os.path.join(ori_folder_name, file_or_folder_path))

        out_file_name = os.path.splitext(file_or_folder_path)[0]
        out_file_path = os.path.normpath(os.path.join("./", out_folder_name, f"{out_file_name}.md"))

        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

        with open(out_file_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        total_converted += 1
    except Exception as e:
        rich_print(f"[red]Cannot convert file: {file_or_folder_path}[/red]")

def convert_files(md: MarkItDown, file_or_folder_paths: list[str]):
    global ori_folder_name

    for file_or_folder_path in file_or_folder_paths:
        convert_file(md, file_or_folder_path)

def convert_in_folder(md: MarkItDown, folder_name: str):
    global ori_folder_name, total_of_workers, total_of_concurrent_processed_files

    target_path = os.path.abspath(os.path.join(ori_folder_name, folder_name))
    folder = Path(target_path)
    file_paths = []
    threads = []

    for item in folder.rglob("*"):
        if item.is_dir():
            continue

        file_name = str(item.relative_to(os.path.abspath(ori_folder_name)))
        file_paths.append(file_name)

    item_chunks = to_chunks(file_paths, total_of_concurrent_processed_files)
    process_thread_count = total_of_workers if len(item_chunks) > total_of_workers else len(item_chunks)

    for i in range(process_thread_count):
        t = threading.Thread(target=convert_files, args=(md, item_chunks[i]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def main():
    global ori_folder_name, out_folder_name

    if not os.path.exists(out_folder_name):
        os.makedirs(os.path.abspath(out_folder_name), exist_ok=True)

    file_or_folder_name = input("Target name (file/folder name): ")

    target_path = os.path.abspath(os.path.join(ori_folder_name, file_or_folder_name))
    print(f"Target: {target_path}")

    md = MarkItDown(enable_plugins=False)

    if os.path.isfile(target_path):
        start = time.time()
        rich_print("[green]Processing...[/green]")
        convert_file(md, file_or_folder_name)
        end = time.time()
    else:
        start = time.time()
        convert_in_folder(md, file_or_folder_name)
        end = time.time()

    print("====================")
    rich_print(f"Total time: [green]{end - start:.4f}s[/green]")
    rich_print(f"Converted: [green]{total_converted} file(s)[/green]")

if __name__ == "__main__":
    main()