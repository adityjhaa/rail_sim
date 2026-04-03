# Railway Simulator

A Python-based simulation tool that visually renders train movements across a railway network based on predefined schedules.

## Features

- **JSON-based Configuration**: Dynamically loads complex railway network topologies (`network.json`) and specific train schedules (`schedule.json`).
- **Interactive Simulation Controls**: Variable simulation speeds (0.5x up to 10.0x scale) with play/pause functionality.
- **Dynamic Camera**: Smooth panning via mouse dragging and zooming via the scroll wheel or arrow keys to inspect specific stations or tracks.
- **Real-time Pathing**: Automatically computes valid paths for trains traversing between stations based on available block connections, departures, and arrivals.

## Workflow & Usage

### 1. Requirements

Ensure you have Python installed along with the required dependencies:
```bash
pip install pygame
```
*(Note: Tkinter is typically included in standard Python installations).*

### 2. Running the Simulator

Launch the main application from your terminal:
```bash
python main.py
```

### 3. Loading Data

Once the application starts, you will see the **Home Screen**.
1. Click **Browse...** under "Network File" and select a valid network topography file (e.g., `input/network.json`).
2. Click **Browse...** under "Schedule File" and select the corresponding schedule (e.g., `input/schedule.json`).
3. Click **Run Simulation** to start.

### 4. Interactive Controls (Simulation Mode)

- **Pan Camera**: Click and drag smoothly across the screen using the Left Mouse Button.
- **Zoom Camera**: Scroll the Mouse Wheel Up/Down (or use the Up/Down Arrow keys) to zoom in and out.
- **Simulation Speed**: Click the `+` and `-` UI buttons in the simulator to speed up or slow down time.
- **Pause/Resume**: Toggle the pause button to halt trains immediately.
- **Exit**: Click the exit button to stop the current run early.

### 5. End State

The simulation automatically halts when the duration of the entire schedule elapsed and all trains finish their routes. You will be prompted with an **End Screen** where you can either:
- **Restart**: Relaunch the simulation with the exact same configuration.
- **Home**: Clear the current setup and return to the main menu to load new files.
