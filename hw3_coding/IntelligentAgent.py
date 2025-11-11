import math
import random
import time
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        depth = self.getAdaptiveDepth(grid)
        return self.bestMove(grid,depth)
        

    def is_over(self, grid):
        if not grid.canMove():
            return True
        return False
    
    def bestMove(self, grid, maxDepth):
        move = None
        best_move = None
        for depth in range(1, maxDepth + 1):
            score, move= self.expectiminimax_w_ab(grid, 0,depth,  float('-inf'), float('inf'), True)
            if move is not None:
                best_move = move
        return best_move

    def expectiminimax_w_ab(self, grid, depth, maxDepth, alpha=float('-inf'), beta=float('inf'),is_max = True):
        move = None 
        if self.is_over(grid) or depth == maxDepth:
            return self.evaluate(grid), None
        if is_max:
            max_score = float('-inf')
            best_move = None
            moves = grid.getAvailableMoves()
            for move, new_grid in moves:
                score, _ = self.expectiminimax_w_ab(new_grid, depth + 1, maxDepth ,alpha, beta, False)
                if score > max_score:
                    max_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    #prune branches
                    break
            return max_score, best_move
        else: 
            empty = grid.getAvailableCells()
            if not empty:
                return self.evaluate(grid), None
            expected_score = 0
            for cell in empty:
                 for value, probability in [(4,0.1), (2,0.9)]:
                     new_grid = grid.clone()
                     new_grid.setCellValue(cell, value)
                     score, _ = self.expectiminimax_w_ab(new_grid, depth + 1, maxDepth, alpha, beta, True)
                     expected_score += probability * score / len(empty)
            return expected_score, move

                    

    def evaluate(self, grid):
        max_tile = grid.getMaxTile()
        if max_tile < 512:
            lowTileWeight = 3
            fourRowWeight = 0
        else:
            lowTileWeight = 0.5
            fourRowWeight = 0.8

    
        return (
        3 * len(grid.getAvailableCells())
        + 2 * self.smoothness(grid) / max_tile #-2500 per
        + 2.5* self.corners(grid) / max_tile
        + 80 * self.monotonicity(grid) / max_tile
        + 3 * self.mergeChainPotential(grid)
        + 3 * self.adjacencyScore(grid)
        + fourRowWeight * self.fourRowPenalty(grid)
        + 2 * self.smallOnTopPenalty(grid)
        + 6 * self.stairCase(grid)
        + 2 * self.blockingTileBonus(grid)
        + lowTileWeight * self.lowTileMergePotential(grid)
        - 3 * self.downPenalty(grid)
        - 0.8 * self.rightPenalty(grid)
    )

    def similarTileAdjacency(self, grid):
        score = 0
        for i in range(grid.size):
            for j in range(grid.size):
                tile = grid.getCellValue((i, j))
                if tile == 0:
                 continue
            
                for dx, dy in [(0, 1), (1, 0)]:
                    ni, nj = i + dx, j + dy
                    if ni < grid.size and nj < grid.size:
                        neighbor = grid.getCellValue((ni, nj))
                        if neighbor == 0:
                         continue
                    
                        diff = abs(tile - neighbor)
                    
                        if diff == 0:
                            score += tile * 2 
                        else:
                            score += max(0, tile - diff / 2)  
        return score

    def smoothness(self, grid):
        score = 0
        for x in range(grid.size):
            for y in range(grid.size):
                value = grid.getCellValue((x,y))
                if value == 0:
                    continue
                for dx,dy in [(0,1), (1,0)]:
                    neighbor = grid.getCellValue((x+dx, y+dy))
                    if neighbor:
                        score -= abs(value - neighbor)
        return score


    def getAdaptiveDepth(self, grid):
        empty_cells = len(grid.getAvailableCells())
    
        if empty_cells <= 2 and grid.getMaxTile() >= 2048:
            return 4
        else:
            return 3
        


    def corners(self, grid):
        return max([
        grid.getCellValue((0, 0)),
        grid.getCellValue((0, 3)),
        grid.getCellValue((3, 0)),
        grid.getCellValue((3, 3))
        ])
    
    def monotonicity(self, grid):
        totals = [0,0,0,0]

        for row in grid.map:
            for i in range(len(row)-1):
                if row[i] > row[i+1]:
                    totals[0] += row[i] - row[i+1]
                else:
                    totals[1] += row[i+1] - row[i]

        for j in range(grid.size):
            for i in range(grid.size-1):
                a = grid.map[i][j]
                b = grid.map[i+1][j]
                if a > b:
                    totals[2] += a - b
                else:
                    totals[3] += b - a

        return -min(totals)

    def mergePotential(self, grid):
        potential = 0
        for i in range(grid.size):
            for j in range(grid.size):
                value = grid.getCellValue((i,j))
                if value == 0:
                    continue
                if j < grid.size -1 and grid.getCellValue((i,j+1)) == value:
                    potential += 1
                if i < grid.size -1 and grid.getCellValue((i+1, j)) == value:
                    potential += 1

        return potential
    
    def mergeChainPotential(self, grid):
        potential = 0
        for i in range(grid.size):
            row = [grid.getCellValue((i,j)) for j in range(grid.size)]
            col = [grid.getCellValue((j,i)) for j in range(grid.size)]
            for j in range(grid.size-2):
                if row[j] == row[j+1] and row[j]*2 == row[j+2]:
                    potential += 2
                if col[j] == col[j+1] and col[j]*2 == col[j+2]:
                    potential += 2
        return potential
        

    weights = [
    [65536, 32768, 16384, 8192],
    [4096, 2048, 1024, 512],
    [256, 128, 64, 32],
    [16, 8, 4, 2]
]


    
    
    def cornerPenalty(self, grid):
        maxTile = grid.getMaxTile()
        if grid.getCellValue((0,0)) != maxTile:
            return -1
        return 0

    def adjacencyScore(self, grid):
        size = grid.size
        
        max_tile = 0
        max_pos = (0, 0)
        for i in range(size):
            for j in range(size):
                val = grid.getCellValue((i, j))
                if val > max_tile:
                    max_tile = val
                    max_pos = (i, j)

    
        second_max = 0
        second_pos = (0, 0)
        for i in range(size):
            for j in range(size):
                val = grid.getCellValue((i, j))
                if val > second_max and val < max_tile:
                    second_max = val
                    second_pos = (i, j)

    
        score = 0
        if max_pos[0] == second_pos[0] and abs(max_pos[1] - second_pos[1]) == 1:
            score += second_max / 10  
        if max_pos[1] == second_pos[1] and abs(max_pos[0] - second_pos[0]) == 1:
            score += second_max / 10

        return score

    def downPenalty(self, grid):
        penalty = 0
        for j in range(grid.size):
            for i in range(1, grid.size):
                upper = grid.getCellValue((i - 1, j))
                lower = grid.getCellValue((i, j))
                if lower > upper and upper != 0:
                    penalty += (lower - upper) / 2
        return penalty

    def rightPenalty(self, grid):
        penalty = 0
        for j in range(grid.size):
            for i in range(1, grid.size):
                upper = grid.getCellValue((i - 1, j))
                lower = grid.getCellValue((i, j))
                if lower > upper and upper != 0:
                    penalty += (lower - upper) / 2
        return penalty

    def fourRowPenalty(self, grid):
        penalty = 0
        for i in range(grid.size):
            row_values = [grid.getCellValue((i, j)) for j in range(grid.size)]
            non_zero_tiles = [v for v in row_values if v != 0]

            if len(non_zero_tiles) == 4:
                penalty -= 1 

        return penalty
    
    def stairCase(self, grid):
        score = 0
        for i in range(grid.size):
            for j in range(grid.size):
                tile = grid.getCellValue((i, j))
                score += tile * self.weights[i][j]
        return score / 50000 
    
    def smallOnTopPenalty(self, grid):
        penalty = 0
        for i in range(grid.size - 1):  # skip last row
            for j in range(grid.size):
                current = grid.getCellValue((i, j))
                below = grid.getCellValue((i + 1, j))
                if current != 0 and below != 0 and current < below:
                    penalty -= (below - current) / 8  # scale penalty
        return penalty

    def blockingTileBonus(self, grid):
        bonus = 0
        for i in range(grid.size):
            for j in range(grid.size):
                tile = grid.getCellValue((i,j))
                if tile == 0:
                    continue

         
            if i < grid.size - 1:
                below = grid.getCellValue((i+1,j))
                if below != 0 and below != tile:
                    bonus += tile * 0.5
                elif below == tile:
                    bonus += tile * 0.2  

           
            if j < grid.size - 1:
                right = grid.getCellValue((i,j+1))
                if right != 0 and right != tile:
                    bonus += tile * 0.5
                elif right == tile:
                    bonus += tile * 0.2
        return bonus

    
    def lowTileMergePotential(self, grid):
    
        bonus = 0
        for i in range(grid.size):
            for j in range(grid.size):
                tile = grid.getCellValue((i, j))
                if tile in [2, 4, 8]:
                
                    if j < grid.size - 1 and grid.getCellValue((i, j + 1)) == tile:
                        bonus += tile * 1.0
               
                    if i < grid.size - 1 and grid.getCellValue((i + 1, j)) == tile:
                        bonus += tile * 1.0
        return bonus
  