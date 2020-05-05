# maze_solver
import copy
import sys
#import random_maze



class MazeSolver:
    START = 'A'
    END = 'B'
    WALL = 'X'
    OPEN = ' '
    DEAD_END = 'W'
    VISITED = 'O'

    def __init__(self, maze):
        self.maze = maze
        for row_index, row in enumerate(maze):
            for column_index, value in enumerate(row):
                if value == self.START:
                    self.start = {'X': row_index, 'Y': column_index}
        self.solved = False
        self.shortest_path = sys.maxsize
        self.shortest_maze = maze
        self.shortest_trail = ""

    def print(self, new_maze):
        for row in new_maze:
            print(row)

    def copy(self, new_maze):
        new_copy = []
        for row_index, row in enumerate(new_maze):
            new_row =[]
            for column_index, value in enumerate(row):
                new_row.append(copy.deepcopy( new_maze[row_index][column_index]))
            new_copy.append(new_row)

        return new_copy


    def _is_position_within_maze_and_open(self, row_index, column_index, new_maze):
        return 0 <= row_index < len(new_maze) \
               and 0 <= column_index < len(new_maze[row_index]) \
               and (new_maze[row_index][column_index] == self.OPEN
                    or new_maze[row_index][column_index] == self.END)

    def _solve(self, row_index, column_index, path, new_maze, trail):

        if self.maze[row_index][column_index] == self.END:
            print("**************************")
            self.print(new_maze)
            if path < self.shortest_path:
                self.shortest_path = path
                self.shortest_maze = self.copy(new_maze)
                self.shortest_trail = trail
            return

        new_maze[row_index][column_index] = self.VISITED

        # east
        if self._is_position_within_maze_and_open(row_index, column_index + 1, new_maze):
            self._solve(row_index, column_index + 1, path+1, self.copy(new_maze) , trail+"E")

        # north
        if self._is_position_within_maze_and_open(row_index - 1, column_index, new_maze):
            self._solve(row_index - 1, column_index, path+1, self.copy(new_maze) , trail+"N")


        # west
        if self._is_position_within_maze_and_open(row_index, column_index - 1, new_maze):
            self._solve(row_index, column_index - 1, path+1, self.copy(new_maze), trail+"W")


        # south
        if self._is_position_within_maze_and_open(row_index + 1, column_index, new_maze):
            self._solve(row_index + 1, column_index, path+1, self.copy(new_maze), trail+"S")


    def solve(self):
        self._solve(self.start['X'], self.start['Y'], 0, self.copy(self.maze), "")
        if self.shortest_path > 0:
            print("---------------------------")
            print("---------------------------")
            self.print(self.shortest_maze)
            print("The trail is :" + self.shortest_trail)
            print("The shortest path is:" + str(self.shortest_path))
            self.solved = True
            return self.shortest_trail