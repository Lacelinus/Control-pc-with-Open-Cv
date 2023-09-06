#Computer control with fingers

This project allows you to control your computer's volume and video playback using hand gestures detected by OpenCV. Specifically, you can use your thumb, index finger, middle finger, and pinky to perform the following actions:

- **Volume Increase**: Touch your thumb and index finger together to increase the computer's volume.

- **Volume Decrease**: Touch your thumb and middle finger together to decrease the computer's volume.

- **Pause Video**: Touch your thumb and pinky together to pause the video.

## Overview

This project leverages computer vision techniques to detect and interpret hand gestures in real-time, making it a versatile tool for enhancing your computer interaction.

## Usage

1. Clone or download this project to your local machine.
2. Ensure you have Python installed.
3. Install the necessary libraries by running `pip install opencv-python mediapipe pyautogui comtypes`.
4. Run the `main.py` script.
5. The application will access your computer's default camera and start monitoring your hand gestures for control.

## Dependencies

Make sure you have the following dependencies installed before running the code:

- [Python](https://www.python.org/): The programming language used for this project.
- [OpenCV](https://opencv.org/): An open-source computer vision library.
- [MediaPipe](https://mediapipe.dev/): A framework for building multimodal pipelines, including hand detection.
- [pyautogui](https://pyautogui.readthedocs.io/en/latest/): A library for controlling the mouse and keyboard to simulate keypresses and automate tasks.
- [ctypes](https://docs.python.org/3/library/ctypes.html): A Python library for interfacing with C libraries.
- [comtypes](https://pypi.org/project/comtypes/): A library for handling COM (Component Object Model) interfaces in Windows.
- [time](https://docs.python.org/3/library/time.html): A Python module for time-related functions.

Please ensure that you have these libraries installed to successfully run the code.

## Important Notes

This project provides a fun and interactive way to control your computer's audio and video playback using hand gestures. You can further customize and extend the code to suit your specific needs.

## Author

This project was created by Lacelinus. If you have any questions or suggestions, feel free to reach out at ekremkprn2@gmail.com.

Enjoy controlling your computer with hand gestures using OpenCV and MediaPipe!
