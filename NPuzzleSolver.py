import math
from copy import deepcopy

from dataclasses import dataclass
from typing import Any, Tuple


@dataclass
class Node:
    tiles: list
    g_score: int
    heuristic_score: int
    f_score: int
    direction: Any
    parent: Any


class NPuzzleSolver:
    def __init__(self, number_of_tiles: int, tiles: list):
        self.shape = int(math.sqrt(number_of_tiles + 1))
        self.current_state = Node(tiles=tiles,
                                  g_score=0,
                                  heuristic_score=self.heuristic_function(tiles),
                                  f_score=0 + self.heuristic_function(tiles),
                                  direction="start",
                                  parent=None)
        self.goal = self.set_goal(self.shape)
        self.open_set = [self.current_state]
        self.close_set = []

    def print_path(self) -> None:
        tmp_state = self.current_state
        answer_state = []
        while tmp_state is not None:
            answer_state.append([tmp_state.tiles, tmp_state.f_score, tmp_state.direction])
            tmp_state = tmp_state.parent
        answer_state.reverse()
        for i, answer in enumerate(answer_state):
            print(f"\t\tstep is {i}")
            print(f"\t\tf_score is :{answer[1]} \n\t\tdirection is :{answer[2]}\n")
            self.print_tile(answer[0])
            print("****************************************************\n")

    def print_tile(self, tiles):
        for i in range(self.shape):
            for j in range(self.shape):
                print("\t", tiles[i][j], end="\t")
            print("\n")
        print("\n")

    def heuristic_function(self, tiles: list) -> int:
        value = 0
        for i in range(self.shape):
            for j in range(self.shape):
                if tiles[i][j] != "_":
                    x, y = self.get_indexes_from_value(tiles[i][j])
                    value += abs(i - x) + abs(j - y)
        return value

    @staticmethod
    def update_g_score(tiles: list, new_g_score: int, list_of_nodes: list) -> bool:
        for node in list_of_nodes:
            if node.tiles == tiles:
                if new_g_score < node.g_score:
                    node.g_score = new_g_score
                    return True
                return False

    def get_indexes_from_value(self, value: int) -> Tuple[int, int]:
        return math.ceil(value / self.shape) - 1, value - self.shape*(math.ceil(value / self.shape) - 1) - 1

    def create_children(self, node: Node) -> None:
        x, y = self.find_blank(node.tiles)
        if x - 1 >= 0:
            self.create_child(node, "Up")
        if x + 1 < self.shape:
            self.create_child(node, "Down")
        if y - 1 >= 0:
            self.create_child(node, "Left")
        if y + 1 < self.shape:
            self.create_child(node, "Right")

    def find_blank(self, tiles: list) -> Tuple[int, int]:
        for i in range(self.shape):
            for j in range(self.shape):
                if tiles[i][j] == "_":
                    return i, j

    def create_child(self, node: Node, direction):
        x, y = self.find_blank(node.tiles)
        if direction == "Left":
            new_tiles = self.exchange_tiles(node.tiles, x, y, x, y - 1)
        elif direction == "Right":
            new_tiles = self.exchange_tiles(node.tiles, x, y, x, y + 1)
        elif direction == "Up":
            new_tiles = self.exchange_tiles(node.tiles, x, y, x - 1, y)
        else:
            new_tiles = self.exchange_tiles(node.tiles, x, y, x + 1, y)
        # if self.is_goal(new_tiles, self.goal):
        #     print("wooooow")
        if self.in_set(new_tiles, self.open_set):
            self.update_g_score(new_tiles,
                                node.g_score + 1,
                                self.open_set)
        elif self.in_set(new_tiles, self.close_set):
            if self.update_g_score(new_tiles,
                                   node.g_score + 1,
                                   self.close_set):
                self.closed_to_open_list(new_tiles)
        else:
            self.open_set.append(Node(tiles=new_tiles,
                                      g_score=node.g_score + 1,
                                      heuristic_score=self.heuristic_function(new_tiles),
                                      f_score=node.g_score + 1 + self.heuristic_function(new_tiles),
                                      direction=direction,
                                      parent=node))

    def closed_to_open_list(self, tiles: list) -> None:
        for node in self.close_set:
            if node.tiles == tiles:
                self.close_set.remove(node)
                self.open_set.append(node)

    @staticmethod
    def is_goal(tiles: list, goal: list) -> bool:
        if tiles == goal:
            return True
        return False

    @staticmethod
    def in_set(tiles: list, list_of_nodes: list) -> bool:
        if list_of_nodes:
            for node in list_of_nodes:
                if node.tiles == tiles:
                    return True
            else:
                return False

    @staticmethod
    def exchange_tiles(tiles: list, x0: int, y0: int, x1: int, y1: int) -> list:
        tiles_copy = deepcopy(tiles)
        tmp = tiles_copy[x0][y0]
        tiles_copy[x0][y0] = tiles_copy[x1][y1]
        tiles_copy[x1][y1] = tmp
        return tiles_copy

    @staticmethod
    def set_goal(shape: int) -> list:
        goal = [list(range(1 + shape * i, 1 + shape * (i + 1)))
                for i in range(shape)]
        goal[shape - 1][shape - 1] = "_"
        return goal

    def get_minimum_f_score_node(self):
        self.open_set = sorted(self.open_set, key=lambda x: x.f_score)
        return self.open_set[0]

    def a_star_algorithm(self):
        while self.open_set:
            self.current_state = self.get_minimum_f_score_node()
            if self.is_goal(self.current_state.tiles, self.goal):
                self.print_path()
                break
            else:
                self.create_children(self.current_state)
            self.open_set.remove(self.current_state)
            self.close_set.append(self.current_state)
