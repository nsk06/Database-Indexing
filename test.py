import sys
inp = sys.argv[1]
inp2 = sys.argv[2]

def data(inp):
    res = []
    with open(inp) as f:
        lines = f.readlines()
        lines = [i.strip() for i in lines]
        for i in lines:
            res.append(int(i))
    return res
res = data(inp)
me = list(set(res))
if(len(me)!=len(res)):
    print("different length")
    # sys.exit(-1)
check = data(inp2)
for i in range(len(me)):
    if res[i] != check[i]:
        print(i+1,res[i],check[i])