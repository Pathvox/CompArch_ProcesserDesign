# CompArch_ProcesserDesign

This repository currently contains:

- The Minterm Matrix website (`soplogic.py` + `web/index.html`)
- A Memory Hierarchy simulation (`memoryhierarchy.py`, `main.py`)
- A browser view for simulation output (`web_output.py`)
- A Single-Cycle Processor simulation + visualizer (`Mmain.py`, `processorr.py`, `visualizer_task4.html`)

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

## Run The Single-Cycle Processor + Visualizer

```powershell
python .\Mmain.py
```

This will:

- Run the required processor validation cases in terminal
- Generate `task4_results.js` from Python execution traces
- Start a local web server and open:
  - http://127.0.0.1:8000/visualizer_task4.html

Keep the terminal running while viewing the webpage.  
Stop the server with `Ctrl + C`.

### Processor Files

- `Mmain.py` - entry point, case runner, trace export, web server launcher
- `processorr.py` - processor pipeline (Fetch -> Decode -> Execute -> Write-back)
- `instruction_memory.py` - instruction encoding and fixed 3-instruction program
- `control_unit.py` - instruction decode and control signal generation
- `Alu.py` / `alu_control.py` - ALU operations and funct decoding
- `register_file.py` - register storage/read/write
- `mux.py` - mux helpers used in datapath
- `test_processor.py` - unit + integration tests
- `visualizer_task4.html` - frontend visualizer (expression, datapath, trace, timeline, truth table, k-map)

## Run Processor Tests

```powershell
python -m pytest .\test_processor.py -v
```
