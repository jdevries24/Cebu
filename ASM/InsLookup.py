RR = 0
RRI = 1
I = 2
O = 3
R = 4
RI = 5
IN = 6

N = 0
U16 = 1
S16 = 2
S20 = 3
S24 = 5
U8 = 6
U24 = 7

regLookup = ["R"+str(i) for i in range(14)] + ["SP","RA"]
formatTypes = [O,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,RR,RR,RR,None,RR,RR,RR,None,RR,RR,RR,None,None,None,None,None,RRI,RRI,RRI,None,RRI,RRI,RRI,None,RRI,RRI,RRI,None,None,None,None,None,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RR,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,RRI,None,I,RRI,RRI,RRI,RRI,None,None,None,None,None,None,None,None,None,None,None,None,RRI,RRI,RRI,RRI,None,None,None,None,None,None,None,None,None,None,None,None,RI,RRI,RR,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,I,R,None,None,None,None,None,None,None,None,None,None,None,None,None,None,O,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,IN,O,R,R,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,I,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
immTypes = [N,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,N,N,N,None,N,N,N,None,N,N,N,None,None,None,None,None,S16,S16,S16,None,S16,S16,S16,None,S16,S16,S16,None,None,None,None,None,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,U16,U16,U16,U16,U16,U16,U16,U16,U16,U16,U16,U16,U16,U16,U16,None,S24,S16,S16,S16,S16,None,None,None,None,None,None,None,None,None,None,None,None,S16,S16,S16,S16,None,None,None,None,None,None,None,None,None,None,None,None,S20,U16,N,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,S24,N,None,None,None,None,None,None,None,None,None,None,None,None,None,None,N,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,U8,N,N,N,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,U24,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
mems = ["NOP",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,"LDB","LDH","LDW",None,"LDBS","LDHS","LDWS",None,"STB","STH","STW",None,None,None,None,None,"LDBI","LDHI","LDWI",None,"LDBSI","LDHSI","LDWSI",None,"STBI","STHI","STWI",None,None,None,None,None,"ADD","SUB","AND","ORR","XOR","NOT","NEG","LSL","LSR","MUL","SMUL","MOD","SMOD","DIV","SDIV","MOV","ADDI","SUBI","ANDI","ORRI","XORI","ASLI","ASRI","LSLI","LSRI","MULI","SMULI","MODI","SMODI","DIVI","SDIVI",None,"JMP","JEQ","JNE","JLT","JGT",None,None,None,None,None,None,None,None,None,None,None,None,"JSEQ","JSNE","JSLT","JSGT",None,None,None,None,None,None,None,None,None,None,None,None,"LEA","MOVU","ADDPC",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,"CAL","CAR",None,None,None,None,None,None,None,None,None,None,None,None,None,None,"RET",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,"INT","RINT","POPIRA","PSHIRA",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,"CSR",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
mems[0x4f] = "MOV"
pcRelitive = [0x50,0x51,0x52,0x53,0x54,0x61,0x62,0x63,0x64,0x71,0xA0]
immTypes[0x4f] = N
formatTypes[0x4f] = RR