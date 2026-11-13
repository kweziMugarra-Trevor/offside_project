import unittest
from offside import analyse_position, check_offside_offence, get_second_last_defender, check_all_attackers


class OffsideTests(unittest.TestCase):
    def analyse(self, center, direction="right", defenders=None, ball=None, halfway=50):
        if defenders is None:
            defenders = [30, 45, 48, 52] if direction == "right" else [70, 55, 52, 48]
        if ball is None:
            ball = 40 if direction == "right" else 60
        return analyse_position(center, 2, defenders, ball, direction, halfway)

    def test_second_last_both_directions(self):
        self.assertEqual(get_second_last_defender([30, 45, 48, 52], "right"), 48)
        self.assertEqual(get_second_last_defender([70, 55, 52, 48], "left"), 52)

    def test_threshold_inclusive_both_directions(self):
        for direction, positions, line in [("right", [50, 55, 60, 70], 60), ("left", [50, 45, 40, 30], 40)]:
            ball = 50
            with self.subTest(direction=direction):
                at = self.analyse(line, direction, positions, ball)
                below = self.analyse(line - (0.01 if direction == "right" else -0.01), direction, positions, ball)
                self.assertEqual(at['fraction_beyond_defender'], 0.5)
                self.assertTrue(at['in_offside_position'])
                self.assertFalse(below['in_offside_position'])

    def test_halfway_front_edge(self):
        self.assertFalse(self.analyse(49, defenders=[20, 30, 40, 45])['in_opponent_half'])
        self.assertTrue(self.analyse(49.5, defenders=[20, 30, 40, 45])['in_opponent_half'])

    def test_ball_front_edge_and_equality(self):
        self.assertFalse(self.analyse(60, ball=61)['ahead_of_ball'])
        self.assertTrue(self.analyse(60, ball=60.5)['ahead_of_ball'])

    def test_offence_requires_involvement(self):
        args = (60, 2, [30, 45, 48, 52], 40, "right")
        self.assertFalse(check_offside_offence(*args))
        self.assertTrue(check_offside_offence(*args, touched_ball=True))
        self.assertTrue(check_offside_offence(*args, interfered_with_opponent=True))
        self.assertTrue(check_offside_offence(*args, gained_advantage=True))
        for restart in ("goal_kick", "throw_in", "corner_kick"):
            self.assertFalse(check_offside_offence(*args, restart_type=restart, touched_ball=True))

    def test_all_attackers(self):
        result = check_all_attackers({'Trevor': 48, 'Amir': 60}, 2, [30, 45, 48, 52], 40, 'right', involved_players=('Amir',))
        self.assertEqual(result, {'Trevor': False, 'Amir': True})

    def test_bad_inputs(self):
        with self.assertRaises(ValueError): self.analyse(60, 'up')
        with self.assertRaises(ValueError): self.analyse(60, defenders=[48])
        with self.assertRaises(ValueError): analyse_position(60, 0, [40, 48], 40, 'right')
        with self.assertRaises(ValueError): self.analyse(float('nan'))
        with self.assertRaises(ValueError): check_offside_offence(60, 2, [40, 48], 40, 'right', restart_type='freekick')


if __name__ == '__main__':
    unittest.main()
