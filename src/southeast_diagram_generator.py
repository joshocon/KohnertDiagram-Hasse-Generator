from .diagram_engine import DiagramEngine

class SoutheastDiagramGenerator:
    def __init__(self, dimension):
        self.dimension = dimension
        self.sets = [[]]
        self.engine = DiagramEngine()
        self.all_cells = []
        
    def get_all_cells(self):
        for i in range(1, self.dimension + 1):
            for j in range(self.dimension, 0, -1):
                new_cell = (i,j)
                self.all_cells.append(new_cell)
                
    def generate(self):
        self.get_all_cells()
        self._generate_recursive(self.all_cells)
        self.sets.pop(0)
        with open('diagrams.txt', 'w') as f:
            for diagram in self.sets:
                line = ' '.join(f'({x},{y})' for (x, y) in diagram)
                f.write(line + '\n')

    def _generate_recursive(self, remaining_cells):
        if not remaining_cells:
            return

        cell = remaining_cells[0]
        new_diagrams = []

        for diagram in self.sets:
            new_diagram = diagram.copy()
            new_diagram.append(cell)

            if self.engine.check_south_east(new_diagram):
                if new_diagram not in self.sets and new_diagram not in new_diagrams:
                    new_diagrams.append(new_diagram)

        self.sets.extend(new_diagrams)
        self._generate_recursive(remaining_cells[1:])
                    
                
                
    
                        
        
                