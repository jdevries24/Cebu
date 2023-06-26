from Tools import *

class FirstPass:

    def __init__(self,Tokens,ASM_INFO):
        self.INS_DIC = ASM_INFO["INS"]
        self.REGISTERS = ASM_INFO["REGISTERS"]
        self.MEMORY_SIZES = ASM_INFO["MEMORY_SIZES"]
        self.VAR_TABLE = {}
        self.LOCATION_TABLE = {}
        self.LINES = []
        self.ERRORS = []
        self.LOC = 0
        self.TokenQueu = Tokens
        self.TokenQueu.reverse()

    def Run_Pass(self):
        nextToken = self.TokenQueu.pop()
        while (len(self.TokenQueu) > 0) and (nextToken.type != "EOF"):
            try:
                if nextToken.type == "nl":
                    pass
                elif nextToken.type == "var":
                    self.VAR(nextToken)
                elif nextToken.type == "ins":
                    self.INS(nextToken)
                elif (nextToken.type == "g_addr") or (nextToken.type == "l_addr"):
                    self.ADDRESS(nextToken)
            except ASSEMBLYERROR as AE:
                self.ERRORS.append(AE)
                self.PassLine()
            finally:
                nextToken = self.TokenQueu.pop()
    
    def peek(self):
        if len(self.TokenQueu) == 0:
            raise ASSEMBLYERROR("Unexpected End of File",0)
        Toke = self.TokenQueu[-1]
        if Toke.type == "var":
            return self.findvar(Toke)
        return Toke
    
    def dequeu(self):
        if len(self.TokenQueu) == 0:
            raise ASSEMBLYERROR("Unexpeced End of File",0)
        Toke = self.TokenQueu.pop()
        if Toke.type == "var":
            return self.findvar(Toke)
        return Toke
    
    def findvar(self,var):
        if var.text not in self.VAR_TABLE.keys():
            raise ASSEMBLYERROR("Var not found",var.line)
        return self.VAR_TABLE[var.text]
    
    def PassLine(self):
        while True:
            if (self.TokenQueu[-1].type in ("EOF","nl")):
                break
            self.TokenQueu.pop()
    
    def VAR(self,Token):
        nextToken = self.dequeu()
        if (nextToken.type in ["EOF","nl"]):
            raise ASSEMBLYERROR("Undefined Varible",Token.line)
        self.VAR_TABLE.update({Token.text:nextToken})
        if (self.TokenQueu[-1].type not in ["EOF","nl"]):
            raise ASSEMBLYERROR("Double diffened Var",Token.line)
        
    def INS(self,Token):
        if(Token.text not in self.INS_DIC.keys()):
            raise ASSEMBLYERROR("Cannot find Instruction "+Token.text,Token.line)
        I = INSTRUCTION(Token.line,self.INS_DIC[Token.text],self.LOC)
        self.LOC += I.INS["SIZE"]
        OPRANDS = I.INS["OPRANDS"][1:]
        AT_END = False
        for ops in OPRANDS:
            if AT_END:
                raise ASSEMBLYERROR("Missing a "+ops,Token.line)
            Token = self.dequeu()
            if Token.type == "comma":
                raise ASSEMBLYERROR("Possible double comma",Token.line)
            if ops == "REG":
                if Token.text not in self.REGISTERS.keys():
                    raise ASSEMBLYERROR(Token.text +" is not a register",Token.line)
                I.Oprands.append(self.REGISTERS[Token.text])
            else:
                I.Oprands.append(Token)
            if self.peek().type in ("EOF","nl"):
                AT_END = True
            if self.peek().type == "comma":
                self.dequeu()
        self.LINES.append(I)
        
    def ADDRESS(self,Token):
        self.LOCATION_TABLE.update({Token.text:self.LOC})
        MEMLINE = ADDRESS(Token.line,Token.text,self.LOC)
        print(self.TokenQueu[-1])
        if self.TokenQueu[-1].type in ("EOF","nl"):
            self.LINES.append(MEMLINE)
            return
        Token = self.dequeu()
        if Token.type != "ins":
            raise ASSEMBLYERROR("Expected memory type",Token.line)
        if Token.text == "ZERO":
            Token = self.dequeu()
            if Token.type != "int":
                raise ASSEMBLYERROR("Expected Zero size to be an interger")
            self.LOC += TOOLS.str_to_int(Token.text)
            MEMLINE.Value = [0 for i in range(TOOLS.str_to_int(Token.text))]
            if self.TokenQueu[-1].type not in ("EOF","nl"):
                raise ASSEMBLYERROR("Extra value in zero decl")
            self.LINES.append(MEMLINE)
            return
        if Token.text not in self.MEMORY_SIZES:
            raise ASSEMBLYERROR("Unrecognized memory type",Token.line)
        itemsize = self.MEMORY_SIZES[Token.text]
        MEMLINE.ItemSize = itemsize
        Token = self.dequeu()
        while True:
            if(Token.type == "comma"):
                pass
            elif(Token.type == "str"):
                self.LOC += (len(Token.text) * itemsize)
                MEMLINE.Oprands.append(Token)
            else:
                self.LOC += itemsize
                MEMLINE.Oprands.append(Token)
            if (self.TokenQueu[-1].type in ("EOF","nl")):
                break
            Token = self.dequeu()
        self.LINES.append(MEMLINE)