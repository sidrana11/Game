This is a Flappy Bird clone implemented in Python using Pygame and OpenCV. 
The game allows the player to control the bird using hand gestures detected via optical flow.

Features:

Classic Flappy Bird mechanics with gravity and pipes.

Gesture-based controls using OpenCV's Optical Flow.

Real-time webcam feed to detect upward hand motions for flapping.

Sound effects for flapping, scoring, and collisions.

Tracks high score.


How to Play:

Run the script using Python:

python flappy_bird.py

Place your hand in the webcam feed within the designated region (a green rectangle).

Move your hand upwards to make the bird flap.

Avoid hitting the pipes or the ground.

The game will track and display your high score.

Press 'q' to quit the webcam feed.


Controls:

Upward Hand Motion: Makes the bird flap.

Quit: Close the game window to exit.


Notes:

Ensure your webcam is connected for gesture detection to work.

Adjust the ROI (Region of Interest) in the code if necessary.

Modify flow_y threshold if motion sensitivity needs tuning.


License:
This project is for educational purposes and personal use. Feel free to modify and enhance it!
