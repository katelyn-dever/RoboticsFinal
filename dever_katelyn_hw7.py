# Katelyn Dever
# Assignment 7

import curses
import time
from gpiozero import CamJamKitRobot, DistanceSensor

# keyboard manipulation
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

# Define GPIO pins to use for distance sensor
pintrigger = 17
pinecho = 18

# create robot and sensor objects
robot = CamJamKitRobot()
sensor = DistanceSensor(echo=pinecho, trigger=pintrigger)

# Distance variables
hownear = 15.0
reversetime = 0.5
turntime = 0.75

# set the relative speeds of the two motors,
motorspeed = 0.3

motorforward = (motorspeed, motorspeed)
motorbackward = (-motorspeed, -motorspeed)
motorleft = (0, motorspeed)
motorright = (motorspeed, 0)


# Return True if the ultrasonic sensor sees an obstacle
def isnearobstacle(localhownear):
    distance=sensor.distance*100

    print("IsNearObstacle: " +str(distance))
    if distance < localhownear:
        return True
    else:
        return False

# Move back a little, then turn right
def avoidobstacle():
    # Back off
    print("Backwards")
    robot.value = motorbackward
    time.sleep(reversetime)
    robot.stop()

    #turn right
    print("right")
    robot.value = motorright
    time.sleep(turntime)
    robot.stop()

def scuttlemode():
    # control the robot
    try:
        # scuttle forever...
        while True:
            robot.value = motorforward
            time.sleep(0.1)
            if isnearobstacle(hownear):
                robot.stop()
                avoidobstacle()
    # exit this mode with Ctrl + C
    except KeyboardInterrupt:
        robot.stop()
    
 
def main():  
    try:
        while True:
            char = screen.getch()
            # exit entire program with q
            if char == ord('q'):
                break
            # arrow robot control
            elif char == curses.KEY_UP:
                robot.value = motorforward
                time.sleep(.5)
            elif char == curses.KEY_DOWN:
                robot.value = motorbackward
                time.sleep(.5)
            elif char == curses.KEY_RIGHT:
                robot.value = motorright
                time.sleep(.5)
            elif char == curses.KEY_LEFT:
                robot.value = motorleft
                time.sleep(.5)
            # stop robot
            elif char == ord('x'):
                robot.stop()
            # scuttle mode and avoid obstacles)
            elif char == ord('s'):
                scuttlemode()
           
    finally:
        # close down curses properly, inc turn echo back on
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()

main()
