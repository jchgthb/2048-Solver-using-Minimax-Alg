#Joshua Cheeran jjc2299

import sys
import math
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
     def __init__(self):
        self.Depth = 6

     def getMove(self, grid):
        return self.minimax(grid, 0, -sys.maxsize - 1, sys.maxsize, True)[0]

     def minimax(self, grid, depth, alpha, beta, is_maximizing):
        if depth == self.Depth:
            return (None, self.heuristic(grid))

        if is_maximizing:
            best_value = -sys.maxsize - 1
            best_move = None
            for move in grid.getAvailableMoves():
                new_grid = grid.clone()
                new_grid.move(move[0])
                value = self.minimax(new_grid, depth + 1, alpha, beta, False)[1]
                if value > best_value:
                    best_value = value
                    best_move = move[0]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_move, best_value
        else:  # Minimizing player
            if depth == self.Depth - 1:
                return (None, self.heuristic(grid))
            best_value = sys.maxsize
            for pos in grid.getAvailableCells()[:3]:
                for value in [2, 4]:
                    new_grid = grid.clone()
                    new_grid.insertTile(pos, value)
                    result = self.minimax(new_grid, depth + 1, alpha, beta, True)[1]
                    if value == 2:
                        result *= 0.9
                    else:  # value == 4
                        result *= 0.1
                    best_value = min(best_value, result)
                    beta = min(beta, best_value)
                    if alpha >= beta:
                        break
            return (None, best_value)
    
     def heuristic(self, grid):
        empty = len(grid.getAvailableCells())
        smoothness, monotonicity = self.calculateSmoothnessAndMonotonicity(grid)
        cluster = self.calculateCluster(grid)
        merges = self.countPossibleMerges(grid)
        max_tile = grid.getMaxTile()
        tile_position = max_tile in (grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3])

        weights = {
            'empty': 3.5,
            'smoothness': 0.8,
            'monotonicity': 2.4,
            'max_tile_position': 6.5 * (1 if tile_position else 0),
            'tile_position': 9.3 * (1 if tile_position else 0),
            'cluster': -1.9,
            'merges': 1.8
        }

        return (
            weights['empty'] * empty +
            weights['smoothness'] * smoothness +
            weights['monotonicity'] * monotonicity +
            weights['max_tile_position'] +
            weights['tile_position'] +
            weights['cluster'] * cluster +
            weights['merges'] * merges
        )

     def calculateSmoothnessAndMonotonicity(self, grid):
        smoothness = 0
        monotonicity = 0
        for x in range(grid.size):
            for y in range(grid.size - 1):
                current_value = math.log(grid.map[x][y], 2) if grid.map[x][y] else 0
                right_value = math.log(grid.map[x][y + 1], 2) if grid.map[x][y + 1] else 0
                down_value = math.log(grid.map[x + 1][y], 2) if x + 1 < grid.size and grid.map[x + 1][y] else 0

                if grid.map[x][y] and grid.map[x][y] == grid.map[x][y + 1]:
                    smoothness += 1
                if grid.map[x][y] and x + 1 < grid.size and grid.map[x][y] == grid.map[x + 1][y]:
                    smoothness += 1

                monotonicity -= abs(current_value - right_value) + abs(current_value - down_value)

        return smoothness, monotonicity
    
     def countPossibleMerges(self, grid):
        merges = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] != 0:
                    for d in [(1, 0), (0, 1)]: 
                        nx, ny = x + d[0], y + d[1]
                        if nx < grid.size and ny < grid.size:
                            if grid.map[x][y] == grid.map[nx][ny]:
                                merges += 1
                                break  
        return merges

     def calculateCluster(self, grid):  
        cluster = 0
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        
        for x in range(grid.size):  # Use grid.size
            for y in range(grid.size):  # Use grid.size
                if grid.map[x][y] == 0:
                    continue  # Skip empties
                tile_value_log = math.log(grid.map[x][y], 2) if grid.map[x][y] != 0 else 0
                # Compare  tile with neighbors
                sum_diff = 0
                num_neighbors = 0
                for dx, dy in neighbors:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid.size and 0 <= ny < grid.size and grid.map[nx][ny] > 0:
                        neighbor_value_log = math.log(grid.map[nx][ny], 2)
                        sum_diff += abs(tile_value_log - neighbor_value_log)
                        num_neighbors += 1
                # Average difference with neighbors
                if num_neighbors > 0:
                    cluster += sum_diff / num_neighbors
        
        return cluster
    
