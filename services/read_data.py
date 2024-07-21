
import json
from typing import List, Dict, Any


def from_file_name(filename: str) -> List[Dict[str, Any]]:
    """
    Reads content of json file in the 'data' directory with a context manager.
    Returns a list of dictionary items.
    """
    with open(f"./data/{filename}.json", "r") as file:
        json_raw = file.read()
    return json.loads(json_raw)