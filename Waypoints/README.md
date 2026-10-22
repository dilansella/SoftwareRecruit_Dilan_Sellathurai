# Waypoint Following

Run: `python waypoint.py` (Python 3, nothing to install).
Tests: `python -m unittest -v`

 Directions I picked
The task doesn't say which way is "0 degrees", so I chose: 0 = +y (north),
90 = +x (east), and heading goes up when turning right. T


How the rover moves
Every 0.1 s, the commands are turned into movement from the last position.
Full turn is 90 deg/s and full drive is 2 m/s, as the task says. 


How it steers
 Where to go: `atan2` gives the direction to the waypoint and `hypot`
  gives the distance.
-hich way to turn: the heading error is wrapped into -180 to 180, so
  going from 350 to 10 degrees is a 20 degree right turn, not 340 leftt.
 Turn or drive: forward speed drops as the rover points away from the
  waypoint, and hits zero at 45 degrees off. So it turns in place when
  it's facing the wrong way, drives straight when lined up, and does a bit
  of both in between.
-Not circling:it slows down within 2 m of the waypoint, and it
  doesn't drive while pointed away. The arrival circle (0.5 m) is bigger
  than its tightest turn at that speed (about 0.3 m), so it re-aims instead
  of orbiting the waypoint.


Waypoints
They're visited in the order entered, and within 0.5 m counts as reached.
After the last one, the program says it's done, sets both commands to 0,
a
Testing
`test_waypoint.py` checks: angle wrapping, the unit scaling (90 deg/s,
2 m/s), turning the short way across 0/360, turning in place when the
waypoint is behind, commands staying between -1 and 1, and a multi-waypoint
route from five different starting headings.

# What would be different in the Utah desert
-GPS isn't exact. Errors are metres, so a 0.5 m arrival circle is
  smaller than what GPS can reliably measure.
-Heading sensors are noisy. Gyros drift, and magnetometers get thrown
  off by metal and motors.
-Sand and slopes cause slip,so the rover won't move exactly as
  commanded. Motors also take time to speed up.
-Real waypoints are latitude/longitude,which would need converting to
  metres first.
-There are rocks and ditches, so a real rover needs to see obstacles and
  plan around them, and needs an emergency stop.