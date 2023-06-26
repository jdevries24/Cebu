from tokenizer import *
from FirstPass import *
from secoundpass import secound_pass
from Linker import *
import json

if __name__ == "__main__":

    def run():
        ASM_INFO = {}
        with open("ASM.json") as ASM_INFO_FILE:
            ASM_INFO = json.load(ASM_INFO_FILE)
        with open("test.s") as ASM_FILE:
            tz = tokenizer(ASM_FILE.read())
            tokens = tz.tokenize()
            pass1 = FirstPass(tokens[:],ASM_INFO)
            pass1.Run_Pass()
            for L in pass1.LINES:
                print(L)
            print(pass1.LOCATION_TABLE)
            pass2 = secound_pass(pass1.LINES,pass1.LOCATION_TABLE)
            pass2.run()
            ERRORS = pass1.ERRORS + pass2.ERRORS
            if len(ERRORS) != 0:
                ASM_FILE.seek(0)
                lines = ASM_FILE.read().split('\n')
                for E in ERRORS:
                    print("Error on line",str(E.line + 1) + ":",E.message)
                    print("   ",lines[E.line])
            if len(ERRORS) == 0:
                OUT = AssemblyOutput(pass2.GlobalLocs,pass2.Reflocations,pass2.lines)
                ASM_FILE.seek(0)
                OUT.output_debug_file(ASM_FILE.read(),"test.d")
                OUT.output_hex_file("test.hex")
                OUT.output_link("test.json")
    
    run()


    

