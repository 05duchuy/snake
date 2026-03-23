# snake
Snake Game
# Overview
A classic implementation of the Snake game designed to demonstrate core gameplay loops, movement mechanics, and difficulty balancing.

# Controls
Use the Arrow Keys (Up, Down, Left, Right) to control the snake.

# Gameplay Mechanics
Objective: Collect the red food items to increase the snake's length and earn points.

Collision: The game ends if the snake hits the boundaries or its own body.

# Difficulty and Scoring System
The game features three difficulty levels to test player reflexes and strategy:

Easy: Slow movement speed with standard scoring.
Normal: Moderate movement speed with increased score rewards.
Hard: High movement speed with the highest score rewards per item collected.

The variable speed and point scaling were implemented to explore basic "Risk vs. Reward" design principles.

# Data Persistence
High Score: The game tracks the highest score achieved and saves it to a highscore.txt file, allowing players to track their progress across different sessions.

# Technical Stack
Language: Python

Library: Pygame