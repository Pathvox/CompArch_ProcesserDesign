# CompArch_ProcesserDesign

This repository currently contains:

- The Minterm Matrix website (`soplogic.py` + `web/index.html`)
- A Memory Hierarchy simulation (`memoryhierarchy.py`, `main.py`)
- A browser view for simulation output (`web_output.py`)

## Requirements

- Python 3.10+ (tested with Python 3.12)

## Run The Memory Hierarchy Simulation (Terminal)

```powershell
python .\main.py
```

This runs all 3 demos:

- Demo 1: Basic simulation (LRU)
- Demo 2: Eviction demo (FIFO)
- Demo 3: Write-back demo (Random)

## View Memory Hierarchy Output In A Web Page

```powershell
python .\web_output.py
```

Then open:

- http://127.0.0.1:8000

The page re-runs the demos and renders the full output in-browser.

## Run The Minterm Matrix Website

```powershell
python .\soplogic.py
```

Then open:

- http://127.0.0.1:8000

### Minterm Matrix Features

- Build Mode: Enter truth-table values in a web UI
- Auto-rendered truth table
- Karnaugh map visualization (2, 3, and 4 variables)
- Game Mode: Guess outputs and reveal the function
- Core SOP/truth-table/K-map logic in `soplogic.py`
