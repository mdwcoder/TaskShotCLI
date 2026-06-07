[Español](README.es.md) | [English](README.en.md)

---

# TaskShotCLI (`tsk`)

Gestor ultrarrapido de microtareas para el terminal. Captura tareas al vuelo sin friccion.

## Caracteristicas

- Rapido: crear, listar y completar en un comando.
- Local: todo se guarda en `~/.tsk` como JSON.
- Limpio: interfaz simple con `rich`.
- Potente: prioridades, fechas, busqueda y filtros.
- Multiplataforma: Linux, macOS y Windows PowerShell.

## Instalacion

### Linux / macOS

```bash
git clone https://github.com/tu-usuario/TaskShotCLI.git
cd TaskShotCLI
./scripts/init.sh
```

### Windows PowerShell

```powershell
.\scripts\init.ps1
```

## Uso basico

```bash
tsk "Call Jordi"
tsk "Review logs" --today --priority high
tsk "Buy bread" --tomorrow

tsk list
tsk list --pending
tsk list --done

tsk done 1
tsk del 1
tsk search "jordi"

tsk config show
tsk config set sort_order asc
tsk config set show_completed false
```

## Estructura

- `src/tskcli`: codigo fuente.
- `scripts/`: instaladores.
- `tests/`: pruebas automatizadas.

## Requisitos

Python 3.9 o superior. `rich` se instala automaticamente.
