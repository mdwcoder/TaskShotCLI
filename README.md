# TaskShotCLI (tsk)

Micro gestor de tareas ultra rápido para terminal. Captura tareas al vuelo sin fricción.

## Características

- 🚀 **Rápido**: Un comando para crear, listar, completar.
- 📂 **Local**: Todo se guarda `~/.tsk` (JSON). Sin nubes ni logins.
- 🎨 **Bonito**: Interfaz limpia usando `rich`.
- 🔍 **Potente**: Prioridades, fechas, búsqueda, filtros.
- 🛠 **Multiplataforma**: Linux, macOS, Windows (PowerShell).

## Instalación

### Linux / macOS

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/TaskShotCLI.git
   cd TaskShotCLI
   ```
2. Ejecutar script de instalación:
   ```bash
   ./scripts/init.sh
   # Reinicia tu terminal o haz source de tu rc file
   ```

### Windows (PowerShell)

1. Clonar el repositorio.
2. Ejecutar script:
   ```powershell
   .\scripts\init.ps1
   # Reinicia tu sesión de PowerShell
   ```

## Uso Básico

```bash
# Crear tarea
tsk "Llamar a Jordi"
tsk "Revisar logs" --today --priority high
tsk "Comprar pan" --tomorrow

# Listar
tsk list           # Pendientes y completadas (últimas arriba)
tsk list --pending # Solo pendientes
tsk list --done    # Solo hechas

# Marcar como hecha
tsk done 1

# Borrar
tsk del 1
tsk del 2 3 4      # Múltiples IDs

# Buscar
tsk search "jordi"

# Configuración
tsk config show
tsk config set sort_order asc   # Cambiar orden
tsk config set show_completed false
```

## Estructura del Proyecto

- `src/tskcli`: Código fuente (Python).
- `scripts/`: Scripts de inicialización.
- `tests/`: Tests automatizados.

## Requisitos

- Python 3.9+
- `rich` (se instala automáticamente)
