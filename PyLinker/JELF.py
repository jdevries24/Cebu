from elftools.elf.elffile import ELFFile
from Dissasembler import Dissasembler

class JRLOC:
    def __init__(self,homeSection,rloc,sym):
        self.homeSection = homeSection
        self.rloc = rloc
        self.sym = sym

    def __str__(self):
        return "{ section:"+str(self.homeSection) + ",\nrloc:" + str(self.rloc) + ",\nsym: " + str(self.sym) + "}"

class JELF:

    def __init__(self,stream):
        self.elf = ELFFile(stream)
        self._build_st()
        self._build_rlocs()
        

    def _build_st(self):
        self.st = {}
        symt = self.elf.get_section_by_name(".symtab")
        for s in symt.iter_symbols():
            if s.name == "":continue
            if (type(s.entry.st_shndx) == int):
                self.st.update({s.name:s.entry})
    
    def decompile(self):
        dcst = {}
        dcrt = {}
        symt = self.elf.get_section_by_name(".symtab")
        text_index = self.elf.get_section_index(".text")
        for name,value in self.st.items():
            if(value.st_shndx == text_index):
                dcst.update({value.st_value:name})
        for val in self.rl:
            if(val.homeSection != text_index):continue
            if(val.sym.st_info.type == "STT_SECTION"):continue
            dcrt.update({val.rloc.r_offset:symt.get_symbol(val.rloc.r_info_sym).name})
        d = Dissasembler(list(self.elf.get_section_by_name(".text").data()),dcst,dcrt)
        print(d.output())


    def _build_rlocs(self):
        self.rl = []
        for s in self.elf.iter_sections():
            if len(s.name) < 4:continue
            if s.name[:4] == ".rel":
                continue
            rloc_section = self.elf.get_section_by_name(".rel" + s.name)
            if(rloc_section != None):
                self._get_rlocs(rloc_section,s)

    def _get_rlocs(self,rel_section,section):
        symt = self.elf.get_section_by_name(".symtab")
        homeIndex = self.elf.get_section_index(section.name)
        for r in rel_section.iter_relocations():
            sm = symt.get_symbol(r.entry.r_info_sym).entry
            self.rl.append(JRLOC(homeIndex,r.entry,sm))
            

def test():
    with open("test.o",'rb') as OBJF:
        elf = JELF(OBJF)
        elf.decompile()
        

if __name__ == "__main__":
    test()