class INSTRUCTION:

    def __init__(self,file,lineNo,value,imType,loc,im = ""):
        self.type = "ins"
        self.file = file
        self.lineNo = lineNo
        self.value = value
        self.imType = imType
        self.loc =loc
        self.im = im

class Memory:

    def __init__(self,file,lineNo,oprands,size,loc):
        self.type = "addr"
        self.file = file
        self.lineNo = lineNo
        self.size = size
        self.oprands = oprands
        self.loc = loc 
        self.value = []
    

class ASSEMBLYERROR(Exception):

    def __init__(self,message,lineNo,file = "unkown"):
        self.message = message
        self.lineNo = lineNo
        self.file = file

class TOOLS:
    
    def strToInt(istr):
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