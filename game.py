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
        
        # Try all possible directions in random order
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Check if new position is valid and free      
            if (world.is_position_free(new_x, new_y, self) and 
                not world.is_near_wall(new_x, new_y)):
                self.x = new_x
                self.y = new_y
                return  # Successfully moved
        
        # If we get here, no valid move was found - stay in place

def select_character():
    characters = [
        ('Batman', '🦇', "The Dark Knight - Master of stealth"),
        ('Robin', '🐦', "The Wonder"),
        ('Spider-Man', '🕷️', "Your friendly neighborhood spider"),
        ('Black Panther', '🐆', "Wakanda Forever!"),
        ('Iron Man', '🤖', "Genius, billionaire, philanthropist"),
        ('Captain America', '🛡️', "The First Avenger"),
        ('Wonder Woman', '⚔️', "Amazon warrior princess"),
        ('Superman', '💪', "The Man of Steel"),
        ('Hulk', '💚', "The strongest there is!"),
        ('Princess Peach', '👸', "Ruler of the Mushroom Kingdom")
    ]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Choose Your Hero! ===\n")
    
    for i, (name, emoji, desc) in enumerate(characters, 1):
        print(f"{i}. {emoji} {name} - {desc}")
    
    while True:
        try:
            choice = input(f"\nEnter the number of your hero (1-{len(characters)}): ")
            idx = int(choice) - 1
            if 0 <= idx < len(characters):
                return characters[idx][0], characters[idx][1]
            else:
                print(f"Please enter a number between 1 and {len(characters)}")
        except ValueError:
            print("Please enter a valid number")

class World:
    def __init__(self, width=40, height=20, level=1):
        self.width = width
        self.height = height
        self.level = level
        self.hero_name, self.hero_symbol = select_character()
        self.blocks = {
            'air': ' ',
            'grass': '▒',
            'tree': '♣',
            'stone': '▓',
            'player': self.hero_symbol,  # Use selected character
            'rabbit': '🐰',
            'squirrel': '🐿️',
            'wolf': '🐺'
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
        self.game_over = False
        self.game_over_message = ""
        self.can_huff = True  # Add cooldown for huff ability

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

    def is_position_free(self, x, y, ignore_entity=None):
        """Check if a position is free of walls and other animals"""
        # Check bounds and walls
        if (x < 0 or x >= self.width or 
            y < 0 or y >= self.height or 
            self.world_map[y][x] != self.blocks['air']):
            return False
            
        # Check for other animals
        for animal in self.animals:
            if animal != ignore_entity and animal.x == x and animal.y == y:
                return False
                
        # Check for player
        if x == self.player_pos[0] and y == self.player_pos[1]:
            return False
            
        return True

    def spawn_initial_animals(self):
        self.animals = []
        self.spawn_animals(6, 'rabbit', speed=5)
        self.spawn_animals(4, 'squirrel', speed=1)
        # Spawn wolves based on level
        self.spawn_animals(self.level, 'wolf', speed=1)

    def spawn_animals(self, count, animal_type, speed):
        spawned = 0
        attempts = 0
        max_attempts = 100 * count  # Increase max attempts to find valid positions
        
        while spawned < count and attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            if self.is_position_free(x, y) and not self.is_near_wall(x, y):
                self.animals.append(Entity(x, y, self.blocks[animal_type], speed))
                spawned += 1
            
            attempts += 1

    def update_animals(self):
        # Move animals randomly
        for animal in self.animals:
            if random.random() < 0.3:  # 30% chance to move
                if animal.symbol == self.blocks['wolf']:
                    self.move_wolf(animal)  # Wolves hunt the player
                else:
                    animal.move_random(self)
        
        # Check for win condition
        if len(self.animals) == 0:
            self.game_won = True

    def move_wolf(self, wolf):
        # 80% chance to chase player, 20% chance to move randomly
        if random.random() < 0.8:
            # Chase player with some randomness
            dx = 0 if self.player_pos[0] == wolf.x else (1 if self.player_pos[0] > wolf.x else -1)
            dy = 0 if self.player_pos[1] == wolf.y else (1 if self.player_pos[1] > wolf.y else -1)
            
            # 30% chance to only move in one direction instead of both
            if random.random() < 0.3 and dx != 0 and dy != 0:
                if random.random() < 0.5:
                    dy = 0  # Only move horizontally
                else:
                    dx = 0  # Only move vertically
            
            # 10% chance to move in a random perpendicular direction
            if random.random() < 0.1:
                if dx != 0:
                    dx = 0
                    dy = random.choice([-1, 1])
                else:
                    dy = 0
                    dx = random.choice([-1, 1])
            
            new_x = wolf.x + dx
            new_y = wolf.y + dy
        else:
            # Random movement like other animals
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            new_x = wolf.x + dx
            new_y = wolf.y + dy
        
        # Check if move is valid
        if self.is_position_free(new_x, new_y, wolf) and not self.is_near_wall(new_x, new_y):
            wolf.x = new_x
            wolf.y = new_y
        
        # Check if wolf caught player
        if (abs(wolf.x - self.player_pos[0]) <= 1 and 
            abs(wolf.y - self.player_pos[1]) <= 1):
            self.game_over = True
            self.game_over_message = "💀 GAME OVER! The wolf got you! 💀"

    def update_hunger(self):
        current_time = time.time()
        if current_time - self.last_move_time >= 1:  # Decrease hunger every second
            self.player_hunger = max(0, self.player_hunger - 0.5)  # Reduced hunger decay
            self.last_move_time = current_time

    def check_win_condition(self):
        # Count only prey animals (not the wolf)
        prey_remaining = sum(1 for animal in self.animals 
                           if animal.symbol in [self.blocks['rabbit'], self.blocks['squirrel']])
        return prey_remaining == 0

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        display_world = [row[:] for row in self.world_map]
        
        for animal in self.animals:
            display_world[animal.y][animal.x] = animal.symbol
        
        # If game over by wolf, show skull instead of bat
        if self.game_over and "wolf got you" in self.game_over_message.lower():
            display_world[self.player_pos[1]][self.player_pos[0]] = '💀'
        else:
            display_world[self.player_pos[1]][self.player_pos[0]] = self.blocks['player']
        
        print('=' * (self.width + 2))
        for row in display_world:
            line = ''.join(row)
            print(f"|{line}|")
        print('=' * (self.width + 2))
        
        filled_blocks = int(self.player_hunger // 10)
        empty_blocks = 10 - filled_blocks
        hunger_bar = f"Hunger: {'█' * filled_blocks}{'-' * empty_blocks}"
        print(f"\nLevel {self.level} - {self.hero_name}")
        print(f"Hunger: {'█' * filled_blocks}{'-' * empty_blocks} ({int(self.player_hunger)}%)")
        
        rabbits = sum(1 for animal in self.animals if animal.symbol == self.blocks['rabbit'])
        squirrels = sum(1 for animal in self.animals if animal.symbol == self.blocks['squirrel'])
        wolves = sum(1 for animal in self.animals if animal.symbol == self.blocks['wolf'])
        print(f"Rabbits remaining: {rabbits}")
        print(f"Squirrels remaining: {squirrels}")
        print(f"Wolves hunting you: {wolves}")
        print("\nControls: Arrow keys to move, SPACE to eat nearby animals, H to huff and puff, Q to quit")
        
        # Add wolf warning if nearby
        for animal in self.animals:
            if (animal.symbol == self.blocks['wolf'] and 
                abs(animal.x - self.player_pos[0]) <= 3 and 
                abs(animal.y - self.player_pos[1]) <= 3):
                print("\n⚠️ WARNING: Wolf nearby! ⚠️")

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # First check if we can move to the new position
        if (0 <= new_x < self.width and 
            0 <= new_y < self.height and 
            self.world_map[new_y][new_x] == self.blocks['air']):
            
            # Check if there's an animal in the way
            for animal in self.animals:
                if animal.x == new_x and animal.y == new_y:
                    return  # Can't move into animal's space
            
            # If no animal blocking, move player
            self.player_pos = [new_x, new_y]
            self.player_hunger = max(0, self.player_hunger - 1)  # Movement still costs hunger

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
        
        print(f"\n💀 GAME OVER! {self.hero_name} has starved! 💀")
        time.sleep(2)  # Pause to show final message

    def huff_and_puff(self):
        # Find all wolves
        wolves = [animal for animal in self.animals if animal.symbol == self.blocks['wolf']]
        if not wolves:
            return "No wolves in sight!"
            
        wolves_blown = 0
        total_distance = 0
        
        # Try to blow each wolf
        for wolf in wolves:
            # Calculate distance to wolf
            dx = wolf.x - self.player_pos[0]
            dy = wolf.y - self.player_pos[1]
            distance = max(abs(dx), abs(dy))
            
            # Blow distance decreases with distance to wolf
            if distance <= 3:
                blow_distance = 4  # Full power at close range
            elif distance <= 6:
                blow_distance = 3  # Medium power at medium range
            elif distance <= 9:
                blow_distance = 2  # Weak at long range
            else:
                blow_distance = 1  # Very weak at very long range
            
            # Normalize direction
            dir_x = dx/max(abs(dx), 1) if dx != 0 else 0
            dir_y = dy/max(abs(dy), 1) if dy != 0 else 0
            
            # Try to blow wolf away
            success = False
            for test_distance in range(blow_distance, 0, -1):
                if success:
                    break
                    
                new_x = wolf.x + int(dir_x * test_distance)
                new_y = wolf.y + int(dir_y * test_distance)
                
                # Try positions around the target point
                for offset_x in [0, -1, 1]:
                    if success:
                        break
                    for offset_y in [0, -1, 1]:
                        test_x = new_x + offset_x
                        test_y = new_y + offset_y
                        
                        if (0 <= test_x < self.width and 
                            0 <= test_y < self.height and 
                            self.is_position_free(test_x, test_y, wolf) and 
                            not self.is_near_wall(test_x, test_y)):
                            # Found a valid position!
                            wolf.x = test_x
                            wolf.y = test_y
                            wolves_blown += 1
                            total_distance = max(total_distance, blow_distance)
                            success = True
                            break
        
        if wolves_blown == 0:
            return "No clear path to blow wolves!"
            
        # Cost hunger only once, even if blowing multiple wolves
        self.player_hunger = max(0, self.player_hunger - 20)
        
        # Add debug information
        print(f"DEBUG: Blown {wolves_blown} out of {len(wolves)} wolves")
        
        return f"success:{total_distance}:{wolves_blown}"

def show_victory_celebration(width, height):
    confetti = [
        '🎉', '🎊', '✨', '⭐', '🌟', '🎈',
        '🔵', '🟦', '💠', '🌐',
        '🟢', '🟩', '💚', '🌿',
        '🌈', '🦄', '🎨',  
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

def show_level_transition():
    messages = [
        "🌙 Night falls... More wolves emerge... 🌙",
        "🐺 The pack is growing... 🐺",
        "Level 2: Double Trouble!",
        "Can our hero survive against TWO wolves?",
        "Get ready..."
    ]
    
    for msg in messages:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 10)
        print(" " * 20 + msg)
        time.sleep(1)

def main():
    try:
        import keyboard
    except ImportError:
        print("Please install the 'keyboard' library first:")
        print("pip install keyboard")
        return

    level = 1
    while level <= 2:  # Support for two levels
        world = World(level=level)
        
        while True:
            world.update_animals()
            world.update_hunger()
            world.draw()
            
            if world.check_win_condition():
                if level == 1:
                    print(f"\nLevel 1 Complete! {world.hero_name} has caught all the prey animals!")
                    show_victory_celebration(world.width, world.height)
                    show_level_transition()
                    level += 1
                    break  # Break inner loop to start level 2
                else:
                    print(f"\nCongratulations! {world.hero_name} has beaten both levels!")
                    print(f"You are the ultimate {world.hero_name}! {world.hero_symbol}")
                    show_victory_celebration(world.width, world.height)
                    return  # End game after beating level 2
            
            if world.game_over:
                print(f"\n{world.game_over_message}")
                return  # End game if caught by wolves
                
            if world.player_hunger <= 0:
                world.show_game_over_animation()
                return  # End game if starved
            
            try:
                event = keyboard.read_event(suppress=True)
                if event.event_type != 'down':
                    continue
                    
                if event.name == 'h':
                    result = world.huff_and_puff()
                    if result.startswith("success"):
                        parts = result.split(":")
                        distance = parts[1]
                        wolves_count = parts[2]
                        if distance == "4":
                            print(f"\n💨 *WHOOSH* You blow {wolves_count} wolves away with full force! 💨")
                        elif distance == "3":
                            print(f"\n💨 *WHOOSH* {wolves_count} wolves are pushed back! 💨")
                        elif distance == "2":
                            print(f"\n💨 {wolves_count} wolves stumble back a bit 💨")
                        else:
                            print(f"\n💨 {wolves_count} wolves barely feel the breeze 💨")
                        time.sleep(0.5)
                    else:
                        print(f"\n❌ Can't huff and puff: {result}")
                        time.sleep(0.5)
                elif event.name == 'q' or event.name == 'esc':
                    print("\nThanks for playing!")
                    return
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
                return

if __name__ == "__main__":
    main()
