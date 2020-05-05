# test_maze

from unittest import TestCase
from maze_solver.maze import MazeSolver


class TestMazeSolver(TestCase):


    def test_solve(self):
        test_maze = [
            ['A', 'X', ' ', ' ', ' '],
            [' ', 'X', ' ', 'X', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', 'X', ' ', 'X', ' '],
            [' ', 'X', ' ', 'X', 'B'],
        ]

        maze_solver = MazeSolver(test_maze)
        self.assertEqual(maze_solver.solve(), "SSEEEESS")