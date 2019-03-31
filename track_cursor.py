#! python3

import pyautogui
print("Press Ctrl+C to quit.")

try:
	while True:
		x, y = pyautogui.position()
		R, G, B = pyautogui.pixel(x,y)
		position_str = 'X: ' + str(x).rjust(4) + '   Y: ' + str(y).rjust(4) + '   RGB:' + str(R).rjust(4) + str(G).rjust(4) + str(B).rjust(4)
		print(position_str, end="\r")

except KeyboardInterrupt:
	print("\nDone")