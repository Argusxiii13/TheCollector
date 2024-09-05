#USE ARROW KEYS TO NAVIGATE THE SHIP TO AVOID ASTEROID AND COLLECT MATERIALS

import turtle
import random
import time
import os

# Set up the screen
screen = turtle.Screen()
screen.setup(600, 600)
screen.title("The Collector")
screen.bgcolor("black")
screen.tracer(0)  # Disable auto screen update for smoother animation

# Function to create and register default shapes
def create_default_shapes():
    # Create triangle shape for spaceship
    triangle = turtle.Turtle()
    triangle.hideturtle()
    triangle.penup()
    triangle.goto(-10, -10)
    triangle.pendown()
    triangle.begin_poly()
    for _ in range(3):
        triangle.forward(20)
        triangle.left(120)
    triangle.end_poly()
    screen.register_shape("spaceship", triangle.get_poly())

    # Create circle shape for asteroid
    circle = turtle.Turtle()
    circle.hideturtle()
    circle.penup()
    circle.goto(0, -10)
    circle.pendown()
    circle.begin_poly()
    circle.circle(10)
    circle.end_poly()
    screen.register_shape("asteroid", circle.get_poly())

    # Create square shape for crate
    square = turtle.Turtle()
    square.hideturtle()
    square.penup()
    square.goto(-10, -10)
    square.pendown()
    square.begin_poly()
    for _ in range(4):
        square.forward(20)
        square.left(90)
    square.end_poly()
    screen.register_shape("crate", square.get_poly())

# Create default shapes
create_default_shapes()

# Function to register shapes and return the shape name
def register_shape(shape_name, default_shape):
    if os.path.isfile(shape_name):  # Check if the file exists
        screen.register_shape(shape_name)
        return shape_name  # Return the GIF name if registered
    else:
        print(f"Warning: {shape_name} not found. Using default shape: {default_shape}.")
        return default_shape  # Return the default shape if not found

# Register the spaceship images and store the resulting shapes
spaceship_shapes = {
    "up": register_shape("spaceship_up.gif", "spaceship"),
    "down": register_shape("spaceship_down.gif", "spaceship"),
    "left": register_shape("spaceship_left.gif", "spaceship"),
    "right": register_shape("spaceship_right.gif", "spaceship"),
}

# Register the asteroid GIF and crate GIFs
asteroid_shape = register_shape("asteroid.gif", "asteroid")
crate_shapes = [
    register_shape("crate1.gif", "crate"),
    register_shape("crate2.gif", "crate"),
]

# Variables for game state
player = None
crate = None
asteroids = []
score = 0
high_score = 0
game_over = False
title_display = None
score_display = None

# Function to display the title screen
def show_title_screen():
    global title_display
    title_display = turtle.Turtle()
    title_display.hideturtle()
    title_display.penup()
    
    # Title text
    title_display.goto(0, 100)
    title_display.color("white")
    title_display.write("The Collector", align="center", font=("Arial", 50, "bold"))
    
    # Instructions text
    title_display.goto(0, 30)
    title_display.write("Collect Materials, Avoid Asteroids,\n    and Don't Go Beyond Border", align="center", font=("Arial", 15, "normal"))
    
    # Start text
    title_display.goto(0, -50)
    title_display.write("Press SPACE to Start", align="center", font=("Arial", 18, "bold"))
    
    screen.onkeypress(start_game, "space")
    screen.listen()

def start_game():
    """Start the game."""
    global player, crate, asteroids, score, high_score, game_over, title_display, score_display
    score = 0
    game_over = False
    asteroids.clear()

    # Clear the title screen elements
    title_display.clear()

    # Create the player (Spaceship)
    player = turtle.Turtle()
    player.shape(spaceship_shapes["up"])  # Start facing up
    player.color("white")  # Set spaceship color to white
    player.penup()
    player.goto(0, -250)  # Starting position below

    # Create a crate-like collectible
    crate = turtle.Turtle()
    crate.penup()
    crate.goto(random.randint(-280, 280), random.randint(-250, 0))
    crate.shape(random_crate_shape())
    crate.color("yellow")  # Set crate color to yellow

    # Set up score display
    global score_display
    score_display = turtle.Turtle()
    score_display.hideturtle()
    score_display.penup()
    score_display.goto(-280, 260)
    score_display.color("white")
    update_score_display()

    # Draw a border for the game field
    draw_border()

    # Create one initial asteroid
    create_asteroid()

    # Start the main game loop
    main()

def random_crate_shape():
    """Randomly choose between two crate shapes."""
    return random.choice(crate_shapes)

def create_asteroid():
    """Create a new asteroid and add it to the asteroids list."""
    if len(asteroids) < 10:  # Limit the maximum number of asteroids to 10
        asteroid = turtle.Turtle()
        asteroid.shape(asteroid_shape)  # Use the registered shape
        asteroid.color("orange")  # Set asteroid color to grey
        asteroid.penup()
        asteroid.goto(random.randint(-280, 280), 300)  # Start from above
        asteroids.append(asteroid)

def update_score_display():
    """Update the score display."""
    global score_display
    score_display.clear()
    score_display.write(f"Score: {score} High Score: {high_score}", align="left", font=("Arial", 16, "normal"))

def draw_border():
    """Draw a border for the game field."""
    border = turtle.Turtle()
    border.penup()
    border.goto(-300, -300)
    border.pendown()
    border.pensize(3)
    border.color("white")
    for _ in range(4):
        border.forward(600)
        border.left(90)
    border.hideturtle()

def load_high_score():
    """Load the high score from a file."""
    global high_score
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except (FileNotFoundError, ValueError):
        high_score = 0

def save_high_score(score):
    """Save the high score to a file if the current score is higher."""
    global high_score
    if score > high_score:
        with open("high_score.txt", "w") as file:
            file.write(str(score))
        high_score = score

load_high_score()

def check_collisions():
    """Check for collisions with the crate, asteroids, and the border."""
    global score, game_over
    
    # Check collision with crate (object to collect)
    if player.distance(crate) < 20:
        crate.goto(random.randint(-280, 280), random.randint(-250, 0))  # Respawn in the lower half
        crate.shape(random_crate_shape())  # Alternate crate shape
        score += 1
        update_score_display()
        create_asteroid()  # Create a new asteroid when a crate is collected
    
    # Check collision with asteroids
    for asteroid in asteroids:
        if player.distance(asteroid) < 20:
            game_over = True

    # Check if player crosses the border
    if abs(player.xcor()) > 290 or abs(player.ycor()) > 290:
        game_over = True

# Define movement functions
def move_up():
    player.shape(spaceship_shapes["up"])  # Change shape to up
    player.setheading(90)
    player.forward(10)
    check_collisions()

def move_down():
    player.shape(spaceship_shapes["down"])  # Change shape to down
    player.setheading(270)
    player.forward(10)
    check_collisions()

def move_left():
    player.shape(spaceship_shapes["left"])  # Change shape to left
    player.setheading(180)
    player.forward(10)
    check_collisions()

def move_right():
    player.shape(spaceship_shapes["right"])  # Change shape to right
    player.setheading(0)
    player.forward(10)
    check_collisions()

# Set up key bindings
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

def main():
    """Main game loop."""
    global game_over
    game_over = False

    while not game_over:
        # Move asteroids
        for asteroid in asteroids:
            asteroid.sety(asteroid.ycor() - 2)  # Move downwards
            
            # Reset asteroid position if it goes off the screen
            if asteroid.ycor() < -300:
                asteroid.goto(random.randint(-280, 280), 300)

        # Check for collisions (with crate, asteroids, and the border)
        check_collisions()

        # Add a small delay to control game speed
        time.sleep(0.01)

        # Update screen
        screen.update()

    # Save high score and display final score
    save_high_score(score)
    screen.clear()
    screen.bgcolor("black")
    final_score = turtle.Turtle()
    final_score.hideturtle()
    final_score.penup()
    final_score.goto(0, 0)
    final_score.color("white")
    final_score.write(f"Game Over!\nFinal Score: {score}\nHigh Score: {high_score}", align="center", font=("Arial", 24, "bold"))

if __name__ == "__main__":
    show_title_screen()
    screen.exitonclick()
#By Janier Kim Anthony Esperida
