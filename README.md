# HandSignDrawer

A real-time hand tracking and drawing application using MediaPipe and OpenCV. Draw by moving your finger on the camera screen, use pinch gesture to move your drawing, and save it as a PNG image.

## Features

- Detects and tracks hands using MediaPipe
- Draws lines following your index finger
- Pinch gesture to move the drawing around
- Countdown before drawing starts
- Save your drawing as a transparent PNG image
- Toggle between drawing and moving modes
- Real-time FPS display

## Usage

- Run the script
- Hold your hand in front of the camera
- After a 3-second countdown, start drawing by moving your index finger
- Press **d** to toggle between drawing and moving mode
- Pinch your index finger and thumb to move the drawing
- Press **s** to save the drawing as `my_sign.png`
- Press **q** to quit

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

Install dependencies with:

```bash
pip install opencv-python mediapipe numpy
