from pathlib import Path


def list_files_in_folder(folder_path: str):
    """List files in a folder.

    Args:
        folder_path (str): path to folder.

    Returns:
        list: list of file paths.
    """
    folder = Path(folder_path)
    file_paths = []

    for item in folder.rglob("*"):
        if item.is_dir():
            continue

        file_name = str()
        file_paths.append(file_name)

    return file_paths
