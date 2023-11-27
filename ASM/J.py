import json
from tokenizer import tokenizer

def readJSON(jsonF):
    ins = {}
    Regs = {}
    MemSizes = {}
    with open(jsonF) as JF:
        info = json.load(JF)
        for i in info["Instructions"]:
            ins.update({i["MEM"]:i})
        Regs = info["REGISTERS"]
        MemSizes = info["MEMORY_SIZES"]
    return ins,Regs,MemSizes

def testToken():
    ins,Regs,MemSizes = readJSON("JRISCins.json")
    T_types = []
    for i in ins.values():
        if i["Im_Type"] not in T_types:
            T_types.append(i["Im_Type"])
    print(T_types)
    
if __name__ == "__main__":
    testToken()