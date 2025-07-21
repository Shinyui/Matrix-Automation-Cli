def load_comments_from_txt(file_path: str) -> list[str]:
    """
    Load a list of comments from a comma-separated UTF-8 encoded text file.

    This function reads the given text file, splits its content by commas,
    strips whitespace from each comment, and returns a list of non-empty strings.

    :param file_path: Path to the .txt file containing comma-separated comments.
    :type file_path: str
    :return: A list of cleaned comment strings.
    :rtype: list[str]
    :raises FileNotFoundError: If the file does not exist.
    :raises UnicodeDecodeError: If the file is not UTF-8 encoded.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return [c.strip() for c in content.split(",") if c.strip()]
