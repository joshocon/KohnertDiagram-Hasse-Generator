'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

class Node:
    def __init__(self, entry):
        self.entry = entry
        self.draw_string = ''
        self.pos = ()

    def __eq__(self, other):
        return isinstance(other, Node) and self.entry == other.entry

    def __hash__(self):
        return hash(self.entry)

    def __repr__(self):
        return f"Node({repr(self.entry)})"