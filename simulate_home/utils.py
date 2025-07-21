def load_comments_from_txt(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return [c.strip() for c in content.split(",") if c.strip()]