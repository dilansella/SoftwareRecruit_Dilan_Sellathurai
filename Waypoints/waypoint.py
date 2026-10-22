"waypoint.py - rover that goes through waypoints"

import math

DT = 0.1
MAX_TURN_RATE = 90.0
MAX_SPEED = 2.0
REACHED_RADIUS = 0.5
TURN_GAIN_DEG = 45.0
SLOW_RADIUS = 2.0
MIN_DRIVE = 0.2
TIMEOUT_S = 600

def wrap180(angle):
    return (angle + 180) % 360 - 180

def clamp(value, low=-1.0, high=1.0):
    return max(low, min(high, value))

def controller(x,y, heading,wx, wy):
    dx, dy, = wx - x, wy - y
    distance = math.hypot(dx, dy)
    bearing = math.degrees(math.atan2(dx,dy))
    error = wrap180(bearing - heading)
    turn_cmd = clamp(error / TURN_GAIN_DEG)
    allignment = max(0.0, 1 - abs(error) / TURN_GAIN_DEG)
    approach = clamp(distance / SLOW_RADIUS, MIN_DRIVE, 1.0)
    return turn_cmd , allignment * approach

