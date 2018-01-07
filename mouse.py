import pyautogui, sys
print('Press Ctrl-C to quit.')
pyautogui.FAILSAFE=False
for i in range(0,1000,100):
    for j in range(0,1000,100):
        pyautogui.moveTo(j,i,0.01)
