'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

import hashlib

class Diagram:
    def __init__(self, cells, row_num, col_num):
        self.cells = cells
        self.zero_index = [(r-1,c-1) for (r,c) in self.cells]
        self.row_num = row_num
        self.col_num = col_num
        self.key = None
        self.row_weight = ''
        self.column_weight = self.get_column_weight()
        self.monomial = ''

    # gives diagram a unique key
    def generate_diagram_key(self, cells):
        sorted_cells = sorted(cells)
        cell_str = str(sorted_cells)
        return hashlib.md5(cell_str.encode()).hexdigest()

    def get_row_weight(self):
        weight = {}
        if self.cells != []:
            for r,c in self.cells:
                r = int(r)  # Ensure r is int
                weight[r] = weight.get(r, 0) + 1

            max_row = max(weight.keys(), default=0)
            row_weight = [weight.get(r, 0) for r in range(1, max_row + 1)]
        
        return row_weight
    
    def get_column_weight(self):
        weight = {}
        if self.cells != []:
            for r, c in self.cells:
                c = int(c)  # Ensure c is int
                weight[c] = weight.get(c, 0) + 1

            max_col = max(weight.keys(), default=0)
            column_weight = [weight.get(c, 0) for c in range(1, max_col + 1)]
        
        return column_weight

    
    def get_monomial(self):
        monomial = ''
        for i in range(len(self.row_weight)):
            if self.row_weight[i] != 0:
                if self.row_weight[i] == 1:
                    monomial += f'x_{i+1}'
                else:
                    monomial += f'x_{i+1}^{self.row_weight[i]}'
        return monomial
    
    
    def test_conjecture(self):
        good_trios = self.condition_a_and_b()
        failed = []

        if len(self.cells) == 1:
            return failed.append('Trival')

        for trio in good_trios:
            if not self.condition_c(trio):
                failed.append('C')
                continue
            if not self.condition_d(trio):
                failed.append('D')
                continue
            if not self.condition_e(trio):
                failed.append('E')
                continue
            if not self.condition_f(trio):
                failed.append('F')
                continue
            return 'Meets conditions'
        return 'Fails: ' + ','.join(failed)


    def condition_a_and_b(self):
        #three cells such that r1 = r2 < r3 and c1 < c2 = c3
        satisfied = []
        n = len(self.zero_index)
        for i in range(n):
            r1,c1 = self.zero_index[i]
            for j in range(n):
                r2,c2 = self.zero_index[j]
                for k in range(n):
                    r3,c3 = self.zero_index[k]
                    #make sure all cells are unique
                    if len({(r1,c1), (r2,c2), (r3,c3)}) != 3:
                        continue
                    if r1 == r2 < r3 and c1 < c2 == c3:
                        satisfied.append(tuple(sorted([(r1, c1), (r2, c2), (r3, c3)])))
        return [list(t) for t in set(satisfied)]

    def condition_c(self, trio):
        #for all columns c2 != c != c1 cwt(D0)_c < cwt(D0)_{c2}
        r1,c1 = trio[0]
        r2,c2 = trio[1]
        return all(self.column_weight[c] < self.column_weight[c2]  for c in range(self.col_num) if c2 != c != c1)
    
    def condition_d(self, trio):
        #at least one empty space in each c1 <= c <= c2 
        r1,c1 = trio[0]
        r2,c2 = trio[1]
        for c in range(c1, c2 + 1):
            found_empty = False
            for r in range(0, r1):
                if (r, c) not in self.zero_index:
                    found_empty = True
                    break
            if not found_empty:
                return False
        return True
    
    def condition_e(self, trio):
        #the cell (r1,c2 + 1) not in the diagram
        r1,c1 = trio[0]
        r2,c2 = trio[1]
        return (r1, c2 + 1) not in self.zero_index
    
    def condition_f(self, trio):
        #for r > r1 the cell (r,c1) not in the diagram
        r1,c1 = trio[0]
        return not any((r,c1) in self.zero_index and r1 < r for (r,c) in self.zero_index)
    
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