'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

class KohnertPoset:
    def __init__(self, graph):
        self.maximal_element = graph.get_root_node()
        self.relations = graph
        self.minimal_elements = self._find_minimal_elements()
        self.maximal_chains = 1
        
    def _find_minimal_elements(self):
        graph = self.relations
        minimal_elements = []
        for vertex in graph.get_vertices():
            if graph.get_neighbors(vertex) == []:
                minimal_elements.append(vertex)
        return minimal_elements
    
    def _find_all_maximal_chains(self):
        graph = self.relations
        root = graph.get_root_node()
        minimal_elements = self.get_minimal_elements()

        all_paths = []

        def dfs(node, path=[]):
            if node in minimal_elements:
                all_paths.append(list(reversed(path + [node])))
                return
            if node not in graph.get_vertices():
                return
            for neighbor in graph.get_neighbors(node):
                dfs(neighbor, path + [node])

        dfs(root)
        return all_paths
    
    def get_minimal_elements(self):
        return self.minimal_elements
    
    def get_maximal_chains(self):
        return self.maximal_chains
    
    def is_bounded(self):
        return len(self.minimal_elements) == 1

    def is_ranked(self):
        expected_length = len(self.maximal_chains[0])
        return all(len(chain) == expected_length for chain in self.maximal_chains)
    
    def result(self):
        graph = self.relations
        res = f'Hasse Diagram of {graph.get_root_node().entry.cells}. Bounded: {self.is_bounded()}'#. Ranked: {self.is_ranked()}'
        return res
    
    def is_simple(self):
        return len(self.maximal_chains[0]) == 1 and len(self.maximal_chains) == 1
    
    def is_monomial_multiplicity_free(self, polynomial):
        return all(monomial_multiplicity == 1 for monomial_multiplicity in polynomial.items())