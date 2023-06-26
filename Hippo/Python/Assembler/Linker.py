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

class linker:

    def __init__(self,files,entry_point = "@MAIN"):
        self.files = files
        self.entry_point = entry_point
        self.LOC = {}
        self.refs = []
        self.offset = 4
        self.code = [0,0,0,0]
        self.errors = []

    def link(self,output_file_name):
        for filename in self.files:
            with open(filename,'r') as OFILE:
                try:
                    self.readlink(json.load(OFILE))
                except KeyError as KE:
                    self.errors.append(LINKERROR("Malformed Header on file "+filename))
        for ref in self.refs:
            try:
                self.addValue(ref)
            except KeyError as KE:
                self.errors.append(LINKERROR("Malformed refrence header"+str(ref)))
            except LINKERROR as LE:
                self.errors.append(LE)
        if len(self.errors) != 0:
            for e in self.errors:
                print(e)
                return
        with open(output_file_name,'wb') as HEXFILE:
            entryaddr = self.LOC[self.entry_point]
            JMP = [0x50,0] + TOOLS.S16_to_bytes(entryaddr)
            for i in range(4):
                self.code[i] = JMP[i]
            for b in self.code:
                HEXFILE.write(b.to_bytes())

    def addValue(self,value):
        val = 0
        if value["type"] == "off":
            if value["name"] not in self.LOC.keys():
                raise LINKERROR("Cannot find symbol "+value["name"])
            val = self.LOC.keys() - value["baseloc"]
        if value["size"] == 2:
            valbytes = TOOLS.S16_to_bytes(val)
            self.code[value["loc"]] = valbytes[0]
            self.code[value["loc"] + 1] = valbytes[1]
        elif value["size"] == 3:
            valbytes = TOOLS.S24_to_bytes(val)
            self.code[value["loc"]] = valbytes[0]
            self.code[value["loc"] + 1] = valbytes[1]
            self.code[value["loc"] + 2] = valbytes[2]


    def readlink(self,link):
        for keys in link["LOCS"].keys():
            link["LOCS"][keys] += self.offset
        for items in link["REFS"]:
            items["loc"] += self.offset
            items["baseloc"] += self.offset
        self.offset += link["CODESIZE"]
        self.LOC.update(link["LOCS"])
        self.refs += link["REFS"]
        self.code += link["CODE"]

    
