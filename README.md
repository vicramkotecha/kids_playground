# R's First Game!

A text-based survival game where you play as Batman hunting woodland creatures in a procedurally generated world. Chase down all the animals before you starve!

## Gameplay

You are Batman (🦇) in a world filled with fast rabbits (🐰) and slower squirrels (🐿️). Your mission is to catch and eat all the animals before your hunger meter runs out.

### Features
- Procedurally generated terrain with grass (▒), trees (♣), and stone (▓)
- Dynamic hunger system that decreases over time
- Two types of prey with different behaviors:
  - Rabbits: Fast (speed 2) and restore 40 hunger points
  - Squirrels: Slower (speed 1) and restore 25 hunger points
- Smart animals that move randomly but avoid walls
- Escape mechanics: Animals have a 50% chance to escape when caught
- Win condition: Catch all animals (with celebratory confetti! 🎉)
- Lose condition: Run out of hunger

### Controls
- Arrow keys to move
- SPACE to eat nearby animals
- Q or ESC to quit

### Tips
- Each movement costs hunger points
- Failed eating attempts cost 10 hunger points
- Animals might escape by jumping away from you
- Rabbits move twice as fast as squirrels
- Rabbits give more hunger points but are harder to catch
- Squirrels are easier to catch but give less hunger
- Plan your hunting strategy:
  - Chase rabbits when you have plenty of hunger
  - Hunt squirrels when you need a quick meal
  - Don't miss your attempts to eat - it's costly!
  - Try to corner animals to prevent escape
- Watch your hunger meter!

## Code Overview

The game is built in Python and uses these main components:

### World Class
- Manages the game world and all entities
- Handles world generation with terrain features
- Controls game state and win/lose conditions
- Tracks different animal types and their counts

### Entity Class
- Manages moving objects (rabbits and squirrels)
- Handles collision detection
- Controls speed-based movement patterns
- Implements different movement speeds for different animals

### Key Features
- Object-oriented design
- Real-time keyboard input
- Terminal-based graphics
- Collision detection system
- Speed-based movement system
- Multiple animal types with different behaviors

## Requirements
- Python 3.x
- keyboard library (`pip install keyboard`)

## Running the Game
1. Install the required library: `pip install keyboard`
2. Run the game: `python game.py`

Note: On Linux systems, you might need to run with sudo privileges for keyboard input: