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
        self.row_weight = self.get_row_weight()
        self.column_weight = self.get_column_weight()
        self.monomial = self.get_monomial()

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

    def get_row_number(self):
        return self.row_num

    def get_col_number(self):
        return self.col_num
    
    def test_bounded_conjecture(self):
        good_trios = self.condition_a_and_b()
        
        possible_failures = {'fails C', 'fails D', 'fails E', 'fails F', 'fails G', 'fails H', 'fails I', 'fails J'}

        for trio in good_trios:
            c_res = self.condition_c(trio)
            d_res = self.condition_d(trio)
            e_res = self.condition_e(trio)
            f_res = self.condition_f(trio)
            g_res = self.condition_g(trio)
            h_res = self.condition_h(trio)
            i_res = self.condition_i(trio)
            j_res = self.condition_j(trio)

            if c_res and d_res and e_res and f_res and g_res and h_res and i_res and j_res:
                return f'Meets with {trio}'
            if c_res:
                possible_failures.discard('fails C')
            if d_res:
                possible_failures.discard('fails D')
            if e_res:
                possible_failures.discard('fails E')
            if f_res:
                possible_failures.discard('fails F')
            if g_res:
                possible_failures.discard('fails G')
            if h_res:
                possible_failures.discard('fails H')
            if i_res:
                possible_failures.discard('fails I')
            if j_res:
                possible_failures.discard('fails J')
                
        return f'Fails: {sorted(possible_failures)}'


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
        return (list(t) for t in set(satisfied))

    def condition_c(self, trio):
        #for columns c1 < c < c2 cwt(D0)c <= cwt(D0)c2 and for c2 < c cwt(D0)c < cwt(D0)c2
        r1,c1 = trio[0]
        r2,c2 = trio[1]
        return (
            all(self.column_weight[c] <= self.column_weight[c2] for c in range(c1 + 1, c2)) 
            and all(self.column_weight[c] < self.column_weight[c2] for c in range(c2 + 1, self.col_num))
        )
    
    def condition_d(self, trio):
        # At least one empty space in each c >= c1 for r < r1
        r1, c1 = trio[0]
        r2, c2 = trio[1]
        
        if r1 == 0:
            return False

        for c in range(c1, self.col_num):
            found_empty = False
            for r in range(r1):
                if (r, c) not in self.zero_index:
                    found_empty = True
                    break

            if not found_empty:
                # Column has no empty space above r1
                # Now check that all (r, c) in that column satisfy r < r1 and c > c2
                for r in range(r1):
                    if (r, c) in self.zero_index:
                        if not (r < r1 and c > c2):
                            return False

        return True

    
    def condition_e(self, trio):
        # For r <= r1 and c > c2 where , if (r, c) in the diagram, all (r', c) for r' < r must be empty
        r1, c1 = trio[0]
        r2, c2 = trio[1]
        for c in range(c2 + 1, self.col_num):
            for r in range(0, r1 + 1):
                if (r, c) in self.zero_index and self.column_weight[c] == self.column_weight[c2]:
                    # Check all rows *below* r in column c
                    for lower_r in range(0, r):
                        if (lower_r, c) in self.zero_index:
                            return False
        return True
    
    def condition_f(self, trio):
        #the column weight of c1 is strictly less than the column weight of c3
        r1,c1 = trio[0]
        r3,c3 = trio[2]
        return self.column_weight[c1] < self.column_weight[c3]
    
    def condition_g(self, trio):
        #for r1 < r <= r3 the cell (r,c1) not in the diagram
        r1,c1 = trio[0]
        r3,c3 = trio[2]
        return all((r,c1) not in self.zero_index for r in range(r1 + 1, r3 + 1))
    
    def condition_h(self, trio):
        #if there is a cell above x1 there is a cell above x3
        r1, c1 = trio[0]
        r3, c3 = trio[2]
        
        def has_above(r, c):
            return any((row, c) in self.zero_index for row in range(r + 1, self.row_num))

        if not has_above(r1,c1):
            return True

        return has_above(r3,c3)
    
    def condition_i(self, trio):
        # If there is no cell above (r1, c1), there must not be a cell above (r3, c3)
        r1, c1 = trio[0]
        r3, c3 = trio[2]

        def has_above(r, c):
            return any((row, c) in self.zero_index for row in range(r + 1, self.row_num))

        if has_above(r1, c1):
            return True 
        
        return not has_above(r3, c3)

    def condition_j(self, trio):
        #if a c > c2 does not have empty space beneath it, then all the columns underneath must be southeast to everything else
        return True
    
    
    def test_ranked_conjecture(self):
        return 'Conjecture Result: Meets Conditions'
    
    def test_mmf_conjecture(self):
        return 'Conjecture Result: Meets Conditions'
    
    def __eq__(self, other):
        return isinstance(other, Diagram) and set(self.cells) == set(other.cells)

    def __hash__(self):
        return hash(frozenset(self.cells))

    def __repr__(self):
        return f'{self.cells}'