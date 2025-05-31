'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

from Node import Node

class Graph:
    def __init__(self):
        self.graph = {}
        self.nodes_by_entry = {}

    def _wrap(self, item):
        if not isinstance(item, Node):
            if item not in self.nodes_by_entry:
                self.nodes_by_entry[item] = Node(item)
            return self.nodes_by_entry[item]
        return item

    def add_vertex(self, vertex):
        node = self._wrap(vertex)
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, vertex, neighbor):
        vertex_node = self._wrap(vertex)
        neighbor_node = self._wrap(neighbor)

        if vertex_node not in self.graph:
            self.graph[vertex_node] = []
        self.graph[vertex_node].append(neighbor_node)

    def get_neighbors(self, vertex):
        return self.graph.get(self._wrap(vertex), [])
    
    def get_root_node(self):
        return next(iter(self.graph.keys()), None)

    def all_nodes(self):
        return list(self.graph.keys())
    
    def get_vertices(self):
        return self.graph.keys()
    
    def get_all_neighbors(self):
        return self.graph.values()
    
    def get_all_items(self):
        return self.graph.items()
    
    def __repr__(self):
        string = ''
        for vertex in self.get_vertices():
           string += f'\nVertex: {vertex} Neighbors: '
           for neighbor in self.get_neighbors(vertex):
                string += f'{neighbor}'
            
        return string
    

                
                    



