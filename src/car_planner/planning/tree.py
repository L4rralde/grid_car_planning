import gridsim.glutils as GLUtils

class Node:
    def __init__(self, data: object, parent: object=None) -> None:
        self.data = data
        self.parent = parent
        self.children = []

    def append(self, data: object) -> None:
        self.children.append(Node(data, self))


class Tree:
    def __init__(self, root: object) -> None:
        self.root = Node(root)  # Renamed to root
    
    def find(self, data: object, start_node: Node = None) -> Node:
        """Depth-first search for node with matching data"""
        current = start_node or self.root
        
        # Check current node first
        if current.data == data:
            return current
        
        # Recursively search children
        for child in current.children:
            found = self.find(data, child)
            if found:
                return found
        
        return None  # Not found in subtree
