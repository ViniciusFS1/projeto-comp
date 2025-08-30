def txt_to_list(file_path: str, comment_char: str = "#") -> list:
    """
    Transforms a text file into a list of non-empty lines, ignoring lines starting with a comment character.

    Args:
        file_path: The path to the text file (str)
        comment_char: Character indicating a comment line (default: "#")
    
    Returns:
        A list of non-empty, non-comment lines from the text file (list)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [
                line.strip() 
                for line in f 
                if line.strip() and not line.strip().startswith(comment_char)
            ]
    except Exception as e:
        print(f"[ERROR] Failed to read {file_path}: {e}")
        return []