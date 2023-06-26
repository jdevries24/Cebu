from Tools import *
import json

class LINKERROR(Exception):

    def __init__(self,message):
        self.message = message

class AssemblyOutput:

    def __init__(self,GlobalTable,RefLocs,Lines):
        self.GlobalTable = GlobalTable
        self.RefLocs = RefLocs
        self.Lines = Lines
    
    def output_debug_file(self,ASMText,FileName):
        with open(FileName,'w') as DB:
            DB.write("OFFSET       Line\n")
            textlines = ASMText.split('\n')
            for l in self.Lines:
                if l.Type == "ADDR":
                    DB.write("             "+textlines[l.line]+'\n')
                else:
                    DB.write(TOOLS.OUTHEX(l.LOC,6) + " "+TOOLS.OUTHEX(l.Value[0]) + " " + TOOLS.OUTHEX(l.Value[1]) + " " + textlines[l.line] +"\n")
                    if len(l.Value) == 4:
                        DB.write("       "+TOOLS.OUTHEX(l.Value[2]) + " " + TOOLS.OUTHEX(l.Value[3])+"\n")
    
    def output_hex_file(self,FileName):
        with open(FileName,'wb') as HEX:
            for l in self.Lines:
                for b in l.Value:
                    HEX.write(b.to_bytes())

    def output_link(self,FileName):
        with open(FileName,'w') as JFILE:
            code = []
            for l in self.Lines:
                code += l.Value
            codesize = len(code)
            json.dump({"LOCS":self.GlobalTable,"REFS":self.RefLocs,"CODESIZE":codesize,"CODE":code},JFILE,indent = 4)
    
