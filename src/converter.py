import os
import threading
from pathlib import Path

from markitdown import MarkItDown

from utils import to_chunks


class MDConverter:
    def __init__(
        self,
        ori_folder_name: str,
        out_folder_name: str,
        total_of_workers: int,
        total_of_concurrent_processed_files: int,
    ):
        self.md = MarkItDown(enable_plugins=False)
        self.ori_folder_name = ori_folder_name
        self.out_folder_name = out_folder_name
        self.total_of_workers = total_of_workers
        self.total_of_concurrent_processed_files = total_of_concurrent_processed_files

    def convert_file(self, md: MarkItDown, file_path: str):
        """Convert a file to markdown.

        Args:
            md (MarkItDown): converter core.
            file_path (str): path to file.
        """
        try:
            result = md.convert(os.path.join(self.ori_folder_name, file_path))

            out_file_name = os.path.splitext(file_path)[0]
            out_file_path = os.path.normpath(
                os.path.join("./", self.out_folder_name, f"{out_file_name}.md")
            )

            os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

            with open(out_file_path, "w", encoding="utf-8") as f:
                f.write(result.text_content)
        except Exception as e:
            print(f"Cannot convert file: {file_path}")

    def convert_files(self, md: MarkItDown, file_paths: list[str]):
        """Convert multiple files to markdown.

        Args:
            md (MarkItDown): converter core.
            file_paths (list[str]): path to file.
        """
        for file_path in file_paths:
            self.convert_file(md, file_path)

    def convert_in_folder(self, md: MarkItDown, folder_name: str):
        """Convert all files in a folder.

        Args:
            md (MarkItDown): converter core.
            folder_name (str): name of folder
        """
        target_path = os.path.abspath(os.path.join(self.ori_folder_name, folder_name))
        folder = Path(target_path)
        file_paths = []
        threads = []

        for item in folder.rglob("*"):
            if item.is_dir():
                continue

            file_name = str(item.relative_to(os.path.abspath(self.ori_folder_name)))
            file_paths.append(file_name)

        item_chunks = to_chunks(file_paths, self.total_of_concurrent_processed_files)
        process_thread_count = (
            self.total_of_workers
            if len(item_chunks) > self.total_of_workers
            else len(item_chunks)
        )

        for i in range(process_thread_count):
            t = threading.Thread(target=self.convert_files, args=(md, item_chunks[i]))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
