'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

class SoutheastDiagramGenerator:
    def __init__(self):
        self.dimension = 1
        self.sets = [[]]
        self.all_cells = []
        
    def is_southeast_extension(self, diagram, new_cell):
        for cell in diagram:
            if (min(cell[0],new_cell[0]), max(cell[1], new_cell[1])) not in diagram:
                return False
        return True
                
    def normalize_cells(self, cells):
        used_columns = sorted(set(y for (x, y) in cells))
        column_mapping = {old_y: new_y+1 for new_y, old_y in enumerate(used_columns)}
        normalized = sorted((x, column_mapping[y]) for (x, y) in cells)
        return normalized      
        
    def _generate(self, cells):
        self.sets = {frozenset()}
        for cell in cells:
            current_diagrams = list(self.sets) 
            for diagram in current_diagrams:
                new_diagram = set(diagram)
                new_diagram.add(cell)
                if self.is_southeast_extension(diagram, cell):
                    self.sets.add(frozenset(new_diagram))
    
    def get_all_cells(self):
        for i in range(1, self.dimension + 1):
            for j in range(self.dimension, 0, -1):
                new_cell = (i,j)
                self.all_cells.append(new_cell)
                
    def generate(self, dimension):
        self.dimension = dimension
        self.get_all_cells()
        self._generate(self.all_cells)
        with open("diagrams.txt", "w") as f:
            for diagram in self.sets:
                if not diagram:
                    continue
                line = ' '.join(f'({x},{y})' for (x, y) in sorted(diagram))
                f.write(line + '\n')            