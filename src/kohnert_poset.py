'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''
from collections import defaultdict


class KohnertPoset:
    def __init__(self, graph):
        self.maximal_element = graph.get_root_node()
        self.relations = graph
        self.minimal_elements = self._find_minimal_elements()
        self.monomial_dict = defaultdict(int)
        self.kohnert_polynomial = ''
        
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
    
    def _get_monomial_dict(self):
        
        root = self.maximal_element
        seen = set()
        
        def dfs(node):
            diagram = node.entry
            frozen = frozenset(diagram.cells)
            if frozen in seen:
                return
            seen.add(frozen)
            diagram.set_row_weight()
            monomial = diagram.get_monomial()
            self.monomial_dict[monomial] += 1

            for neighbor in self.relations.get_neighbors(node):
                dfs(neighbor)
                
        dfs(root)
        
    
    def get_minimal_elements(self):
        return self.minimal_elements
    
    def get_maximal_chains(self):
        return self.maximal_chains
    
    def is_bounded(self):
        return len(self.minimal_elements) == 1

    def is_ranked(self):
        return self._is_ranked()
    
    def is_monomial_multiplicity_free(self):
        self._get_monomial_dict()
        res = True
        terms = []
        for key, value in self.monomial_dict.items():
            if value != 1:
                terms.append(f"{value}{key}")
                res = False
            else:
                terms.append(f"{key}")
        self.kohnert_polynomial = " + ".join(terms)
        return res

    def boundedness_result(self):
        res = f'Hasse Diagram of {self.maximal_element.entry.cells}. Bounded: {self.is_bounded()}'
        return res
    
    def rankedness_result(self):
        res = f'Hasse Diagram of {self.maximal_element.entry.cells}. Ranked: {self.is_ranked()}'
        return res
    
    def monomial_multiplicity_free_result(self):
        bool = self.is_monomial_multiplicity_free()
        res = f'Hasse Diagram of {self.maximal_element.entry.cells} (Polynomial: ${self.kohnert_polynomial}$). MMF: {bool}'
        return res
         
    
    def is_simple(self):
        return len(self.maximal_chains[0]) == 1 and len(self.maximal_chains) == 1