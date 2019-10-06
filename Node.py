class Node:
    '''This is the node class'''
    def __init__(self,cap):
        self.capacity = cap
        self.keys = []
        self.pointers = []
        self.leafcheck = True
        self.right_node = None

    def nodesplit(self):
        mynewnode = Node(self.capacity)
        mid = len(self.keys)//2
        midpoint = self.keys[mid]
        if self.leafcheck == True:
            mynewnode.leafcheck = True
            mynewnode.keys = self.keys[mid:]
            mynewnode.pointers = self.pointers[mid:]
            self.keys = self.keys[:mid]
            self.pointers = self.pointers[:mid]
            mynewnode.right_node = self.right_node
            self.right_node = mynewnode
            # print("idhr dekhna,,",self.right_node.keys)
        else:
            mynewnode.leafcheck = False
            mynewnode.keys = self.keys[mid+1:]
            mynewnode.pointers = self.pointers[mid+1:]
            self.keys = self.keys[:mid]
            self.pointers = self.pointers[:mid+1]
        
        return midpoint,mynewnode
