# Copyright Sierra

import json
import os
from typing import Any

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> dict[str, Any]:
    data = {}
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".json"):
            key = filename[:-5]  # Remove .json extension
            with open(os.path.join(FOLDER_PATH, filename)) as f:
                data[key] = json.load(f)
    return data