# in some complex situations it takes some time because
# of a lot of nodes in a tree but must generates solution

import random
import copy  # for making deepcopy of the current puzzle
from queue import PriorityQueue


class PuzzleNode:
    def __init__(self, data):
        self.g_score = 0  # same as depth level
        self.data = data
        self.heuristic = 0
        self.f_score = 0
        self.parent = None

    # this function display the Node/puzzle
    def print_node(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print(self.data[i][j], end="   ")
            print('\n')

    # find the position of 0 in puzzle
    def find_blank(self):
        for index, value in enumerate(self.data):
            if 0 in value:
                return index, value.index(0)

    # find the possible moves of blank or 0
    def get_possible_moves(self):
        x, y = self.find_blank()
        left = (x, y - 1) if y - 1 >= 0 else None
        right = (x, y + 1) if y + 1 <= 2 else None
        top = (x - 1, y) if x - 1 >= 0 else None
        bottom = (x + 1, y) if x + 1 <= 2 else None
        moves = [left, right, top, bottom]
        # removing none from moves
        return [m for m in moves if m is not None]

    # it returns the list of nearest neighbors
    def get_neighbors(self):
        moves = self.get_possible_moves()
        neighbors = list()
        blank_x, blank_y = self.find_blank()
        for move in moves:
            x, y = move
            temp_puzzle = PuzzleNode(copy.deepcopy(self.data))  # new node so that handle changes

            # swapping the indexes
            temp_puzzle.data[x][y], temp_puzzle.data[blank_x][blank_y] = temp_puzzle.data[blank_x][blank_y], \
                                                                         temp_puzzle.data[x][y]

            temp_puzzle.g_score = self.g_score + 1  # increasing the depth of child
            neighbors.append(temp_puzzle)

        return neighbors

    # to make class objects comparable for priority queue
    def __lt__(self, other):
        return self.f_score < other.f_score


class EightPuzzle:
    def __init__(self):
        self._path_cost = 0
        self._goal = PuzzleNode(data=[[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self._initial_puzzle = PuzzleNode(self.generate_initial_puzzle())

        self._initial_puzzle.f_score = self.heuristic_tiles_misplaced(
            self._initial_puzzle) + self._initial_puzzle.g_score

    # it generate the random initial puzzle
    def generate_initial_puzzle(self):
        choices = list(range(9))
        random.shuffle(choices)  # shuffle the choices list
        # converting the list into 2d list of 3x3
        return [choices[i:i + 3] for i in range(0, len(choices), 3)]

    # number of tiles miss placed
    def heuristic_tiles_misplaced(self, puzzle):
        miss_placed = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if puzzle.data[i][j] != 0:
                    if puzzle.data[i][j] != self._goal.data[i][j]:
                        miss_placed += 1
        return miss_placed

    # a* algorithm to find the solution
    def find_solution(self):

        print("Initial puzzle")
        self._initial_puzzle.print_node()
        print("Goal State")
        self._goal.print_node()
        print("Solving...")

        count = 0  # to store number of steps

        open_list = PriorityQueue()
        close_list = list()

        # putting the initial node/puzzle in open list
        open_list.put((self._initial_puzzle.f_score, self._initial_puzzle))

        while True:
            count += 1

            if open_list.empty():
                return

            current_puzzle = open_list.get()[1]  # getting the item from priority queue

            if current_puzzle.data == self._goal.data:  # checking if it is goal state
                path = list()
                while current_puzzle.parent:  # storing a path in path variable
                    path.append(current_puzzle)
                    current_puzzle = current_puzzle.parent
                path.append(current_puzzle)
                path = path[::-1]  # reversing the path to get the path from start to end
                self.show_path(path, count)
                return

            if current_puzzle.data not in close_list:  # if it is not explored yet
                close_list.append(current_puzzle.data)  # if not explored put it in the close list and start exploring
                for neighbor in current_puzzle.get_neighbors():
                    neighbor.heuristic = self.heuristic_tiles_misplaced(neighbor)
                    neighbor.f_score = neighbor.heuristic + neighbor.g_score
                    neighbor.parent = current_puzzle # setting neighbor parent
                    open_list.put((neighbor.f_score, neighbor)) # putting neighbors in the open list priority queue

    def show_path(self, path, steps):
        print(f"Number of steps taken : {steps}")
        print("Steps of solving puzzle")
        for node in path:
            for i in range(0, 3):
                for j in range(0, 3):
                    print(node.data[i][j], end=" ")
                print(" ")
            if path.index(node) != len(path) - 1:
                print('  ↓')
        return


puzzle_obj = EightPuzzle()
puzzle_obj.find_solution()
