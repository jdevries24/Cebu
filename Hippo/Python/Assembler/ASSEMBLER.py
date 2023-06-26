from tokenizer import *
from FirstPass import *
from secoundpass import secound_pass
from Linker import *
import json
import argparse

if __name__ == "__main__":

    def run(input_file,output_types,output_file):
        ASM_INFO = {}
        with open("ASM.json") as ASM_INFO_FILE:
            ASM_INFO = json.load(ASM_INFO_FILE)
        with open(input_file) as ASM_FILE:
            tz = tokenizer(ASM_FILE.read())
            tokens = tz.tokenize()
            pass1 = FirstPass(tokens[:],ASM_INFO)
            pass1.Run_Pass()
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
                outname = output_file.split(".")[0]
                outputer = AssemblyOutput(pass2.GlobalLocs,pass2.Reflocations,pass2.lines)
                if "d" in output_types:
                    ASM_FILE.seek(0)
                    outputer.output_debug_file(ASM_FILE.read(),outname + ".d")
                if "o" in output_types:
                    outputer.output_link(outname+".o")
                if "h" in output_types:
                    outputer.output_hex_file(outname+".hex")
    
    def runLinker(infile,outfile):
        l = linker([infile])
        l.link(outfile)

    run("test.s",["d","o"],"test")
    runLinker("test.o","test.hex")


    

