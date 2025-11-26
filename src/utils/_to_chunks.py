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