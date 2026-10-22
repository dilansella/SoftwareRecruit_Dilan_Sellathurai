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

def step(x, y, heading, turn_cmd, drive_cmd):
    turn = clamp(turn_cmd) * MAX_TURN_RATE * DT
    mid = math.radians(heading + turn / 2)
    dist = clamp(drive_cmd) * MAX_SPEED * DT
    return (x + dist * math.sin(mid), y + dist * math.cos(mid),
            (heading + turn) % 360)

def follow(x, y, heading, waypoints):
    turn = drive = 0.0
    steps = 0
    for i, (wx, wy) in enumerate(waypoints, 1):
        start = steps 
        while math.hypot(wx - x, wy-y) > REACHED_RADIUS:
            if (steps - start) * DT > TIMEOUT_S:
                print(f"Waypoint {i} time out")
                return x, y, heading
            turn, drive = controller(x, y, heading, wx, wy)
            x, y, heading = step(x, y, heading, turn, drive)
            steps += 1
            if steps % 10 ==0: 
                print(f"t={steps * DT:6.1f}s pos=({x:7.2f}, {y:7.2f}) "
                      f"hdg={heading:6.1f} turn={turn:+.2f} drive={drive:.2f}")
                print(f"Waypoint {i} reached ({x:.2f}, {y:.2f})")
    turn = drive = 0.0 
    print(f" completed moving, turn_cmd={turn:.2f}, drive_cmd={drive:.2f}")
    return x, y, heading

def ask_float(prompt):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print(" Please use a whole numbber avoe one")

def ask_count(prompt):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("  Please enter a whole number of at least 1.")
 

def main(): 
    print("Units in meters. Heading in degrees")
    x = ask_float("x:")
    y = ask_float("y:")
    heading = ask_float("start heading :") % 360
    while True:
        count = ask_count("# of waypoints?: ")
        waypoints = []
        for i in range(1, count + 1):
            waypoints.append((ask_float(f"waypoint {i} x:")),
                              ask_float(f"waypoimt {i} y:"))
        x, y, heading = follow(x, y, heading, waypoints)
        if input("more waypoitns? (y/n):  ").strip().lower() != "y":
            break
                              
if __name__ == "__main__":
    main()