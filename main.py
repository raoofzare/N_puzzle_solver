from NPuzzleSolver import NPuzzleSolver

if __name__ == "__main__":
    number_of_tiles = int(input())
    tiles = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, "_", 15]]
    n_puzzle = NPuzzleSolver(number_of_tiles, tiles)
    n_puzzle.a_star_algorithm()
