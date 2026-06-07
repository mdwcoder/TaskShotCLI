[Español](README.es.md) | [English](README.en.md)

---

# TaskShotCLI (tsk)

Ultra-fast micro task manager for the terminal. Capture tasks on the fly without friction.

## Features

- 🚀 **Fast**: One command to create, list, and complete tasks.
- 📂 **Local**: Everything is stored in `~/.tsk` (JSON). No cloud, no logins.
- 🎨 **Clean**: Simple interface powered by `rich`.
- 🔍 **Powerful**: Priorities, dates, search, and filters.
- 🛠 **Cross-platform**: Linux, macOS, Windows (PowerShell).

## Installation

### Linux / macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/tu-usuario/TaskShotCLI.git
   cd TaskShotCLI
   ```
2. Run the setup script:
   ```bash
   ./scripts/init.sh
   # Restart your terminal or source your rc file
   ```

### Windows (PowerShell)

1. Clone the repository.
2. Run the script:
   ```powershell
   .\scripts\init.ps1
   # Restart your PowerShell session
   ```

## Basic Usage

```bash
# Create a task
tsk "Call Jordi"
tsk "Review logs" --today --priority high
tsk "Buy bread" --tomorrow

# List tasks
tsk list           # Pending and completed (latest first)
tsk list --pending # Pending only
tsk list --done    # Completed only

# Mark as done
tsk done 1

# Delete
tsk del 1
tsk del 2 3 4      # Multiple IDs

# Search
tsk search "jordi"

# Configuration
tsk config show
tsk config set sort_order asc   # Change order
tsk config set show_completed false
```

## Project Structure

- `src/tskcli`: Source code (Python).
- `scripts/`: Setup scripts.
- `tests/`: Automated tests.

## Requirements

- Python 3.9+
- `rich` (installed automatically)
