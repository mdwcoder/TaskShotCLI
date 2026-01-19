import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch

from tskcli import logic, model, storage

@pytest.fixture
def mock_storage(tmp_path):
    # Mock the TASKS_FILE to point to a temp file
    store = tmp_path / ".tsk"
    with patch("tskcli.storage.TASKS_FILE", store):
        # We also need to reload logic or ensure it calls storage functions that use the patched variable?
        # storage.TASKS_FILE is imported in storage.py.
        # But `load_data` uses `TASKS_FILE`.
        # Patching `tskcli.storage.TASKS_FILE` works if `load_data` looks up `TASKS_FILE` globally.
        # Yes.
        yield store

def test_add_task(mock_storage):
    t = logic.add_task("Test Task", priority="high", due="2026-01-20")
    assert t.id == 1
    assert t.text == "Test Task"
    assert t.priority == "high"
    
    data = storage.load_data()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["text"] == "Test Task"

def test_delete_multiple(mock_storage):
    logic.add_task("T1")
    logic.add_task("T2")
    logic.add_task("T3")
    
    deleted = logic.delete_tasks([1, 3])
    assert 1 in deleted
    assert 3 in deleted
    assert 2 not in deleted
    
    tasks = logic.list_tasks(show_all=True)
    ids = [t.id for t in tasks]
    assert 1 not in ids
    assert 3 not in ids
    assert 2 in ids

def test_complete_task(mock_storage):
    t = logic.add_task("To complete")
    assert t.status == "pending"
    
    t2 = logic.complete_task(t.id)
    assert t2.status == "done"
    assert t2.done_at is not None
    
    tasks = logic.list_tasks(show_all=True)
    assert tasks[0].status == "done"

def test_list_filtering(mock_storage):
    logic.add_task("Pending 1")
    t2 = logic.add_task("Done 1")
    logic.complete_task(t2.id)
    
    # Default config shows pending (if show_completed is True default? No wait. 
    # Default config has show_completed=True.)
    
    # Check default list
    all_t = logic.list_tasks()
    # logic puts completed at bottom or top depending on sort?
    # but filters?
    # list_tasks logic:
    # if pending_only -> pending
    # elif done_only -> done
    # elif not config.show_completed -> pending
    # else -> all (implicit)
    
    assert len(all_t) == 2
    
    # Filter pending
    pending = logic.list_tasks(pending_only=True)
    assert len(pending) == 1
    assert pending[0].text == "Pending 1"
    
    # Filter done
    done = logic.list_tasks(done_only=True)
    assert len(done) == 1
    assert done[0].text == "Done 1"

def test_storage_corruption_handling(mock_storage):
    # Write garbage
    with open(mock_storage, "w") as f:
        f.write("{ invalid json")
        
    # Should not crash, just return empty
    tasks = logic.list_tasks()
    assert tasks == []
    
    # Should have backed up
    # Note: load_data creates backup if corrupt
    assert os.path.exists(str(mock_storage) + ".bak")

def test_atomic_write(mock_storage):
    logic.add_task("Atomic")
    assert mock_storage.exists()
    
    # Check content
    with open(mock_storage) as f:
        data = json.load(f)
    assert data["tasks"][0]["text"] == "Atomic"
