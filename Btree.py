import sys,os
from bisect import *
from Node import Node
class Btree:
    '''Btree main class'''
    def __init__(self):
        self.nodecapacity = 3
        self.treeroot = Node(self.nodecapacity)
    def keyinsertstart(self,query):
        cur_root = self.treeroot
        mynewnode,splitroot = self.keyinsert(query,self.treeroot)
        if splitroot:
            tempnode = Node(self.nodecapacity)
            tempnode.keys.append(splitroot)
            tempnode.pointers.append(self.treeroot)
            tempnode.pointers.append(mynewnode)
            tempnode.leafcheck = False
            self.treeroot = tempnode
    
    def keyinsert(self,query,insertnode):
        splitcheck = None
        if insertnode.leafcheck == True:
            pos = bisect_right(insertnode.keys,query)
            if(pos > len(insertnode.keys)-1):
                insertnode.keys.append(query)
            else:
                insertnode.keys.insert(pos,query)
            if len(insertnode.keys) > insertnode.capacity:
                midpoint,mynewnode = insertnode.nodesplit()
                return mynewnode,midpoint
            else:
                return None,None                
        
        else:
            
            if query < insertnode.keys[0]:
                mynewnode,splitcheck = self.keyinsert(query,insertnode.pointers[0])
            if (query >= insertnode.keys[len(insertnode.keys)-1]):
                mynewnode,splitcheck  = self.keyinsert(query,insertnode.pointers[len(insertnode.pointers)-1])

            for i in range(len(insertnode.keys)-1):
                if (query < insertnode.keys[i+1] and  query >= insertnode.keys[i]  ):
                    mynewnode,splitcheck = self.keyinsert(query,insertnode.pointers[i+1])
            
        if splitcheck:
            pos = bisect_right(insertnode.keys,splitcheck)
            if(pos > len(insertnode.keys)-1):
                insertnode.keys.append(splitcheck)
                insertnode.pointers.insert(pos+1,mynewnode)
            else:
                insertnode.keys.insert(pos,splitcheck)
                insertnode.pointers.insert(pos+1,mynewnode)
            # insertnode.keys[pos] = splitcheck
            # insertnode.pointers[pos+1] = mynewnode
            if(len(insertnode.keys) > insertnode.capacity):
                midpoint,mynewnode = insertnode.nodesplit()
                return mynewnode,midpoint
            else:
                return None,None                
        else:
            return None,None
    
    def findnode(self,query,curnode):
        if curnode.leafcheck == True:
            return curnode
        if query <= curnode.keys[0]:
            check_node = self.findnode(query,curnode.pointers[0])
            return check_node
        if query > curnode.keys[len(curnode.keys)-1]:
            return self.findnode(query,curnode.pointers[len(curnode.pointers)-1])
        for i in range(len(curnode.keys)-1):
            if (query <= curnode.keys[i+1] and query > curnode.keys[i]):
                check_node = self.findnode(query,curnode.pointers[i+1])
                return check_node 
    def rangecount(self,startmin,endmax,startnode):
        ret = 0
        right_node = None
        if(len(startnode.keys)==0):
            return 0,None

        for keys in startnode.keys:
            if (keys <= endmax and keys>=startmin):
                # print("here",keys)
                ret+=1
        if(startnode.keys[len(startnode.keys)-1]>endmax):
            right_node = None
        else:
            if not startnode.right_node :
                right_node = None     
                # print("test")
               
            else:
                right_node = startnode.right_node
                # print("YOYO",right_node.keys)
                # sys.exit(1)

        
        return ret,right_node
    def rangeinitialise(self,mymin,mymax):
        # print(mymin,mymax)
        start_node = self.findnode(mymin,self.treeroot)
        res = 0
        # print("test2",start_node.right_node)
        count,right_node = self.rangecount(mymin,mymax,start_node)
        res += count
        # print("kidhr",right_node)
        while right_node != None:
            count,right_node = self.rangecount(mymin,mymax,right_node)
            res += count
        return res

   


def runtests(command):
    global Tree
    if(command[0]=="INSERT"):
        Tree.keyinsertstart(int(command[1]))
        return -1
    elif(command[0]=="FIND"):
        ans = Tree.rangeinitialise(int(command[1]),int(command[1]))
        if ans ==0:
            return "NO"
        else:
            return "YES"
    elif(command[0]=="COUNT"):
        ans = Tree.rangeinitialise(int(command[1]),int(command[1]))
        return ans
    elif(command[0]=="RANGE"):
        ans = Tree.rangeinitialise(int(command[1]),int(command[2]))
        return ans
    else:
        print("Query Not Supported")
        sys.exit(-1)

def main():
    if(len(sys.argv)!=2):
        print("Please only input test_file as command line")
        sys.exit(-1)
    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
        lines = [i.strip() for i in lines]
        commands = []
        for i in lines:
            commands.append(i.split())
    out = []
    # print(commands)
    for c in commands:
        # print(c)
        ret = runtests(c)
        if(ret!=-1):
            out.append(ret)
            # print("Answer is ",ret)
    for o in out:
        print(o)

if __name__ == "__main__":
    Tree = Btree()
    main()
