import sys
class LinearHash:
    def __init__(self):
        self.buckets = {}
        self.nbuckets = 2
        self.bucketcapacity = 2
        self.splitpercent = .75
        self.splitpos = 0
        self.curmod = 2
        self.partialsplit = False
        self.partialmod = 2*self.curmod
    def insertvalue(self,val):
        pres = self.searchindex(val)
        if(pres):
            # print("present")
            return 
        else:
            print(val)
            hash_value = val%self.curmod
            if (self.partialsplit):
                if(hash_value<self.splitpos):
                    hash_value = val%(self.partialmod)
                    if hash_value not in self.buckets:
                        self.buckets[hash_value] = [val]
                    else:
                        self.buckets[hash_value].append(val)
                        if(len(self.buckets[hash_value])>self.bucketcapacity):
                            self.splitbucket()
                else:
                    if hash_value not in self.buckets:
                        self.buckets[hash_value] = [val]
                    else:
                        self.buckets[hash_value].append(val)
                        if(len(self.buckets[hash_value])>self.bucketcapacity):
                            self.splitbucket()
            else:
                if hash_value not in self.buckets:
                    self.buckets[hash_value] = [val]
                else:
                    self.buckets[hash_value].append(val)
                    if(len(self.buckets[hash_value])>self.bucketcapacity):
                        self.partialsplit = True
                        self.partialmod = self.curmod*2
                        self.splitbucket()
        # print(self.buckets)
    def splitbucket(self):
        temp = []
        # print("Splitting",self.splitpos)
        # if self.splitpos not in self.buckets:
        #     self.buckets[self.splitpos] = []
        self.nbuckets+=1
        self.buckets[len(self.buckets)] = []
        for i in self.buckets[self.splitpos]:
            if i%self.partialmod not in self.buckets:
                self.buckets[i%self.partialmod] = [i]
            else:
                temp.append(i)
        self.buckets[self.splitpos]=temp
        self.splitpos+=1
        # print("After Spit",self.buckets)
        if(len(self.buckets)==self.partialmod):
            self.splitpos=0
            self.curmod = self.partialmod
            self.partialsplit=False
    def searchindex(self,val):
        hash_value = val%self.curmod
        if(hash_value<self.splitpos):
            hash_value = val%self.partialmod
            if hash_value not in self.buckets:
                return False
            else:
                if val not in self.buckets[hash_value]:
                    return False
                else:
                    return True
        else:
            if hash_value not in self.buckets:
                return False
            else:
                if val not in self.buckets[hash_value]:
                    return False
                else:
                    return True    

def main():
    global Hash
    if(len(sys.argv)!=2):
        print("Please only input test_file as command line")
        sys.exit(-1)
    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
        lines = [i.strip() for i in lines]
        commands = []
        for i in lines:
            commands.append(int(i))
    for c in commands:
        Hash.insertvalue(c)

if __name__ == "__main__":
    Hash = LinearHash()
    main()