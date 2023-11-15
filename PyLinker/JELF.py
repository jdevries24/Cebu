from elftools.elf.elffile import ELFFile
from Dissasembler import Dissasembler
class JSYMBOL:

    def __init__(self,name,section,offset):
        self.name = name
        self.section = section
        self.offset = offset

    def __str__(self):
        return " : ".join([str(self.name),str(self.section),str(self.offset)])

class JRELOC:

    def __init__(self,name,Stype,section,offset):
        self.name = name
        self.type = "JRISC_S24"
        if Stype == 2:
            self.type = "JRISC_S20"
        if Stype == 3:
            self.type = "JRISC_U32"
        self.section = section
        self.offset = offset

    def __str__(self):
        return " : ".join([str(self.name),str(self.type),str(self.section),str(self.offset)])
        

class JELF:

    def __init__(self,stream):
        self.elf = ELFFile(stream)
        self._build_st()
        self._build_rlocs()
        
    def dump_syms(self):
        for v in self.st.values():
            print(v)
    
    def dump_relocs(self):
        for v in self.rl:
            print(v)

    def _build_st(self):
        self.st = {}
        symt = self.elf.get_section_by_name(".symtab")
        for s in symt.iter_symbols():
            if s.name == "":continue
            if (type(s.entry.st_shndx) == int):
                self.st.update({s.name:JSYMBOL(s.name,self.elf.get_section(s.entry.st_shndx).name,s.entry.st_value)})
    
    def decompile(self):
        dcst = {}
        for name,value in self.st.items():
            if value.section == ".text":
                dcst.update({value.offset:value.name})
        d = Dissasembler(list(self.elf.get_section_by_name(".text").data()),dcst,None)
        print(d.output())


    def _build_rlocs(self):
        self.rl = []
        for s in self.elf.iter_sections():
            if len(s.name) < 4:continue
            if s.name[:4] == ".rel":
                self._get_rlocs(s)

    def _get_rlocs(self,section):
        symt = self.elf.get_section_by_name(".symtab")
        for r in section.iter_relocations():
            sm = symt.get_symbol(r.entry.r_info_sym)
            #print(r.entry)
            #print(sm.entry)
            self.rl.append(JRELOC(sm.name,
            r.entry.r_info_type,section.name[4:],r.entry.r_offset))
            

def test():
    with open("test.o",'rb') as OBJF:
        elf = JELF(OBJF)
        elf.decompile()
        

if __name__ == "__main__":
    test()