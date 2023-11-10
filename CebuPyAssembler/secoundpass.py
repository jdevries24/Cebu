from Tools import *

class secound_pass:

    def __init__(self,lines,LocationTable):
        self.lines = lines
        self.GlobalLocs = {}
        self.Reflocations = []
        self.ERRORS = []
        self.LocationTable = LocationTable
        self.typeops = {
            "SRC_DEST":self.SRC_DEST,
            "SRC_DEST_JMP":self.SRC_DEST_OFFSET,
            "SRC_DEST_OFFSET":self.SRC_DEST_OFFSET,
            "SRC_DEST_IM":self.SRC_DEST_IM,
            "SINGLE":self.SINGLE,
            "SRC":self.SRC,
            "DEST":self.DEST,
            "BYTE":self.BYTE,
            "DEST_OFFSET":self.DEST_OFFSET,
            "JMP":self.JMP,
            "CAL":self.CAL
        }

    def run(self):
        #To pass just go thorugh the INSTRUCTION and MEMORY structs
        for l in self.lines:
            try:
                if l.Type == "ADDR":
                    self.ReadMemory(l)
                else:
                    self.readIns(l)
            except ASSEMBLYERROR as AE:
                self.ERRORS.append(AE)

    def ReadMemory(self,memory_line):
        if memory_line.Name[0] == "@":
            self.GlobalLocs.update({memory_line.Name:memory_line.LOC}) #IF a global location track it for linking reasons
        for op in memory_line.Oprands:
            if op.type == "str": #If reading a string add all the chars to memory
                for chr in op.text:
                    memory_line.Value += TOOLS.to_bytes(ord(chr),memory_line.ItemSize)
            elif op.type == "int":#if int just add the value
                v = TOOLS.str_to_int(op.text)
                memory_line.Value += TOOLS.to_bytes(v,memory_line.ItemSize,v < 0)
            elif op.type == "g_addr": #IF an global address find the location or add to reflocation table
                if op.text in self.LocationTable:
                    memory_line.Value += TOOLS.to_bytes(self.LocationTable[op.text],memory_line.ItemSize)
                else:
                    self.Reflocations.append({
                        "type":"abs",
                        "size":memory_line.ItemSize,
                        "loc":memory_line.LOC + len(memory_line.Value),
                        "baseloc":memory_line.LOC
                    })
            elif op.type == "l_addr": #Loads the location. if a local address that must be in the location table
                if op.text not in self.LocationTable:
                    raise ASSEMBLYERROR("Location not Found",memory_line.line)
                memory_line.Value += TOOLS.to_bytes(self.LocationTable[op.text],memory_line.ItemSize)

    def ReadOffset(self,LOC,memoryToke,Offsetsize = 2):
        #Takes in a base location and a memorytoken then attempts to find the +- diffrence and returns the value. Otherwise adds to reflocation list
        if memoryToke.text in self.LocationTable:
            memoryLOC = self.LocationTable[memoryToke.text]
            return memoryLOC - LOC
        elif memoryToke.type == "l_addr":
            raise ASSEMBLYERROR("Location not Found",memoryToke.line)
        elif memoryToke.type == "g_addr":
            self.Reflocations.append({
                "name":memoryToke.text,
                "type":"off",
                "size":Offsetsize,
                "loc":LOC + (4 - Offsetsize),
                "baseloc":LOC
            })
            return 0
        
    def readValue(self,Token,LOC,Offsetsize = 2):
        #Some oprands will still be value this attempts to read values in
        if Token.type == "int":
            return TOOLS.str_to_int(Token.text)
        elif Token.type in ("g_addr","l_addr"):
            return self.ReadOffset(LOC,Token,Offsetsize)
        elif Token.type == "str":
            if Token.text > 1:
                schar = {"\\n":0xa,"\\b":0x8}
                if Token.text in schar.keys():
                    return schar[Token.text]
                raise ASSEMBLYERROR("Only Chars can be values",Token.line)
            if Token.text == "": return 0
            return ord(Token.text[0])
        else:
            raise ASSEMBLYERROR("Invalid Value",Token.line)
        
    def readIns(self,I):
        #Generic switch for diffrent types of instructions
        Itype = I.INS["TYPE"]
        self.typeops[Itype](I)

    def SINGLE(self,I):
        """Instruction by itself"""
        opcode = int(I.INS["OPCODE"],16)
        I.Value = [opcode,0] 
    
    def SRC(self,I):
        """Instruction that only defines a source"""
        opcode = int(I.INS["OPCODE"],16)
        I.Value = [opcode,I.Oprands[0] << 4]

    def DEST(self,I):
        """Instruction that only defines a Dest"""
        opcode = int(I.INS["OPCODE"],16)
        I.Value = [opcode,I.Oprands[0]]

    def DEST_OFFSET(self,I):
        """Basicly just Load Effective address"""
        opcode = int(I.INS["OPCODE"],16)
        offset = self.readValue(I.Oprands[1],I.LOC)
        if abs(offset) > 0x8000:
            raise ASSEMBLYERROR("OFFSET to large",I.line)
        I.Value = [opcode,I.Oprands[0]] + TOOLS.S16_to_bytes(offset)

    def BYTE(self,I):
        """Instruction with a byte opprand only for interupts"""
        opcode = int(I.INS["OPCODE"],16)
        IM = self.readValue(I.Oprands[0],I.LOC,1)
        if(IM < 0) or (IM > 255):
            raise ASSEMBLYERROR("Inturupts can only be a byte")
        I.Value = [opcode,IM]
        
    def SRC_DEST(self,I):
        """Instruction with a source dest oprands"""
        opcode = int(I.INS["OPCODE"],16)
        srcdest = (I.Oprands[0] << 4) | (I.Oprands[1])
        I.Value = [opcode,srcdest]

    def SRC_DEST_OFFSET(self,I):
        """Instructions with a source and dest register and a offset"""
        opcode = int(I.INS["OPCODE"],16)
        srcdest = (I.Oprands[0] << 4) | (I.Oprands[1])
        offset = self.readValue(I.Oprands[2],I.LOC)
        if abs(offset) > 0x8000:
            raise ASSEMBLYERROR("OFFSET too large",I.line)
        I.Value = [opcode,srcdest] + TOOLS.S16_to_bytes(offset)
    
    def JMP(self,I):
        """Raw JMP instruction"""
        opcode = int(I.INS["OPCODE"],16)
        offset = self.readValue(I.Oprands[0],I.LOC)
        if abs(offset) > 0x8000:
            raise ASSEMBLYERROR("OFFSET too large",I.line)
        I.Value = [opcode,0] + TOOLS.S16_to_bytes(offset)

    def SRC_DEST_IM(self,I):
        """A source and DEST register and Immediate value"""
        opcode = int(I.INS["OPCODE"],16)
        srcdest = (I.Oprands[0] << 4) | (I.Oprands[1])
        offset = self.readValue(I.Oprands[2],I.LOC)
        if offset > 0xFFFF:
            raise ASSEMBLYERROR("Immidate too large",I.line)
        if offset < 0:
            raise ASSEMBLYERROR("Immidate cannot be negitive",I.line)
        I.Value = [opcode,srcdest] + TOOLS.U16_to_bytes(offset)

    def CAL(self,I):
        """calls a 24 bit offset"""
        opcode = int(I.INS["OPCODE"],16)
        offset = self.readValue(I.Oprands[0],I.LOC,3)
        if abs(offset) > 0x800000:
            raise ASSEMBLYERROR("OFFSET too large",I.line)
        I.Value = [opcode] + TOOLS.S24_to_bytes(offset)
    