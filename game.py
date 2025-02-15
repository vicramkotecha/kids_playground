import os
import random
import time

class Entity:
    def __init__(self, x, y, symbol, speed=1):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.speed = speed
        self.move_counter = 0

    def move_random(self, world):
        self.move_counter += 1
        if self.move_counter < self.speed:
            return
            
        self.move_counter = 0
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        # Try to move up to speed steps
        for _ in range(self.speed):
            new_x = self.x + dx
            new_y = self.y + dy
            
            if (0 <= new_x < world.width and 
                0 <= new_y < world.height and 
                world.world_map[new_y][new_x] == world.blocks['air'] and
                not world.is_near_wall(new_x, new_y)):
                self.x = new_x
                self.y = new_y

class World:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.blocks = {
            'air': ' ',
            'grass': '▒',
            'tree': '♣',
            'stone': '▓',
            'player': '🦇',
            'rabbit': '🐰',
            'squirrel': '🐿️'
        }
        self.world_map = self.generate_world()
        # Find the ground level at the middle of the map
        middle_x = width // 2
        for y in range(height):
            if self.world_map[y][middle_x] == self.blocks['grass']:
                self.player_pos = [middle_x, y - 1]
                break
        self.player_hunger = 100
        self.animals = []
        self.spawn_initial_animals()
        self.last_move_time = time.time()
        self.game_won = False

    def generate_world(self):
        # Initialize empty world
        world = [[self.blocks['air'] for _ in range(self.width)] for _ in range(self.height)]
        
        # Generate terrain
        ground_height = self.height - 3
        for x in range(self.width):
            # Add some variation to ground height
            variation = random.randint(-1, 1)
            current_height = ground_height + variation
            
            # Place ground blocks
            for y in range(current_height, self.height):
                world[y][x] = self.blocks['grass']
            
            # Randomly place trees
            if random.random() < 0.1 and current_height > 0:  # 10% chance
                world[current_height - 1][x] = self.blocks['tree']
            
            # Randomly place stone
            if random.random() < 0.2:  # 20% chance
                world[current_height][x] = self.blocks['stone']

        return world

    def is_near_wall(self, x, y):
        # Check if position is adjacent to any non-air blocks
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = x + dx
                check_y = y + dy
                if (0 <= check_x < self.width and 
                    0 <= check_y < self.height and 
                    self.world_map[check_y][check_x] in [self.blocks['grass'], self.blocks['stone']]):
                    return True
        return False

    def spawn_initial_animals(self):
        self.spawn_animals(6, 'rabbit', speed=2)  # 6 fast rabbits
        self.spawn_animals(4, 'squirrel', speed=1)  # 4 slower squirrels

    def spawn_animals(self, count, animal_type, speed):
        for _ in range(count):
            attempts = 0
            while attempts < 100:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if (self.world_map[y][x] == self.blocks['air'] and 
                    not self.is_near_wall(x, y)):
                    self.animals.append(Entity(x, y, self.blocks[animal_type], speed))
                    break
                attempts += 1

    def update_animals(self):
        # Move animals randomly (removed reproduction code)
        for animal in self.animals:
            if random.random() < 0.3:  # 30% chance to move
                animal.move_random(self)
        
        # Check for win condition
        if len(self.animals) == 0:
            self.game_won = True

    def update_hunger(self):
        current_time = time.time()
        if current_time - self.last_move_time >= 1:  # Decrease hunger every second
            self.player_hunger = max(0, self.player_hunger - 0.5)  # Reduced hunger decay
            self.last_move_time = current_time

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        display_world = [row[:] for row in self.world_map]
        
        for animal in self.animals:
            display_world[animal.y][animal.x] = animal.symbol
        display_world[self.player_pos[1]][self.player_pos[0]] = self.blocks['player']
        
        print('=' * (self.width + 2))
        for row in display_world:
            line = ''.join(row)
            print(f"|{line}|")
        print('=' * (self.width + 2))
        
        filled_blocks = int(self.player_hunger // 10)
        empty_blocks = 10 - filled_blocks
        hunger_bar = f"Hunger: {'█' * filled_blocks}{'-' * empty_blocks}"
        print(f"\n{hunger_bar} ({int(self.player_hunger)}%)")
        
        rabbits = sum(1 for animal in self.animals if animal.symbol == self.blocks['rabbit'])
        squirrels = sum(1 for animal in self.animals if animal.symbol == self.blocks['squirrel'])
        print(f"Rabbits remaining: {rabbits}")
        print(f"Squirrels remaining: {squirrels}")
        print("\nControls: Arrow keys to move, SPACE to eat nearby animals, Q to quit")

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if (0 <= new_x < self.width and 
            0 <= new_y < self.height and 
            self.world_map[new_y][new_x] == self.blocks['air']):
            self.player_pos = [new_x, new_y]
            self.player_hunger = max(0, self.player_hunger - 1)  # Reduced movement hunger cost

    def eat_nearby_animal(self):
        # Get player's position, accounting for emoji width
        px = self.player_pos[0]
        py = self.player_pos[1]
        
        # Check all adjacent positions including diagonals
        for animal in self.animals[:]:
            # Calculate true distance, accounting for emoji width
            dx = abs(animal.x - px)
            dy = abs(animal.y - py)
            
            # If within one space in any direction
            if dx <= 1.5 and dy <= 1:
                # 50% chance of escape
                if random.random() < 0.5:
                    # Calculate escape direction (opposite of player)
                    escape_dx = animal.x - px
                    escape_dy = animal.y - py
                    
                    # Normalize to get direction
                    if escape_dx != 0:
                        escape_dx = escape_dx // abs(escape_dx)
                    if escape_dy != 0:
                        escape_dy = escape_dy // abs(escape_dy)
                    
                    # Try to escape
                    new_x = animal.x + escape_dx
                    new_y = animal.y + escape_dy
                    
                    # Check if escape position is valid
                    if (0 <= new_x < self.width and 
                        0 <= new_y < self.height and 
                        self.world_map[new_y][new_x] == self.blocks['air'] and
                        not self.is_near_wall(new_x, new_y)):
                        animal.x = new_x
                        animal.y = new_y
                
                    # Whether escape was successful or not, it counts as a miss
                    self.player_hunger = max(0, self.player_hunger - 10)
                    return False
                
                # If didn't try to escape, get eaten
                self.animals.remove(animal)
                hunger_boost = 40 if animal.symbol == self.blocks['rabbit'] else 25
                self.player_hunger = min(100, self.player_hunger + hunger_boost)
                return True
        
        # No animal in range - costs hunger
        self.player_hunger = max(0, self.player_hunger - 10)
        return False

    def show_game_over_animation(self):
        # Find ground level at player's x position
        ground_y = self.player_pos[1]
        while ground_y < self.height and self.world_map[ground_y][self.player_pos[0]] == self.blocks['air']:
            ground_y += 1
        
        # Animate falling
        fall_y = self.player_pos[1]
        while fall_y < ground_y - 1:  # Stop one above ground
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Create display world
            display_world = [row[:] for row in self.world_map]
            
            # Add animals
            for animal in self.animals:
                display_world[animal.y][animal.x] = animal.symbol
            
            # Add falling player
            display_world[fall_y][self.player_pos[0]] = self.blocks['player']
            
            # Draw the world
            print('=' * (self.width + 2))
            for row in display_world:
                line = ''.join(row)
                print(f"|{line}|")
            print('=' * (self.width + 2))
            
            # Draw final stats
            print(f"\nHunger: {'█' * 0}{'-' * 10} (0%)")
            print(f"Rabbits remaining: {sum(1 for animal in self.animals if animal.symbol == self.blocks['rabbit'])}")
            print(f"Squirrels remaining: {sum(1 for animal in self.animals if animal.symbol == self.blocks['squirrel'])}")
            
            fall_y += 1
            time.sleep(0.2)  # Slow down the falling animation
        
        # Final position with dramatic message
        os.system('cls' if os.name == 'nt' else 'clear')
        display_world = [row[:] for row in self.world_map]
        for animal in self.animals:
            display_world[animal.y][animal.x] = animal.symbol
        display_world[ground_y - 1][self.player_pos[0]] = '💀'  # Change to skull when dead
        
        print('=' * (self.width + 2))
        for row in display_world:
            line = ''.join(row)
            print(f"|{line}|")
        print('=' * (self.width + 2))
        
        print("\n💀 GAME OVER! Batman has starved! 💀")
        time.sleep(2)  # Pause to show final message

def show_victory_celebration(width, height):
    confetti = [
        '🎉', '🎊', '✨', '⭐', '🌟', '🎈',
        '🔵', '🟦', '💠', '🌐',
        '🟢', '🟩', '💚', '🌿',
        '🌈', '🦄', '☘️', '🎨',  
        '🌺', '💫', '⚡', '🎆'   
    ]  
    celebration_frames = 5
      
    for _ in range(celebration_frames):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create empty celebration frame
        frame = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Add random confetti
        for _ in range(width * 2):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            frame[y][x] = random.choice(confetti)
        
        # Draw the frame
        print('=' * (width + 2))
        for row in frame:
            print(f"|{''.join(row)}|")
        print('=' * (width + 2))
        
        # Victory message with rainbow borders
        message = "🌈 🏆 CONGRATULATIONS! YOU WIN! 🏆 🌈"
        padding = (width - len(message)) // 2
        print('\n' + ' ' * padding + message)
        
        time.sleep(0.5)  # Pause between frames

def main():
    try:
        import keyboard
    except ImportError:
        print("Please install the 'keyboard' library first:")
        print("pip install keyboard")
        return

    world = World()
    
    while True:
        world.update_animals()
        world.update_hunger()
        world.draw()
        
        if world.game_won:
            print("\nCongratulations! You've caught all the animals!")
            show_victory_celebration(world.width, world.height)
            break
        
        if world.player_hunger <= 0:
            world.show_game_over_animation()
            break
        
        try:
            event = keyboard.read_event(suppress=True)
            if event.event_type != 'down':
                continue
                
            if event.name == 'q' or event.name == 'esc':
                print("\nThanks for playing!")
                break
            elif event.name == 'up':
                world.move_player(0, -1)
            elif event.name == 'down':
                world.move_player(0, 1)
            elif event.name == 'left':
                world.move_player(-1, 0)
            elif event.name == 'right':
                world.move_player(1, 0)
            elif event.name == 'space':
                world.eat_nearby_animal()
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()
