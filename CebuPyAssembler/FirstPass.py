from Tools import *

class FirstPass:

    def __init__(self,Tokens,ASM_INFO):
        """Takes in a series of tokens and a Directory of information about the Instruction set given"""
        self.INS_DIC = ASM_INFO["INS"]
        self.REGISTERS = ASM_INFO["REGISTERS"]
        self.MEMORY_SIZES = ASM_INFO["MEMORY_SIZES"]
        self.VAR_TABLE = {} #Var tokens and values
        self.LOCATION_TABLE = {} #Offsets of all the mentioned locations
        self.LINES = [] #Nodes that hold information about diffrent instructions and Memory Locations
        self.ERRORS = [] #Errors found while passing
        self.LOC = 0 #Location in the assembly
        self.TokenQueu = Tokens
        self.TokenQueu.reverse()

    def Run_Pass(self):
        """runs through the token queu. Does syntax analysis and establishes where diffrent locations are"""
        nextToken = self.TokenQueu.pop() 
        while (len(self.TokenQueu) > 0) and (nextToken.type != "EOF"):
            try:
                if nextToken.type == "nl":
                    pass #pass by any newlines found
                elif nextToken.type == "var":
                    self.VAR(nextToken) #Reads a var
                elif nextToken.type == "ins":
                    self.INS(nextToken) #Reads a INS
                elif (nextToken.type == "g_addr") or (nextToken.type == "l_addr"):
                    self.ADDRESS(nextToken) #Reads a ADDRESS
            except ASSEMBLYERROR as AE: 
                self.ERRORS.append(AE)# adds an error to the error list
                self.PassLine()
            finally:
                nextToken = self.TokenQueu.pop()
    
    def peek(self):
        """peeks at the next token in line"""
        if len(self.TokenQueu) == 0:
            raise ASSEMBLYERROR("Unexpected End of File",0)
        Toke = self.TokenQueu[-1]
        if Toke.type == "var":
            return self.findvar(Toke) #Hot swap vars
        return Toke
    
    def dequeu(self):
        """Dequees the next token in line"""
        if len(self.TokenQueu) == 0:
            raise ASSEMBLYERROR("Unexpeced End of File",0)
        Toke = self.TokenQueu.pop()
        if Toke.type == "var":
            return self.findvar(Toke) #Hot swaps vars
        return Toke
    
    def findvar(self,var):
        """Finds a var or throws an ERROR"""
        if var.text not in self.VAR_TABLE.keys():
            raise ASSEMBLYERROR("Var not found",var.line)
        return self.VAR_TABLE[var.text]
    
    def PassLine(self):
        """Simply pushes on to a newline or EOF"""
        while True:
            if (self.TokenQueu[-1].type in ("EOF","nl")):
                break
            self.TokenQueu.pop()
    
    def VAR(self,Token):
        """Adds a var to the var Table"""
        nextToken = self.dequeu()
        if (nextToken.type in ["EOF","nl"]):
            raise ASSEMBLYERROR("Undefined Varible",Token.line)
        self.VAR_TABLE.update({Token.text:nextToken})
        if (self.TokenQueu[-1].type not in ["EOF","nl"]):
            raise ASSEMBLYERROR("Double diffened Var",Token.line)
        
    def INS(self,Token):
        #First establish if an instruction is in our instruction list
        if(Token.text not in self.INS_DIC.keys()):
            raise ASSEMBLYERROR("Cannot find Instruction "+Token.text,Token.line)
        #then fetch that instruction and create a new instruction object
        I = INSTRUCTION(Token.line,self.INS_DIC[Token.text],self.LOC)
        self.LOC += I.INS["SIZE"]#update the location
        OPRANDS = I.INS["OPRANDS"][1:]
        AT_END = False
        #Reads in oprands for somegiven instruction
        for ops in OPRANDS:
            if AT_END: #IF missing an oprand
                raise ASSEMBLYERROR("Missing a "+ops,Token.line)
            Token = self.dequeu()
            if Token.type == "comma": #if double comma
                raise ASSEMBLYERROR("Possible double comma",Token.line)
            if ops == "REG": #If a reg then get the number of that register
                if Token.text not in self.REGISTERS.keys():
                    raise ASSEMBLYERROR(Token.text +" is not a register",Token.line)
                I.Oprands.append(self.REGISTERS[Token.text])
            else:
                I.Oprands.append(Token) #otherwise its a value and just push in the next token
            if self.peek().type in ("EOF","nl"):
                AT_END = True
            if self.peek().type == "comma":
                self.dequeu() #Consumes the comma
        self.LINES.append(I)
        
    def ADDRESS(self,Token):
        """Reads in the location and offset of a ADDRESS"""
        self.LOCATION_TABLE.update({Token.text:self.LOC})
        MEMLINE = ADDRESS(Token.line,Token.text,self.LOC)
        if self.TokenQueu[-1].type in ("EOF","nl"): #IF just a address with no values just return
            self.LINES.append(MEMLINE)
            return
        Token = self.dequeu() #Otherwise attempt to get the memory type
        if Token.type != "ins":
            raise ASSEMBLYERROR("Expected memory type",Token.line)
        if Token.text == "ZERO": #IF zero add the zeros to the ADRESS ITEM then inc the location by that much
            Token = self.dequeu()
            if Token.type != "int":
                raise ASSEMBLYERROR("Expected Zero size to be an interger")
            self.LOC += TOOLS.str_to_int(Token.text)
            MEMLINE.Value = [0 for i in range(TOOLS.str_to_int(Token.text))]
            if self.TokenQueu[-1].type not in ("EOF","nl"):
                raise ASSEMBLYERROR("Extra value in zero decl")
            self.LINES.append(MEMLINE)
            return
        
        #Otherwise get the size of memory values
        if Token.text not in self.MEMORY_SIZES:
            raise ASSEMBLYERROR("Unrecognized memory type",Token.line)
        itemsize = self.MEMORY_SIZES[Token.text]
        MEMLINE.ItemSize = itemsize
        Token = self.dequeu()
        #then find the number of items and inc the LOCATION
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