import sys,os
from bisect import *
from Node import Node
class Btree:
    '''Btree main class'''
    def __init__(self):
        self.root = Node()
    
    def keyinsertstart(self,key):
        splitcheck,mynewnode = self.keyinsert(key,self.root)
        if splitcheck:
            tempnode = Node()
            tempnode.leafcheck = False
            tempnode.keys.append(splitcheck)
            tempnode.pointers.append(self.root)
            tempnode.pointers.append(mynewnode) 
            self.root = tempnode
        # print("*******************",self.root.keys,self.root.pointers)
        # for i in self.root.pointers:
        #     print (i.keys)
        
    
    def keyinsert(self,key,insertnode):
        splitcheck = None
        if insertnode.leafcheck == True:
            pos = bisect_right(insertnode.keys,key)
            if(pos > len(insertnode.keys)-1):
                insertnode.keys.append(key)
                # insertnode.pointers[pos:pos] = [key]
            else:
                insertnode.keys.insert(pos,key)
                # insertnode.pointers.insert(pos,key)
            if len(insertnode.keys) <= insertnode.capacity:
                return None,None
            else:
                midpoint,mynewnode = insertnode.nodesplit()
                return midpoint,mynewnode
        
        else:
            if key < insertnode.keys[0]:
                splitcheck,mynewnode = self.keyinsert(key,insertnode.pointers[0])
            for i in range(len(insertnode.keys)-1):
                if (key >= insertnode.keys[i] and key < insertnode.keys[i+1]):
                    splitcheck,mynewnode = self.keyinsert(key,insertnode.pointers[i+1])
            if (key >= insertnode.keys[len(insertnode.keys)-1]):
                splitcheck,mynewnode = self.keyinsert(key,insertnode.pointers[-1])
        if splitcheck:
            pos = bisect_right(insertnode.keys,splitcheck)
            if(pos > len(insertnode.keys)-1):
                insertnode.keys.append(splitcheck)
                insertnode.pointers[pos+1:pos+1] = [mynewnode]
            else:
                insertnode.keys.insert(pos,splitcheck)
                insertnode.pointers[pos+1:pos+1] = [mynewnode]
            # insertnode.keys[pos] = splitcheck
            # insertnode.pointers[pos+1] = mynewnode
            if(len(insertnode.keys) <= insertnode.capacity):
                return None,None
            else:
                midpoint,mynewnode = insertnode.nodesplit()
                return midpoint,mynewnode
        else:
            return None,None
    
    def findnode(self,key,curnode):
        if curnode.leafcheck == True:
            return curnode
        
        if key <= curnode.keys[0]:
            check_node = self.findnode(key,curnode.pointers[0])
            return check_node
        if key > curnode.keys[len(curnode.keys)-1]:
            return self.findnode(key,curnode.pointers[-1])
        for i in range(len(curnode.keys)-1):
            if key > curnode.keys[i] and key <= curnode.keys[i+1]:
                check_node = self.findnode(key,curnode.pointers[i+1])
                return check_node 
    def rangeinitialise(self,mymin,mymax):
        # print(mymin,mymax)
        res = 0
        start_node = self.findnode(mymin,self.root)
        # print("test2",start_node.right_node)
        count,right_node = self.rangecount(mymin,mymax,start_node)
        res += count
        # print("kidhr",right_node)
        while right_node:
            count,right_node = self.rangecount(mymin,mymax,right_node)
            res += count
        return res

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
            if startnode.right_node :
                right_node = startnode.right_node
                # print("YOYO",right_node.keys)
                # sys.exit(1)
            else:
                # print("test")
                right_node = None
        
        return ret,right_node
        
    def findkeycount(self,key):
        start_node = self.findnode(key,self.root)
        res = 0
        # print("test4",start_node.keys)
        count,right_node = self.rangecount(key,key,start_node)
        # if right_node:
            # print(right_node.keys)
            # sys.exit(1)
        res += count
        while right_node:
            count,right_node = self.rangecount(key,key,right_node)
            res += count
        return res


def runtests(command):
    global Tree
    if(command[0]=="INSERT"):
        Tree.keyinsertstart(int(command[1]))
        return -1
    elif(command[0]=="FIND"):
        ans = Tree.findkeycount(int(command[1]))
        if ans ==0:
            return "NO"
        else:
            return "YES"
    elif(command[0]=="COUNT"):
        ans = Tree.findkeycount(int(command[1]))
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