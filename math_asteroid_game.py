import pygame
import random
import time
import json
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Asteroid Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)
pause_font = pygame.font.Font(None, 74)

# Load images
background_img = pygame.Surface((screen_width, screen_height))
background_img.fill((0, 0, 80))  # Dark blue gradient
player_img = pygame.Surface((50, 50))
player_img.fill(blue)
asteroid_img = pygame.Surface((50, 50))
asteroid_img.fill((255, 0, 0))
powerup_img = pygame.Surface((30, 30))
powerup_img.fill((0, 255, 0))

# Game variables
player_pos = [screen_width // 2, screen_height - 60]
player_size = player_img.get_width()
player_speed = 5

asteroids = []
asteroid_size = asteroid_img.get_width()
asteroid_speed = 1  # Reduced speed
spawn_rate = 180  # Number of frames between each new asteroid

powerups = []
powerup_size = powerup_img.get_width()
powerup_spawn_rate = 300  # Number of frames between each new powerup

score = 0
lives = 3
level = 1

# Bullet class
class Bullet:
    def __init__(self, position):
        self.position = list(position)
        self.size = 5
        self.color = (255, 0, 0)
        self.speed = 5  # Reduced speed

    def move(self):
        self.position[1] -= self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.size)

# Function to create a new asteroid
def create_asteroid():
    x_pos = random.randint(0, screen_width - asteroid_size)
    y_pos = 0 - asteroid_size
    problem, options, solution = generate_trigonometric_problem()
    asteroids.append({"pos": [x_pos, y_pos], "problem": problem, "options": options, "solution": solution, "solved": False})

# Function to create a new powerup
def create_powerup():
    x_pos = random.randint(0, screen_width - powerup_size)
    y_pos = 0 - powerup_size
    powerups.append({"pos": [x_pos, y_pos]})

# Function to generate a trigonometric problem
def generate_trigonometric_problem():
    angle = random.choice([30, 45, 60, 90])  # Basic angles
    func = random.choice(["sin", "cos", "tan"])
    options = []
    if func == "sin":
        problem = f"sin({angle}°)"
        solution = round(math.sin(math.radians(angle)), 2)
    elif func == "cos":
        problem = f"cos({angle}°)"
        solution = round(math.cos(math.radians(angle)), 2)
    else:
        problem = f"tan({angle}°)"
        solution = round(math.tan(math.radians(angle)), 2)
    
    # Generate multiple-choice options
    options = [solution] + [round(random.uniform(-1, 1), 2) for _ in range(3)]
    random.shuffle(options)
    
    return problem, options, solution

# Function to check if the player solved the problem correctly
def check_answer(solution, answer):
    try:
        return abs(float(answer) - solution) < 0.01  # Tolerance for floating point comparisons
    except:
        return False

# Function to draw the player
def draw_player():
    screen.blit(player_img, (player_pos[0], player_pos[1]))

# Function to draw asteroids
def draw_asteroids():
    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid["pos"][0], asteroid["pos"][1]))
        problem_text = font.render(asteroid["problem"], True, white)
        screen.blit(problem_text, (asteroid["pos"][0] + 10, asteroid["pos"][1] + 10))
        for i, option in enumerate(asteroid["options"]):
            option_text = font.render(f"{i + 1}: {option}", True, white)
            screen.blit(option_text, (asteroid["pos"][0] + 10, asteroid["pos"][1] + 40 + i * 30))

# Function to draw powerups
def draw_powerups():
    for powerup in powerups:
        screen.blit(powerup_img, (powerup["pos"][0], powerup["pos"][1]))

# Function to draw the score and lives
def draw_score_and_lives():
    score_text = font.render(f"Score: {score}", True, white)
    lives_text = font.render(f"Lives: {lives}", True, white)
    level_text = font.render(f"Level: {level}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (10, 70))

# Function to draw the input box
def draw_input_box(text):
    pygame.draw.rect(screen, white, (player_pos[0], player_pos[1] - 40, 200, 30), 2)
    input_text = input_font.render(text, True, white)
    screen.blit(input_text, (player_pos[0] + 5, player_pos[1] - 35))

# Function to draw the pause screen
def draw_pause_screen():
    pause_text = pause_font.render("Paused", True, white)
    screen.fill((0, 0, 0, 150))  # Semi-transparent overlay
    screen.blit(pause_text, (screen_width // 2 - 150, screen_height // 2 - 50))
    pygame.display.flip()

# Function to save game state
def save_game():
    try:
        with open("savegame.json", "w") as file:
            json.dump({
                "player_pos": player_pos,
                "asteroids": asteroids,
                "powerups": powerups,
                "score": score,
                "lives": lives,
                "level": level
            }, file)
            print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

# Function to load game state
def load_game():
    global player_pos, asteroids, powerups, score, lives, level
    try:
        with open("savegame.json", "r") as file:
            data = json.load(file)
            player_pos = data.get("player_pos", player_pos)
            asteroids = data.get("asteroids", asteroids)
            powerups = data.get("powerups", powerups)
            score = data.get("score", score)
            lives = data.get("lives", lives)
            level = data.get("level", level)
    except Exception as e:
        print(f"Error loading game: {e}")

# Main game loop
running = True
paused = False
frame_count = 0
answer = ""
bullets = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Toggle pause
                paused = not paused
            elif event.key == pygame.K_BACKSPACE:
                answer = answer[:-1]
            elif event.key == pygame.K_RETURN:
                for asteroid in asteroids:
                    if check_answer(asteroid["solution"], answer):
                        score += 10
                        asteroid["solved"] = True
                        bullets.append(Bullet(player_pos))  # Create a bullet
                        break
                else:
                    lives -= 1
                answer = ""
            else:
                answer += event.unicode

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += player_speed

        if frame_count % spawn_rate == 0:
            create_asteroid()
        if frame_count % powerup_spawn_rate == 0:
            create_powerup()

        for asteroid in asteroids:
            asteroid["pos"][1] += asteroid_speed
            if asteroid["pos"][1] > screen_height:
                asteroids.remove(asteroid)
                lives -= 1
            elif asteroid["solved"]:
                asteroids.remove(asteroid)

        for powerup in powerups:
            powerup["pos"][1] += asteroid_speed
            if powerup["pos"][1] > screen_height:
                powerups.remove(powerup)
            elif (player_pos[0] < powerup["pos"][0] < player_pos[0] + player_size or
                  player_pos[0] < powerup["pos"][0] + powerup_size < player_pos[0] + player_size) and \
                 (player_pos[1] < powerup["pos"][1] < player_pos[1] + player_size or
                  player_pos[1] < powerup["pos"][1] + powerup_size < player_pos[1] + player_size):
                powerups.remove(powerup)
                lives += 1

        for bullet in bullets[:]:
            bullet.move()
            if bullet.position[1] < 0:
                bullets.remove(bullet)
            else:
                bullet.draw()

        if score > 0 and score % 100 == 0:
            level += 1
            asteroid_speed = max(1, asteroid_speed - 0.5)  # Further reduce the speed
            spawn_rate = max(120, spawn_rate - 10)  # Slow down the spawn rate

        screen.blit(background_img, (0, 0))
        draw_player()
        draw_asteroids()
        draw_powerups()
        draw_score_and_lives()
        draw_input_box(answer)

        pygame.display.flip()
        frame_count += 1
        clock.tick(30)
    else:
        draw_pause_screen()

    if lives <= 0:
        save_game()
        running = False

pygame.quit()

# Game over screen
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Over")
game_over_font = pygame.font.Font(None, 74)
game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
screen.fill((0, 0, 0))
screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
pygame.display.flip()
time.sleep(3)
pygame.quit()
