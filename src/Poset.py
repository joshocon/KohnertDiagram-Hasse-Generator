class Poset:
    def __init__(self, graph):
        self.maximal_element = graph.get_root_node()
        self.minimal_elements = self._find_minimal_elements(graph)
        self.maximal_chains = self._find_all_maximal_chains(graph)
        
    def _find_minimal_elements(self, graph):
        minimal_elements = []
        for vertex in graph.get_vertices():
            if graph.get_neighbors(vertex) == []:
                minimal_elements.append(vertex)
        return minimal_elements
    
    def _find_all_maximal_chains(self, graph):
        root = graph.get_root_node()
        minimal_elements = self.get_minimal_elements()

        all_paths = []

        def dfs(node, path=[]):
            if node in minimal_elements:
                print('Node is minimal - adding path')
                all_paths.append(list(reversed(path + [node])))
                return
            if node not in graph.get_vertices():
                print('Node is not in graph')
                return
            for neighbor in graph.get_neighbors(node):
                print(f'Beginning DFS with neighbor: {neighbor}')
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

            