import json

INS_TYPES = ['SINGLE', 'SRC', 'CAL', 'DEST_OFFSET', 'BYTE', 'DEST', 'SRC_DEST', 'JMP', 'SRC_DEST_JMP', 'SRC_DEST_OFFSET', 'SRC_DEST_IM']
INS_OPS = {
    "SINGLE":["OPCODE"],
    "SRC":["OPCODE","REG"],
    "CAL":["OPCODE","VALUE"],
    "DEST_OFFSET":["OPCODE","REG","VALUE"],
    "BYTE":["OPCODE","VALUE"],
    "DEST":["OPCODE","REG"],
    "SRC_DEST":["OPCODE","REG","REG"],
    "JMP":["OPCODE","VALUE"],
    "SRC_DEST_JMP":["OPCODE","REG","REG","VALUE"],
    "SRC_DEST_OFFSET":["OPCODE","REG","REG","VALUE"],
    "SRC_DEST_IM":["OPCODE","REG","REG","VALUE"]
}

regDic = {"SP":15,"RA":16,"ZERO":0}
HX = "ABCDEF"
for i in range(16):
    regDic.update({str(i):i,"R"+str(i):i})
    if i > 9:
        H = HX[i-10]
        regDic.update({"R"+H:i,H:i})

sizeDecls = {"B":1,"BYTE":1,"H":2,"HALF":2,"W":4,"WORD":4}


with open("INS.json") as JSONFILE:
    insdic = json.load(JSONFILE)
    for names in insdic.keys():
        ins = insdic[names]
        ins.update({"OPRANDS":INS_OPS[ins["TYPE"]],"MEM":names})
    with open("ASM.json",'w') as UPDATEFILE:
        dic = {"INS":insdic,"REGISTERS":regDic,"MEMORY_SIZES":sizeDecls}
        json.dump(dic,UPDATEFILE,indent=4)