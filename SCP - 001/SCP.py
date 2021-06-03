from lex import *
from parse import * 
from emit import *
import sys
import os
os.system("color")

def main():
    print (colored.CYAN("||SCP - 001 : Simple Compiler Program||"))
    if len (sys.argv) != 2:
        sys.exit(colored.RED("ERROR:") + " Compiler needs source file as argument.")
    with open (sys.argv[1],'r') as inputFile:
        input = inputFile.read()
        
    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer,emitter)
    
    parser.program(sys.argv[1])
    emitter.writeFile()
    print(colored.GREEN("Compiling completed."))
main()