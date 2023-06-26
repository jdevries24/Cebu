class INSTRUCTION:

    def __init__(self,line,INS,LOC):
        self.Type = "INS"
        self.line = line
        self.LOC = LOC
        self.INS = INS
        self.Oprands = []
        self.Value = []

    def __str__(self):
        return str(self.INS["MEM"]) + " [" + ",".join([str(O) for O in self.Oprands]) + "]"

class ADDRESS:

    def __init__(self,line,Name,LOC):
        self.Type = "ADDR"
        self.line = line
        self.Name = Name
        self.LOC = LOC
        self.ItemSize = 0
        self.Oprands = []
        self.Value = []
    
    def __str__(self):
        return str(self.Name) + " [" + ",".join([str(O) for O in self.Oprands]) + "]"

class ASSEMBLYERROR(Exception):

    def __init__(self,message,line):
        self.message = message
        self.line = line

class TOOLS:

    def OUTHEX(num,size = 2):
        hexval = hex(num)[2:]
        for i in range(size - len(hexval)):
            hexval = "0" + hexval
        return hexval[:size].upper()
    
    def U16_to_bytes(number):
        O1 = (number >> 8) & 0xff
        O2 = number & 0xff
        return [O1,O2]

    def S16_to_bytes(number):
        if number < 0:
            number = (number * -1) | 0x8000
        return TOOLS.U16_to_bytes(number) 
    
    def S24_to_bytes(number):
        if number < 0:
            number = (number * -1) | 0x800000
        O1 = (number >> 16) & 0xff
        O2 = (number >> 8) & 0xff
        O3 = number & 0xff
        return [O1,O2,O3] 
    
    
    def str_to_int(istr):
        if len(istr) < 2:
            return int(istr)
        if istr[:2] == "0X":
            return int(istr[2:],16)
        elif istr[:2] == "0B":
            return int(istr[2:],2)
        else:
            return int(istr,10)
        
    def to_bytes(number,size,signed = False):
        byte_list = number.to_bytes(size,signed = signed,byteorder="big")
        return [int(b) for b in byte_list]