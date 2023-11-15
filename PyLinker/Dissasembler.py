from InsLookup import *

class Instruction:
    def __init__(self,size,opcode,mem,regs,imm = None):
        self.opcode = opcode
        self.size = size
        self.mem = mem
        self.regs = regs
        self.imm = imm

    def __str__(self):
        st = " ".join([str(self.mem),str(self.regs)])
        if(self.imm != None):
            return st +("," if self.regs != "" else "")+ str(self.imm)
        else:
            return st

class Dissasembler:

    def __init__(self,text,st,rc):
        self.text = text
        self.st = st
        self.rc = rc
        self.pc = 0
        self.Instructions = []
        self.__firstpass()

    def output(self):
        lines = []
        self.pc = 0
        for I in self.Instructions:
            if self.pc in self.st.keys():
                lines.append(self._output_sym(self.st[self.pc]))
            lines.append('\t' + self._output_INS(I))
        return "\n".join(lines)

    def _output_INS(self,I):
        I_Str = I.mem
        if I.regs != "":
            I_Str += " " + I.regs
        if I.imm != None:
            I_Str += "," if I.regs != "" else " "
            if(I.opcode in pcRelitive):
                I_Str += self._get_offset(I.imm)
            else:
                I_Str += str(I.imm)
        self.pc += I.size
        return I_Str
    
    def _get_offset(self,imm):
        if imm == 0:return "0"
        loc = self.pc + imm
        if loc in self.st.keys():
            return self.st[loc]
        return str(imm)

    def _output_sym(self,sym):
        if sym[0] == ".":
            return sym
        else:
            return "@" + sym

    def __firstpass(self):
        maxi = len(self.text)
        while(self.pc < maxi):
            self._decode()

    def _decode(self):
        opcode = self.text[self.pc]
        INS_type = formatTypes[opcode]
        if INS_type == RR:
            self._decode_RR(opcode)
        elif INS_type == RRI:
            self._decode_RRI(opcode)
        elif INS_type == I:
            self._decode_I(opcode)
        else:
            if immTypes[opcode] in (U8,N):
                self.Instructions.append(Instruction(2,opcode,mems[opcode],""))
                self.pc += 2
            else:
                self.Instructions.append(Instruction(4,opcode,mems[opcode],""))
                self.pc += 4


    def _decode_RR(self,opcode):
        regs = self._decode_register_pair()
        self.Instructions.append(Instruction(2,opcode,mems[opcode],regs))
        self.pc += 2

    def _decode_RRI(self,opcode):
        regs = self._decode_register_pair()
        IMM = (int(self.text[self.pc + 2]) << 8) + (int(self.text[self.pc + 3]))
        if(immTypes[opcode] == S16):
            if(IMM >= 0x8000):
                IMM = (IMM & 0x7fff) * -1
        self.Instructions.append(Instruction(4,opcode,mems[opcode],regs,IMM))
        self.pc += 4

    def _decode_I(self,opcode):
        IMM = (int(self.text[self.pc + 1]) << 16) + (int(self.text[self.pc + 2]) << 8) + (int(self.text[self.pc + 3]))
        if(immTypes[opcode] == S24):
            if(IMM >= 0x800000):
                IMM = (IMM & 0x7fffff) * -1
            self.Instructions.append(Instruction(4,opcode,mems[opcode],"",IMM))
            self.pc += 4

    def _decode_register_pair(self):
        pairbyte = self.text[self.pc+1]
        SRC = Reg_lookup[(pairbyte >> 4) & 0xf]
        DEST = Reg_lookup[(pairbyte & 0xf)]
        return ",".join([SRC,DEST])