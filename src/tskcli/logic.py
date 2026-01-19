from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Any
from .model import Task
from .storage import load_data, save_data, DEFAULT_CONFIG

def get_next_id(tasks: List[dict]) -> int:
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1

def add_task(text: str, priority: Optional[str] = None, due: Optional[str] = None) -> Task:
    data = load_data()
    tasks_data = data["tasks"]
    
    new_id = get_next_id(tasks_data)
    new_task = Task(id=new_id, text=text, priority=priority, due=due)
    
    tasks_data.append(new_task.to_dict())
    save_data(data)
    return new_task

def list_tasks(pending_only: bool = False, done_only: bool = False, limit: Optional[int] = None, show_all: bool = False) -> List[Task]:
    data = load_data()
    tasks = [Task.from_dict(t) for t in data["tasks"]]
    config = data.get("config", DEFAULT_CONFIG)
    
    # Filter
    if show_all:
        pass # No filter
    elif pending_only:
        tasks = [t for t in tasks if t.status == "pending"]
    elif done_only:
        tasks = [t for t in tasks if t.status == "done"]
    elif not config.get("show_completed", True):
         # If config says hide completed, and we didn't ask for all or done specifically
         # Use pending_only behavior effectively
         tasks = [t for t in tasks if t.status == "pending"]

    # Sort
    # Default sort_order is desc (newest/highest id first? or last added?)
    # "desc = ultimo arriba" suggests LIFO or newer IDs at top.
    # Let's interpret "desc" as ID descending (newest first).
    sort_order = config.get("sort_order", "desc")
    reverse = (sort_order == "desc")
    
    # Simple sort by ID for now. Maybe logic can be enhanced later.
    tasks.sort(key=lambda t: t.id, reverse=reverse)
    
    if limit:
        tasks = tasks[:limit]
        
    return tasks

def complete_task(task_id: int) -> Optional[Task]:
    data = load_data()
    tasks_data = data["tasks"]
    
    for t_data in tasks_data:
        if t_data["id"] == task_id:
            if t_data["status"] == "done":
                return Task.from_dict(t_data) # Already done
                
            t_data["status"] = "done"
            t_data["done_at"] = datetime.now().isoformat()
            save_data(data)
            return Task.from_dict(t_data)
            
    return None

def delete_tasks(task_ids: List[int]) -> List[int]:
    """
    Deletes tasks with given IDs.
    Returns list of IDs that were actually deleted.
    """
    data = load_data()
    tasks_data = data["tasks"]
    
    initial_count = len(tasks_data)
    
    # Filter out tasks to delete
    # We want to keep tasks whose ID is NOT in task_ids
    # But we want to know which ones we found to delete.
    
    ids_set = set(task_ids)
    kept_tasks = []
    deleted_ids = []
    
    for t in tasks_data:
        if t["id"] in ids_set:
            deleted_ids.append(t["id"])
        else:
            kept_tasks.append(t)
            
    if deleted_ids:
        data["tasks"] = kept_tasks
        save_data(data)
        
    return deleted_ids

def search_tasks(query: str) -> List[Task]:
    data = load_data()
    tasks = [Task.from_dict(t) for t in data["tasks"]]
    
    query = query.lower()
    return [t for t in tasks if query in t.text.lower()]

def get_current_config() -> dict:
    data = load_data()
    return data.get("config", DEFAULT_CONFIG)

def update_config(key: str, value: Any) -> bool:
    data = load_data()
    if "config" not in data:
        data["config"] = DEFAULT_CONFIG.copy()
        
    if key in DEFAULT_CONFIG:
        # Validate types if necessary, mostly simple here
        data["config"][key] = value
        save_data(data)
        return True
    return False
