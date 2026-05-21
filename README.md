
# Knucklebones ML

This is a Python PettingZoo implementation of the dice game "Knucklebones" from the video game Cult of the Lamb.

## Features
- PVP, PVAI, and AI vs AI game modes
- Multiple AI agents with different strategies
- Multiple rendering options with human input support
- Simulation of multiple games to gather statistics
- Easy to extend with new agents or game rules

## Requirements
- Python 3.12
- uv (or pip, if you must)

## Usage
1. Clone the repository:
```bash
git clone https://github.com/Vexxelle/knucklebones-ml.git
```

2. Navigate to the project directory:
```bash
cd knucklebones-ml
```

3. 
- Run any of the example scripts to see the game in action:
```bash
uv run examples/pvp_terminal_play.py
```
- Or install the package and use it in your own code:
```bash
uv pip install -e .
```

Or if you prefer pip:
- Activate your virtual environment (optional but recommended):
```bash
.venv\Scripts\activate.bat  # On Windows (cmd/powershell)
source .venv/bin/activate  # On Unix or MacOS (bash/zsh)
```
- Install the dependencies:
```bash
pip install -r requirements.txt
```
- Run any of the example scripts:
```bash
python examples/pvp_terminal_play.py
```
- Or install the package:
```bash
pip install -e .
```