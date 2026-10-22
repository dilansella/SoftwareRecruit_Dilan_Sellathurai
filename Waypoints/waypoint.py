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