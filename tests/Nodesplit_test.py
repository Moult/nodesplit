import unittest
import nodesplit.nodesplit as nodesplit
from math import pi

class EngineTest(unittest.TestCase):

    def setUp(self):
        # This is a 1 unit cube, with two slots filled up
        self.world = [
            [0, 0, 0, True],
            [1, 0, 0, False],
            [0, 1, 0, False],
            [1, 1, 0, False],
            [0, 0, 1, False],
            [1, 0, 1, False],
            [0, 1, 1, False],
            [1, 1, 1, True],
        ]

        # Lines formed by the edges of the box
        self.boxlines = [
            [[0,0,0], [1,0,0], True],
            [[1,0,0], [1,1,0], True],
            [[1,1,0], [0,1,0], True],
            [[0,1,0], [0,0,0], True],
            [[0,0,1], [1,0,1], True],
            [[1,0,1], [1,1,1], True],
            [[1,1,1], [0,1,1], True],
            [[0,1,1], [0,0,1], True],
            [[0,0,0], [0,0,1], True],
            [[1,0,0], [1,0,1], True],
            [[1,1,0], [1,1,1], True],
            [[0,1,0], [0,1,1], True],
        ]

        # A single unkinked line, attached from those two corners
        self.lines = list(self.boxlines)
        self.lines.append(
            [[0,0,0], [1,1,1], False]
        )

        self.sus = nodesplit.Engine(self.world, self.lines)
        self.assertEqual(self.sus.world, self.world)
        self.assertEqual(self.sus.lines, self.lines)

    def test_pick_line_to_operate_on(self):
        self.sus.pick_operation_line()
        self.assertEqual(self.sus.operation_line, [[0,0,0], [1,1,1],False])

    def test_get_midpoint_of_line(self):
        self.assertEqual(
            self.sus.get_midpoint([0,0,0], [1,1,1]),
            [0.5, 0.5, 0.5]
        )

    def test_get_free_slot(self):
        world = [
            [0, 0, 0, True],
            [1, 0, 0, False],
        ]
        self.sus = nodesplit.Engine(world, self.lines)
        self.assertEqual(self.sus.get_free_slot(), [1, 0, 0])
        self.assertNotEqual(self.sus.used_slots, [])

    def test_get_kink(self):
        self.assertEqual(
            self.sus.get_kink([0, 0, 0], [0, 1, 0], [1, 0.5, 0]),
            [self.sus.kink_factor, 0.5, 0]
        )

    def test_get_distance(self):
        self.assertEqual(self.sus.get_distance([0, 0, 0], [1, 0, 0,]), 1)

    def test_get_stabiliser_slot(self):
        self.sus.get_stabiliser_slot([0, 0, 0], [1, 0, 0])

    def test_get_vector(self):
        self.assertEqual(
            self.sus.get_vector([0, 0, 0], [1, 0, 0]),
            [1, 0, 0]
        )

    def test_angle(self):
        self.assertEqual(
            self.sus.angle([1, 0, 0], [0, 1, 0]),
            pi / 2
        )

    def test_execute(self):
        self.sus.execute()

    def test_mark_used_slots(self):
        world = [
            [0, 0, 0, True],
            [1, 0, 0, False],
        ]
        used_world = [
            [0, 0, 0, True],
            [1, 0, 0, True],
        ]
        self.sus = nodesplit.Engine(world, self.lines)
        self.sus.get_free_slot()
        self.sus.mark_used_slots()
        for slot in world:
            self.assertEqual(slot[3], True)

    def test_update_lines(self):
        self.sus.pick_operation_line()
        self.sus.update_lines(
            [0, 0, 0], # Not a real kink
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 1],
        )
