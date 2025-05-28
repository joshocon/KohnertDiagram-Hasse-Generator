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

    def add_edge(self, parent, child):
        parent_node = self._wrap(parent)
        child_node = self._wrap(child)

        if parent_node not in self.graph:
            self.graph[parent_node] = []
        self.graph[parent_node].append(child_node)

    def get_neighbors(self, vertex):
        return self.graph.get(self._wrap(vertex), [])
    
    def get_root_node(self):
        # Return the first node inserted, assuming it's the root
        return next(iter(self.graph.keys()), None)

    def all_nodes(self):
        return list(self.graph.keys())
    
    def get_vertices(self):
        return self.graph.keys()


