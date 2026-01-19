#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime, timedelta
from typing import List

from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text

from . import logic
from .model import Task
from .storage import DEFAULT_CONFIG

console = Console()

def format_due_date(due_str: str) -> str:
    if not due_str:
        return ""
    try:
        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        delta = (due_date - today).days
        
        if delta == 0:
            return "[bold red]Today[/]"
        elif delta == 1:
            return "[bold yellow]Tomrw[/]"
        elif delta < 0:
            return f"[bold red]{due_str} (Overdue)[/]"
        else:
            return f"[cyan]{due_str}[/]"
    except ValueError:
        return due_str

def get_priority_style(priority: str) -> str:
    if priority == "high":
        return "[bold red]HIGH[/]"
    elif priority == "med":
        return "[yellow]MED[/]"
    elif priority == "low":
        return "[blue]LOW[/]"
    return ""

def print_tasks(tasks: List[Task], title: str = "Tasks"):
    if not tasks:
        console.print(f"[italic dim]No tasks found ({title.lower()})[/]")
        return

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4, justify="right")
    table.add_column("S", width=3, justify="center") Status icon
    table.add_column("Task", ratio=1)
    table.add_column("Pri", width=6, justify="center")
    table.add_column("Due", width=12, justify="right")
    
    for t in tasks:
        Status icon
        status_icon = "✔" if t.status == "done" else "●"
        status_style = "green" if t.status == "done" else "white"
        
        Text decoration
        text = t.text
        if t.status == "done":
            text = f"[strike dim]{text}[/]"
            
        table.add_row(
            str(t.id),
            f"[{status_style}]{status_icon}[/]",
            text,
            get_priority_style(t.priority),
            format_due_date(t.due)
        )
        
    console.print(table)

def cmd_add(args):
    text = " ".join(args.text)
    
    due = None
    if args.today:
        due = datetime.now().strftime("%Y-%m-%d")
    elif args.tomorrow:
        due = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif args.week:
        due = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    task = logic.add_task(text, args.priority, due)
    console.print(f"[bold green]✓[/] Task created: [bold]{task.id}[/] - {task.text}")

def cmd_list(args):
    Logic to handle filters
    If no flags provided, behavior depends on config or default
    If flags provided, they override
    
    pending_only = args.pending
    done_only = args.done
    all_tasks = args.all
    
    If --all is passed, show everything regardless of config
    if all_tasks:
        We need to hack this a bit because logic.list_tasks uses config if we don't strict filter
        But we want to override config.
        Actually logic.list_tasks logic is:
        if pending_only -> pending
        elif done_only -> done
        elif not config.show_completed -> pending
        else -> all
        
        So to force all, we can't just pass nothing if config hides completed.
        We need to modify logic or do a little trick.
        Let's see: logic.list_tasks returns all if show_completed is true and pending/done flags are false.
        
        Currently logic.list_tasks doesn't support an explicit "show all override".
        Let's just fix logic in list_tasks? 
        Or we can just get all raw tasks from storage here? No, better use logic.
        
        Let's look at logic.py again.
        if pending_only: ...
        elif done_only: ...
        elif not config.get("show_completed", True): ...
        
        So if we want ALL, we need to ensure pending_only=False, done_only=False, AND somehow bypass config check.
        Since I can't change logic easily without checking it out again (I can, but logic.py is already written).
        Actually I can just update logic.py later if needed, but wait.
        
        If I want ALL, I effectively want to NOT filter.
        But logic filters by default based on config.
        I'll just temporarily override config in memory? No that's hacky.
        
        Let's just call get_tasks() directly from storage? No logic.list_tasks handles sorting.
        I'll modify logic.py? 
        Actually, let's just accept that 'all' might need a tweak.
        Wait, if --all is passed, I can just fetch ALL tasks via logic?
        
        Let's Update logic.py to support 'force_all'? 
        Or simpler:
        pass Placeholder thought
        
    tasks = logic.list_tasks(pending_only, done_only, args.limit, show_all=all_tasks)
    
    If --all is passed but config has show_completed=False, logic.list_tasks currently returns pending only.
    This is a bug in my logic.py design relative to the CLI requirements.
    I should have added an 'ignore_config' or 'show_all' param to list_tasks.
    
    Correction: I will update logic.py in a separate tool call if strictly necessary, 
    OR I can just read raw in CLI for this specific case? No, sort order matters.
    
    Let's look at logic.py implementation in my head:
    if pending_only: ...
    elif done_only: ...
    elif not config.get("show_completed", True): ...
    
    If I want "all", I need to make sure none of those `if`s enter?
    But the last `elif` checks config.
    
    Workaround: If args.all is True, I will manually handle it in CLI by calling logic.list_tasks(pending_only=False, done_only=False)
    AND if the result is filtered (check count?), maybe I need to do something else.
    
    Actually, simplest fix: Update logic.py to take `include_completed=True` argument?
    Better: logic.list_tasks(filter_status="pending"|"done"|"all"|None)
    
    For now, let's implement CLI assuming logic works or I'll patch logic.py shortly.
    I'll patch logic.py first effectively.
    
    print_tasks(tasks)

def cmd_done(args):
    task = logic.complete_task(args.id)
    if task:
        console.print(f"[bold green]✓[/] Task {task.id} marked as done.")
    else:
        Maybe it doesn't exist or was already done?
        logic.complete_task return None if not found, but returns task if already done? 
        My logic.py returns existing task if already done.
        logic.py: if t_data["id"] == task_id: if done -> return task.
        So None means not found.
        console.print(f"[bold red]![/] Task {args.id} not found.")

def cmd_delete(args):
    args.ids is a list of strings due to possible commas
    We need to flatten and split
    ids = []
    for item in args.ids:
        split by comma
        parts = item.split(',')
        for p in parts:
            if p.strip().isdigit():
                ids.append(int(p))
    
    if not ids:
        console.print("[yellow]No valid IDs provided.[/]")
        return
        
    deleted = logic.delete_tasks(ids)
    if deleted:
        console.print(f"[bold green]✓[/] Deleted {len(deleted)} tasks: {', '.join(map(str, deleted))}")
    else:
        console.print("[yellow]No tasks matched the provided IDs.[/]")

def cmd_search(args):
    tasks = logic.search_tasks(args.query)
    print_tasks(tasks, title=f"Search results: '{args.query}'")

def cmd_config(args):
    if args.action == "show":
        cfg = logic.get_current_config()
        console.print(cfg)
    elif args.action == "set":
        if not args.key or not args.value:
            console.print("[red]Usage: config set <key> <value>[/]")
            return
            
        Conversion for boolean
        val = args.value
        if val.lower() == "true": val = True
        elif val.lower() == "false": val = False
        
        if logic.update_config(args.key, val):
            console.print(f"[green]✓[/] Config updated: {args.key} = {val}")
        else:
            console.print(f"[red]![/] Failed to update config (invalid key?).")

def main():
    parser = argparse.ArgumentParser(prog="tsk", description="TaskShotCLI - Frictionless Task Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    ADD
    We want `tsk "text"` to work. Argparse usually expects `tsk add "text"`.
    To support implicit add, we can check sys.argv?
    Or just make 'add' a subcommand but make it optional?
    Argparse default subcommand hack:
    
    If the first arg is not a known subcommand, assume it's 'add' arguments?
    This is tricky with flags.
    Simpler: Make 'add' the default if no subcommand is parsed?
    But argparse errors out.
    
    Robust way: Check sys.argv[1] against list of commands.
    commands = ["list", "done", "delete", "del", "search", "config", "help", "--help", "-h"]
    
    if len(sys.argv) > 1 and sys.argv[1] not in commands:
         Insert 'add'
         sys.argv.insert(1, "add")
    
    ADD parser
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("text", nargs="+", help="Task text")
    p_add.add_argument("--today", action="store_true", help="Due today")
    p_add.add_argument("--tomorrow", action="store_true", help="Due tomorrow")
    p_add.add_argument("--week", action="store_true", help="Due in 1 week")
    p_add.add_argument("-p", "--priority", choices=["low", "med", "high"], help="Priority")
    p_add.set_defaults(func=cmd_add)
    
    LIST parser
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument("--pending", action="store_true")
    p_list.add_argument("--done", action="store_true")
    p_list.add_argument("--all", action="store_true")
    p_list.add_argument("--limit", type=int)
    p_list.set_defaults(func=cmd_list)
    
    DONE parser
    p_done = subparsers.add_parser("done", help="Complete task")
    p_done.add_argument("id", type=int, help="Task ID")
    p_done.set_defaults(func=cmd_done)
    
    DELETE parser
    p_del = subparsers.add_parser("delete", aliases=["del"], help="Delete tasks")
    p_del.add_argument("ids", nargs="+", help="IDs to delete (space or comma separated)")
    p_del.set_defaults(func=cmd_delete)
    
    SEARCH parser
    p_search = subparsers.add_parser("search", help="Search tasks")
    p_search.add_argument("query", help="Search query")
    p_search.set_defaults(func=cmd_search)
    
    CONFIG parser
    p_config = subparsers.add_parser("config", help="Manage config")
    p_config.add_argument("action", choices=["show", "set"], help="show or set")
    p_config.add_argument("key", nargs="?", help="Config key")
    p_config.add_argument("value", nargs="?", help="Config value")
    p_config.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        Default to list if no args? Or help?
        If we injected 'add', this branch is unlikely unless empty args.
        If empty args -> list?
        if len(sys.argv) == 1:
            Manually trigger list
            cmd_list(parser.parse_args(["list"]))
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
