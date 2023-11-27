from Tools import *
from tokenizer import tokenizer
from Dissasembler import Dissasembler
import argparse
from J import readJSON

_JSONf = "/home/jdevries/Cebu/ASM/JRISCins.json"
class Assembler:

    def __init__(self,files):
        self.ins,self.registers,self.memSizes = readJSON(_JSONf)
        self.files = files
        self.vars = {}
        self.tokenLists = {}
        self.globalSyms = {}
        self.localSyms = {}
        self.offset = 0
        self.workingFile = ""
        self.items = []
        self.atData = False
        self.tokenQueu = []
        self.insCallbacks = {
            "O":self.v_O,
            "RR":self.v_RR,
            "RRI":self.v_RRI,
            "I":self.v_I,
            "RI":self.v_RI,
            "R":self.v_R,
            "IN":self.v_IN,
        }
        self.imFixes = {
            "S16":self.v_S16,
            "U16":self.v_U16,
            "S20":self.v_S20,
            "S24":self.v_S24,
            "U24":self.v_U24
        }
        self.errors = []

    def outputHex(self,filename):
        if(len(self.errors) != 0):return
        with open(filename,"wb") as hexfile:
            for item in self.items:
                for v in item.value:
                    hexfile.write(v.to_bytes(1,'big'))

    def DumpDissasemble(self):
        if(len(self.errors) != 0):return
        code = []
        for item in self.items:
            if item.type == "ins":
                code += item.value
            else:
                break
        st = {}
        for key,item in self.globalSyms.items():
            if(item not in st.keys()):
                st.update({item:key})
        for ps in self.localSyms.values():
            for key,item in ps.items():
                if(item not in st.keys()):
                    st.update({item:key})
        diss = Dissasembler(code,st,{})
        print(diss.output())


    def Run(self,entry = "@MAIN"):        
        tkn = tokenizer("JMP "+entry.upper())
        tokens = tkn.tokenize()
        tokens.reverse()
        self.tokenQueu = tokens
        self.parseINS()
        for file in self.files:
            tokens = []
            with open(file,"r") as TF:
                self.workingFile = file
                self.localSyms.update({file:{}})
                tkn = tokenizer(TF.read())
                tokens = tkn.tokenize()
                tokens.reverse()
                self.tokenLists.update({file:tokens[:]})
                self.tokenQueu = self.tokenLists[file]
                self.parseINS()
                self.atData = False
        for file,queu in self.tokenLists.items():
            self.workingFile = file
            self.tokenQueu = queu
            self.parseINS()
            self.atData = False
        for item in self.items:
            try:
                if(item.type == "ins"):
                    if(item.imType == "N"):
                        continue
                    self.imFixes[item.imType](item)
                if(item.type == "addr"):
                    self.relaxMem(item)
            except ASSEMBLYERROR as AE:
                self.errors.append(AE)
        if len(self.errors) != 0:
            self.reportErrors()


    def findVar(self,var):
        if(var.text not in self.vars.keys()):
            raise ASSEMBLYERROR("Cannot find var "+var.text,var.line,self.workingFile)
        else:
            return self.vars[var.text]

    def peek(self):
        if(len(self.tokenQueu) == 0):
            raise ASSEMBLYERROR("unexpected eof",0,self.workingFile)
        tok = self.tokenQueu[-1]
        if tok.type == "var":
            return self.findVar(tok)
        return tok
    
    def pop(self):
        if(len(self.tokenQueu) == 0):
            raise ASSEMBLYERROR("unexpected eof",0,self.workingFile)
        tok = self.tokenQueu.pop()
        if tok.type == "var":
            return self.findVar(tok)
        return tok

    def parseINS(self):
        if(len(self.tokenQueu) == 0):return
        nextToken = self.tokenQueu.pop()
        while(len(self.tokenQueu) != 0) and (nextToken.type != "EOF") and not self.atData:
            try:
                if nextToken.type == "var":
                    self.v_Var(nextToken)
                elif nextToken.type == "ins":
                    if(nextToken.text in self.memSizes.keys()):
                        self.v_MEM(nextToken)
                    elif(nextToken.text in self.ins.keys()):
                        info = self.ins[nextToken.text]
                        self.insCallbacks[info["F_code"]](nextToken)
                    elif(nextToken.text == "ZERO"):
                        self.v_Zero(nextToken)
                    else:
                        self.errors.append(ASSEMBLYERROR("Instruction not found!",nextToken.line,self.workingFile))
                        while True:
                            if(self.peek().type in ("EOF","nl")):
                                break
                            self.pop()
                elif nextToken.type in ("l_addr","g_addr"):
                    self.v_Addr(nextToken)
                elif nextToken.type == "nl":
                    pass
            except ASSEMBLYERROR as AE:
                self.errors.append(AE)
                while True:
                    if(self.peek().type in ("EOF","nl")):
                        break
                    self.pop()
            if(len(self.tokenQueu) != 0):
                nextToken = self.tokenQueu.pop()

                



###################################################
##########Section dedicated to first pass########## 
###################################################

    def getRegister(self,Token):
        if(Token.text not in self.registers.keys()):
            raise ASSEMBLYERROR("No register "+Token.text,Token.line,self.workingFile)
        return self.registers[Token.text]

    def v_Addr(self,Token):
        if(Token.type == "g_addr"):
            if(Token.text in self.globalSyms.keys()):
                raise ASSEMBLYERROR("Double def of symbol",Token.line,self.workingFile)
            self.globalSyms.update({Token.text:self.offset})
        if(Token.type == "l_addr"):
            l_table = self.localSyms[self.workingFile]
            if(Token.text in l_table.keys()):
                raise ASSEMBLYERROR("Double def of symbol",Token.line,self.workingFile)
            l_table.update({Token.text:self.offset})

    def v_Var(self,Token):
        if(Token.text == "$DATA"):
            self.atData = True
            return
        else:
            nextToken = self.tokenQueu.pop()
            self.vars.update({Token.text:nextToken})
    
    def v_O(self,Token):
        opcode = int(self.ins[Token.text]["OPCODE"],16)
        self.items.append(INSTRUCTION(self.workingFile,
                                      Token.line,
                                      [opcode,0],
                                      "N",
                                      self.offset)) 
        self.offset += 2

    def v_RR(self,Token):
        ins = self.ins[Token.text]
        opcode = int(ins["OPCODE"],16)
        src = self.getRegister(self.pop())
        if(self.pop().type != "comma"):
            raise ASSEMBLYERROR("missing comma",Token.line,self.workingFile)
        dest = self.getRegister(self.pop())
        srcDest = (src << 4) | dest
        self.items.append(INSTRUCTION(self.workingFile,
                                      Token.line,
                                      [opcode,srcDest],
                                      "N",
                                      self.offset))
        self.offset += 2

    def v_RRI(self,Token):
        ins = self.ins[Token.text]
        opcode = int(ins["OPCODE"],16)
        src = self.getRegister(self.pop())
        if(self.pop().type != "comma"):
            raise ASSEMBLYERROR("missing comma",Token.line,self.workingFile)
        dest = self.getRegister(self.pop())
        srcDest = (src << 4) | dest
        if(self.pop().type != "comma"):
            raise ASSEMBLYERROR("missing comma",Token.line,self.workingFile)
        imm = self.pop()
        if(imm.type in ("EOF","nl")):
            raise ASSEMBLYERROR("missing imm",Token.lineNo,self.workingFile)
        self.items.append(INSTRUCTION(self.workingFile,
                                      Token.line,
                                      [opcode,srcDest,0,0],
                                      ins["Im_Type"],
                                      self.offset,
                                      imm))
        self.offset += 4

    def v_I(self,Token):
        ins = self.ins[Token.text]
        opcode = int(ins["OPCODE"],16)
        imm = self.pop()
        if(imm.type in ("EOF","nl")):
            raise ASSEMBLYERROR("missing imm",Token.lineNo,self.workingFile)
        self.items.append(INSTRUCTION(self.workingFile,
                                      Token.line,
                                      [opcode,0,0,0],
                                      ins["Im_Type"],
                                      self.offset,
                                      imm))
        self.offset += 4


    def v_RI(self,Token):
        ins = self.ins[Token.text]
        opcode = int(ins["OPCODE"],16)
        src = self.getRegister(self.pop()) << 4
        if(self.pop().type != "comma"):raise ASSEMBLYERROR("expected comma",Token.line,self.workingFile)
        imm = self.pop()
        if(imm.type in ("EOF","nl")):
            raise ASSEMBLYERROR("Missing Im",Token.line,self.workingFile)
        self.items.append(INSTRUCTION(self.workingFile,
                                      Token.line,
                                      [opcode,src,0,0],
                                      ins["Im_Type"],
                                      self.offset,
                                      imm))
        self.offset += 4
        

    def v_R(self,Token):
        pass

    def v_IN(self,Token):
        opcode = 0xc0
        im = self.pop()
        if(im.type != "int"):
            raise ASSEMBLYERROR("Inproper inturupt value",Token.text,self.workingFile)
        imm = TOOLS.strToInt(im.text)
        if (imm > 255) or (imm < 0):
            message = "Int to large" if imm > 255 else "Int to small"
            raise ASSEMBLYERROR(message,Token.text,self.workingFile)
        self.items.append(INSTRUCTION(self.workingFile,
                                      Token.line,
                                      [opcode,imm],
                                      "N",
                                      self.offset))
        self.offset += 2

    def v_MEM(self,Token):
        size = self.memSizes[Token.text]
        ops = []
        nextToken = self.pop()
        while(nextToken.type not in("EOF","nl")):
            if(nextToken.type == "comma"):
                nextToken = self.pop()
                continue
            elif(nextToken.type == "int"):
                ops.append(TOOLS.strToInt(nextToken.text))
            elif(nextToken.type == "str"):
                for c in nextToken.text:
                    ops.append(ord(c))
            else:
                ops.append(nextToken)
            nextToken = self.pop()
        self.items.append(Memory(self.workingFile,Token.line,ops,size,self.offset))
        self.offset += len(ops) * size

    def v_Zero(self,Token):
        imm = self.pop()
        if imm.type != "int":
            raise ASSEMBLYERROR("non int zero size",Token.line,self.workingFile)
        imm = TOOLS.strToInt(imm.text)
        self.items.append(Memory(self.workingFile,Token.line,[0 for i in range(imm)],1,self.offset))
        self.offset += imm

###################################################
#########Section dedicated to secound pass######### 
###################################################

    def getSym(self,item,subLoc = True):
        if(item.type == "ins"):
            if(item.im.type == "g_addr"):
                if(item.im.text not in self.globalSyms.keys()):
                    raise ASSEMBLYERROR("cannot find symbol",item.lineNo,item.file)
                return self.globalSyms[item.im.text] - item.loc
            elif(item.im.type == "l_addr"):
                l_syms = self.localSyms[item.file]
                if(item.im.text not in l_syms.keys()):
                    raise ASSEMBLYERROR("cannot_find_symbol",item.lineNo,item.file)
                return l_syms[item.im.text] - item.loc
            elif(item.im.type == "int"):
                return TOOLS.strToInt(item.im.text)
            else:
                raise ASSEMBLYERROR("Value not valid",item.lineNo,item.file)
            
    def checkRange(self,item,val,min,max):
        if val < min:
            raise ASSEMBLYERROR("symbol to small",item.lineNo,item.file)
        if val > max:
            raise ASSEMBLYERROR("symbol to large",item.lineNo,item.file)
        
    def v_S16(self,item):
        val = self.getSym(item)
        self.checkRange(item,val,-0x7fff,0x7fff)
        if val < 0:
            val = (val * -1) | 0x8000
        val = TOOLS.to_bytes(val,2)
        item.value[2] = val[0]
        item.value[3] = val[1]

    def v_U16(self,item):
        val = self.getSym(item)
        self.checkRange(item,val,0,0xffff)
        val = TOOLS.to_bytes(val,2)
        item.value[2] = val[0]
        item.value[3] = val[1]

    def v_S24(self,item):
        val = self.getSym(item)
        self.checkRange(item,val,-0x7fffff,0x7fffff)
        if val < 0:
            val = (val * -1) | 0x800000
        val = TOOLS.to_bytes(val,3)
        item.value[1] = val[0]
        item.value[2] = val[1]
        item.value[3] = val[2]

    def v_S20(self,item):
        val = self.getSym(item)
        self.checkRange(item,val,-0x7ffff,0x7ffff)
        if val < 0:
            val = (val * -1) | 0x80000
        val = TOOLS.to_bytes(val,3)
        item.value[1] |= val[0]
        item.value[2] |= val[1]
        item.value[3] |= val[2]

    def v_U24(self):
        pass

    def reportErrors(self):
        fileInfo = {}
        for E in self.errors:
            if E.file not in fileInfo.keys():
                with open(E.file,'r') as F:
                    fileInfo.update({E.file:F.read().split('\n')})
            print("Error in",E.file,"Line Number",E.lineNo + 1)
            print(' ',fileInfo[E.file][E.lineNo])
            print(E.message,'\n')

    def relaxMem(self,mem):
        new_val = []
        for loc,v in enumerate(mem.oprands):
            if(type(v) == int):
                mem.value += TOOLS.to_bytes(v,mem.size,True)


if __name__ == "__main__":

    def test():
        #asm = Assembler(["JSTD.s","stack.s","stacktest.s"])
        asm = Assembler(["JSTD.s","test.s"])
        asm.Run()
        asm.outputHex("test.hex")
        asm.DumpDissasemble()

    def run():
        parser = argparse.ArgumentParser(description = "JRISC assembly assembler")
        parser.add_argument('files',nargs="+")
        parser.add_argument("-o",nargs="?",default="a.hex")
        parser.add_argument("-d",nargs="?")
        parser.add_argument("-e",nargs="?",default = "@MAIN")
        args = parser.parse_args()
        asm = Assembler(args.files)
        asm.Run(args.e)
        asm.outputHex(args.o)
        if args.d != None:
            asm.DumpDissasemble()


    run()
