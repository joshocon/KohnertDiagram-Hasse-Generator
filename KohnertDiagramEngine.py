'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

import copy
from Diagram import Diagram

class KohnertDiagramEngine:
    
    def get_dimension(self, cells):
        row_num = 0
        col_num = 0
        for cell in cells:
            if row_num < cell[0]:
                row_num = cell[0]
            if col_num < cell[1]:
                col_num = cell[1]
        return [row_num, col_num]

    def check_south_east(self, cells):
            for i in range(len(cells)):
                for j in range(len(cells)):
                    if i != j:
                        if (
                            min(cells[i][0], cells[j][0]),
                            max(cells[i][1], cells[j][1]),
                        ) not in cells:
                            return False
            return True

    def find_move_cells(self, D):
            diagram = D
            cells = set(diagram.cells)
            max_cells = {}

            # build dictionary whose key is the row and value is the furthest right cell in that row
            for row, col in cells:
                if row not in max_cells or col > max_cells[row][1]:
                    max_cells[row] = (row, col)

            moveable = []
            # for the furthest right cell in each row, is it moveable? meaning is there an empty space beneath it in its column
            # checks each from starting at r-1 to 0 for an empty space
            for cell in max_cells.values():
                row, col = cell

                for r in range(row - 1, 0, -1):
                    if (r, col) not in cells:
                        moveable.append(cell)
                        break  # once we know an open spot exists, break
            return moveable
        
    def kohnert_move(self, graph, diagram, cell, cache=None):
            if cache is None:
                cache = {}

            # initialize new_diagram and set its cells = cells in initial diagram parameter
            new_cells = copy.copy(diagram.cells)
            new_diagram = Diagram(new_cells, diagram.row_num, diagram.col_num)
            new_diagram.cells.remove(cell)  # remove the cell we are going to move

            row, col = cell
            target_row = None
            # we find the first open spot in the same way we did in the find_move_cells method
            for r in range(row - 1, 0, -1):
                if (r, col) not in diagram.cells:
                    target_row = r
                    break
            # failsafe
            if target_row is None:
                return

            # append new cell
            new_diagram.cells.append((target_row, col))

            key = frozenset(new_diagram.cells)
            # if new diagram cells is in the cache, grab it and set it as a child of the initial diagram
            if key in cache:
                existing = cache[key]
                graph.add_edge(diagram, existing)
            else:
                # else, set the parent of the new_diagram to the initial diagram, add it to the child list, and add it to the cache.
                graph.add_edge(diagram, new_diagram)
                cache[key] = new_diagram
                # find move eligible cells for the new diagram, and recurse
                move_cells = self.find_move_cells(new_diagram)
                for next_cell in move_cells:
                    self.kohnert_move(graph, new_diagram, next_cell, cache)