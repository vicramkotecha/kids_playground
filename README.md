# R's First Game!

A text-based survival game where you play as Batman hunting rabbits in a procedurally generated world. Chase down all the rabbits before you starve!

## Gameplay

You are Batman (🦇) in a world filled with rabbits (ᴥ). Your mission is to catch and eat all the rabbits before your hunger meter runs out.

### Features
- Procedurally generated terrain with grass (▒), trees (♣), and stone (▓)
- Hunger system that decreases over time
- Smart rabbits that move randomly but avoid walls
- Win condition: Catch all rabbits
- Lose condition: Run out of hunger

### Controls
- Arrow keys to move
- SPACE to eat nearby rabbits
- Q or ESC to quit

### Tips
- Each movement costs hunger points
- Eating a rabbit restores 40 hunger points
- Plan your route carefully to catch rabbits efficiently
- Don't let rabbits get too far away
- Watch your hunger meter!

## Code Overview

The game is built in Python and uses these main components:

### World Class
- Manages the game world and all entities
- Handles world generation with terrain features
- Controls game state and win/lose conditions

### Entity Class
- Manages moving objects (rabbits)
- Handles collision detection
- Controls random movement patterns

### Key Features
- Object-oriented design
- Real-time keyboard input
- Terminal-based graphics
- Collision detection system
- Simple AI for rabbit movement

## Requirements
- Python 3.x
- keyboard library (`pip install keyboard`)

## Running the Game
1. Install the required library: `pip install keyboard`
2. Run the game: `python game.py`

Note: On Linux systems, you might need to run with sudo privileges for keyboard input:
```bash
sudo python game.py
```

Happy hunting! 🦇🐰