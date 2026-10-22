
import contextlib
import io
import math
import unittest

import waypoint as w


class TestWaypoint(unittest.TestCase):
    def test_wrap180(self):
        self.assertEqual(w.wrap180(350), -10)
        self.assertEqual(w.wrap180(-190), 170)
        self.assertEqual(w.wrap180(10), 10)

    def test_units(self):
        self.assertAlmostEqual(w.step(0, 0, 0, 1, 0)[2], 9.0)   # 90 deg/s
        self.assertAlmostEqual(w.step(0, 0, 0, 0, 1)[1], 0.2)   # 2 m/s

    def test_shortest_turn_across_360(self):
        self.assertGreater(w.controller(0, 0, 350, 1, 5)[0], 0)   # go right
        self.assertLess(w.controller(0, 0, 10, -1, 5)[0], 0)      # go left

    def test_target_behind_turns_in_place(self):
        turn, drive = w.controller(0, 0, 0, 0, -10)
        self.assertEqual(drive, 0)
        self.assertEqual(abs(turn), 1)

    def test_commands_stay_in_range(self):
        for hdg in range(0, 360, 15):
            for wx, wy in [(5, 5), (-3, 8), (0.2, -0.1), (-50, -50)]:
                turn, drive = w.controller(1, 2, hdg, wx, wy)
                self.assertTrue(-1 <= turn <= 1 and -1 <= drive <= 1)

    def test_reaches_every_waypoint(self):
        route = [(10, 10), (-5, 20), (0, 0), (0.3, 0.2)]
        for start_heading in (0, 90, 180, 270, 355):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                x, y, _ = w.follow(0, 0, start_heading, route)
            self.assertLessEqual(math.hypot(x - 0.3, y - 0.2), w.REACHED_RADIUS)
            self.assertEqual(out.getvalue().count("reached at"), len(route))


if __name__ == "__main__":
    unittest.main()