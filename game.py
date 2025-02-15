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
        # Check adjacent squares for animals
        for animal in self.animals[:]:
            if (abs(animal.x - self.player_pos[0]) <= 1 and 
                abs(animal.y - self.player_pos[1]) <= 1):
                self.animals.remove(animal)
                # Rabbits give more hunger points because they're harder to catch
                hunger_boost = 40 if animal.symbol == self.blocks['rabbit'] else 25
                self.player_hunger = min(100, self.player_hunger + hunger_boost)
                return True
        return False

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
        
        # Check win/lose conditions
        if world.game_won:
            print("\nCongratulations! You've caught all the animals!")
            break
        
        if world.player_hunger <= 0:
            print("\nGame Over! You starved!")
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
