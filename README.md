# Auto-Clicking for Lyto Different Color Game with OpenCV

This is an simple project with Python and Opencv for auto-gaming on Lyto color game. The project is inspired by [kketernality](https://github.com/kketernality/LytoColorHack) and [OuYangMinOa
](https://github.com/OuYangMinOa/Lyto-Different-Color)

## Demo

## Installation
```
pip install numpy
pip install opencv-python
pip install pillow
pip install pyautogui
```

## How to use 
Run the following command. The program window will pop out.
```
python LytoColorHack.py
```


* Let the browser stay at the middle of the screen. 
* Adjust the size of browser until the window can catch all of the circles in game.
* Press `s` to start auto-gaming. 
* Press `esc` to stop auto-gaming.
* If the answer cannot detected correctly, try modify the parameters `param1` and `param2` in `cv2.HoughCircles`.
