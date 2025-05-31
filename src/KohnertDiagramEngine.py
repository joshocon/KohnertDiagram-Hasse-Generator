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
        cells_set = set(cells)
        for i in range(len()):
            for j in range(i + 1, len(cells)):
                if (
                    min(cells[i][0], cells[j][0]),
                    max(cells[i][1], cells[j][1]),
                ) not in cells_set:
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
                    moveable.append([cell, (r,col)])
                    break  # once we know an open spot exists, break - moveable contains lists in the form [cell_to_be_moved, new_cell_position]
        return moveable
        
    def kohnert_move(self, graph, diagram, move_pair, cache=None):
            if cache is None:
                cache = {}
                
            cell = move_pair[0]
            new_cell = move_pair[1]

            # initialize new_diagram and set its cells = cells in initial diagram parameter
            new_cells = copy.copy(diagram.cells)
            new_diagram = Diagram(new_cells, diagram.row_num, diagram.col_num)
            new_diagram.cells.remove(cell)  # remove the cell we are going to move

            target_row, col = new_cell
            
            new_diagram.cells.append((target_row, col))

            key = frozenset(new_diagram.cells)
            # if new diagram cells is in the cache, grab it and set it as a child of the initial diagram
            if key in cache:
                existing = cache[key]
                graph.add_edge(diagram, existing)
                graph.add_vertex(existing)
            else:
                # else, set the parent of the new_diagram to the initial diagram, add it to the child list, and add it to the cache.
                graph.add_edge(diagram, new_diagram)
                cache[key] = new_diagram
                graph.add_vertex(new_diagram)
                # find move eligible cells for the new diagram, and recurse
                new_move_cells = self.find_move_cells(new_diagram)
                for new_move_pair in new_move_cells:
                    self.kohnert_move(graph, new_diagram, new_move_pair, cache)

