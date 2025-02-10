import pygame
import sys
import random
import cv2
import numpy as np
# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Game variables
clock = pygame.time.Clock()
gravity = 0.5
bird_movement = 0
pipe_speed = 5
score = 0
high_score = 0  # High score initialized
passed_pipes = []  # List to track which pipes have been passed

# Fonts
font = pygame.font.Font(None, 50)

# Load assets
bird = pygame.Rect(100, HEIGHT // 2, 30, 30)
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Load sounds
flap_sound = pygame.mixer.Sound(r'C:\Users\Siddharth\Documents\Flappy Bird\389634__stubb__wing-flap-1.wav')
collision_sound = pygame.mixer.Sound(r'C:\Users\Siddharth\Documents\Flappy Bird\382310__mountain_man__game-over-arcade.wav')
score_sound = pygame.mixer.Sound(r'C:\Users\Siddharth\Documents\Flappy Bird\721513__baggonotes__points_tick1.wav')

def create_pipe():
    pipe_height = random.randint(150, 450)
    top_pipe = pygame.Rect(WIDTH, pipe_height - 500, 50, 500)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height + 150, 50, 500)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            pygame.mixer.Sound.play(collision_sound)
            return False
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        pygame.mixer.Sound.play(collision_sound)
        return False
    return True

def update_high_score(current_score, high_score):
    return max(current_score, high_score)

# Optical flow setup
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
roi = (100, 100, 300, 300)  # Region of interest for gesture detection

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            sys.exit()
        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())

    # Optical Flow - Gesture Detection
    ret, frame = cap.read()
    if not ret:
        break

    # Process ROI for motion detection
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_roi = frame_gray[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    prev_roi = prev_gray[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

    # Calculate dense optical flow
    flow = cv2.calcOpticalFlowFarneback(prev_roi, frame_roi, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow_y = np.mean(flow[:, :, 1])  # Vertical motion (Y-axis)

    # Flap detection based on upward motion
    if flow_y < -2:  # Negative Y means upward motion
        bird_movement = -8
        pygame.mixer.Sound.play(flap_sound)

    # Update previous frame
    prev_gray = frame_gray.copy()

    # Draw ROI for debugging
    cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Bird mechanics
    bird_movement += gravity
    bird.centery += bird_movement

    # Pipe mechanics
    pipes = move_pipes(pipes)

    # Check if the bird passes through pipes and increase score
    for pipe in pipes:
        if pipe.centerx < bird.centerx and pipe not in passed_pipes:
            passed_pipes.append(pipe)
            score += 1  # Increment score when bird passes a pipe
            pygame.mixer.Sound.play(score_sound)

    # Check collisions
    game_active = check_collision(bird, pipes)

    # Drawing
    screen.fill(BLUE)
    pygame.draw.ellipse(screen, BLACK, bird)  # Bird
    draw_pipes(pipes)

    # Score display
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # High score display
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 50))

    pygame.display.update()
    clock.tick(30)

    # If game over, reset
    if not game_active:
        high_score = update_high_score(score, high_score)
        bird = pygame.Rect(100, HEIGHT // 2, 30, 30)
        pipes.clear()
        passed_pipes.clear()
        bird_movement = 0
        score = 0

cv2.destroyAllWindows()
cap.release()