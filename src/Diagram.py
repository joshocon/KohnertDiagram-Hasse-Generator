'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

import hashlib

class Diagram:
    def __init__(self, cells, row_num, col_num):
        self.cells = cells
        self.row_num = row_num
        self.col_num = col_num
        self.key = None
        self.row_weight = self.get_row_weight()

    # gives diagram a unique key
    def generate_diagram_key(self, cells):
        sorted_cells = sorted(cells)
        cell_str = str(sorted_cells)
        return hashlib.md5(cell_str.encode()).hexdigest()

    def get_row_weight(self):
        weight = {}
        for r,c in self.cells:
            r = int(r)  # Ensure r is int
            weight[r] = weight.get(r, 0) + 1

        max_row = max(weight.keys(), default=0)
        row_weight = [weight.get(r, 0) for r in range(1, max_row + 1)]
        
        return row_weight

    def get_row_number(self):
        return self.row_num

    def get_col_number(self):
        return self.col_num
    
    def __eq__(self, other):
        return isinstance(other, Diagram) and set(self.cells) == set(other.cells)

    def __hash__(self):
        return hash(frozenset(self.cells))

    def __repr__(self):
        return f'{self.cells}'
    
    

