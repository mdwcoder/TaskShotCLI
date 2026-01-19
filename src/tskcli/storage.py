import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Any

from .model import Task

# Default location: ~/.tsk
TASKS_FILE = Path.home() / ".tsk"

DEFAULT_CONFIG = {
    "sort_order": "desc",
    "show_completed": True
}

def get_tasks_file_path() -> Path:
    return TASKS_FILE

def load_data() -> Dict[str, Any]:
    """
    Loads data from ~/.tsk. 
    Returns a dict with 'config' and 'tasks' (list of dicts).
    If file doesn't exist or is corrupt, returns default empty structure.
    """
    if not TASKS_FILE.exists():
        return {"config": DEFAULT_CONFIG.copy(), "tasks": []}

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure keys exist
            if "config" not in data:
                data["config"] = DEFAULT_CONFIG.copy()
            if "tasks" not in data:
                data["tasks"] = []
            return data
    except (json.JSONDecodeError, OSError):
        # Backup corrupt file if it exists and has content
        if TASKS_FILE.stat().st_size > 0:
            backup_path = TASKS_FILE.with_suffix(".bak")
            shutil.copy2(TASKS_FILE, backup_path)
            # You might want to warn the user here, but this is a library function.
            # We'll just return empty/default state.
        
        return {"config": DEFAULT_CONFIG.copy(), "tasks": []}

def save_data(data: Dict[str, Any]) -> None:
    """
    Saves data to ~/.tsk atomically.
    1. Write to temp file.
    2. Move temp file to ~/.tsk.
    """
    # Create temp file in the same directory to ensure atomic move works
    # Note: Path.home() is usually writable.
    
    # However, standard tempfile.NamedTemporaryFile puts it in /tmp usually.
    # To ensure atomic rename, we should try to create it in the same dir or use a robust method.
    # os.replace is atomic on POSIX.
    
    parent_dir = TASKS_FILE.parent
    
    with tempfile.NamedTemporaryFile("w", dir=parent_dir, delete=False, encoding="utf-8") as tmp_f:
        json.dump(data, tmp_f, indent=2, ensure_ascii=False)
        tmp_path = Path(tmp_f.name)
    
    try:
        # Atomic replace
        tmp_path.replace(TASKS_FILE)
    except OSError:
        # Fallback if replace fails (e.g. permission issues, though unlikely in home)
        if tmp_path.exists():
            os.remove(tmp_path)
        raise

def get_tasks() -> List[Task]:
    data = load_data()
    return [Task.from_dict(t) for t in data["tasks"]]

def get_config() -> Dict[str, Any]:
    data = load_data()
    return data["config"]
