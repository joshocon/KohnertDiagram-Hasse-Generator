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
        
    def _find_minimal_elements(self):
        graph = self.relations
        minimal_elements = []
        for vertex in graph.get_vertices():
            if graph.get_neighbors(vertex) == []:
                minimal_elements.append(vertex)
        return minimal_elements
    
    def _is_ranked(self):
        from collections import defaultdict, deque

        in_degree = defaultdict(int)
        rank = {}
        neighbors = defaultdict(list)
        graph = self.relations

        for u in graph.get_vertices():
            for v in graph.get_neighbors(u):  
                neighbors[u].append(v)
                in_degree[v] += 1

        queue = deque()
        for v in graph.get_vertices():
            if in_degree[v] == 0:
                rank[v] = 0
                queue.append(v)

        while queue:
            u = queue.popleft()
            for v in neighbors[u]:
                expected_rank = rank[u] + 1
                if v in rank:
                    if rank[v] != expected_rank:
                        return False 
                else:
                    rank[v] = expected_rank

                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        max_ranks = set()
        for v in graph.get_vertices():
            if not neighbors[v]: 
                max_ranks.add(rank[v])

        return len(max_ranks) == 1
    
    def get_minimal_elements(self):
        return self.minimal_elements
    
    def get_maximal_chains(self):
        return self.maximal_chains
    
    def is_bounded(self):
        return len(self.minimal_elements) == 1

    def is_ranked(self):
        return self._is_ranked()
    
    def result(self):
        graph = self.relations
        res = f'Hasse Diagram of {graph.get_root_node().entry.cells}. Bounded: {self.is_bounded()}. Ranked: {self.is_ranked()}'
        return res
    
    def is_simple(self):
        return len(self.maximal_chains[0]) == 1 and len(self.maximal_chains) == 1
    
    def is_monomial_multiplicity_free(self, polynomial):
        return all(monomial_multiplicity == 1 for monomial_multiplicity in polynomial.items())