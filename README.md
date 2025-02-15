# R's First Game!

A text-based survival game where you play as Batman hunting woodland creatures in a procedurally generated world. Chase down all the animals before you starve!

## Gameplay

You are Batman (🦇) in a world filled with fast rabbits (🐰), slower squirrels (🐿️), and a deadly wolf (🐺). Your mission is to catch and eat all the animals before your hunger meter runs out.

### Features
- Procedurally generated terrain with grass (▒), trees (♣), and stone (▓)
- Dynamic hunger system that decreases over time
- Multiple types of animals:
  - Rabbits: Very fast (speed 5) and restore 40 hunger points
  - Squirrels: Slower (speed 1) and restore 25 hunger points
  - Wolf: Deadly predator that hunts you! (speed 1)
- Smart animal behaviors:
  - Prey animals move randomly and avoid walls
  - Wolf actively hunts the player
- Danger warning system when wolf is nearby
- Win condition: Catch all prey animals (with celebratory confetti! 🎉)
- Lose conditions:
  - Get caught by the wolf
  - Run out of hunger
- Special ability: Huff and puff to blow the wolf away!
  - Costs 20 hunger points
  - Only works when wolf is within 3 squares
  - Blows wolf back 4 squares

### Controls
- Arrow keys to move
- SPACE to eat nearby animals
- H to huff and puff (blow the wolf away)
- Q or ESC to quit

### Tips
- Each movement costs hunger points
- Failed eating attempts cost 10 hunger points
- Animals block movement - you can't move into their space
- Watch out for the wolf - it will hunt you down!
- Warning appears when wolf is nearby
- Rabbits move five times faster than squirrels
- Plan your hunting strategy:
  - Keep away from the wolf at all costs
  - Chase rabbits when you have plenty of hunger
  - Hunt squirrels when you need a quick meal
  - Try to corner animals to prevent escape
  - Use SPACE to eat from adjacent squares
- Watch your hunger meter!
- Use your huff and puff ability wisely:
  - Saves you from the wolf but costs lots of hunger
  - Only works at close range
  - Great for emergency escapes

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