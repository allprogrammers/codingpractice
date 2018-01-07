import sys

symbolTable = {"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24576}

########## Modules

class Parser:
    def __init__(self,filename):
        self.code = open(filename,"r")
        self.beginpos = self.code.tell()

    def hasMoreCommand(self):
        self.current = self.code.readline()
        if self.current:
            return False
        return True

    def advance(self):
            return self.current

    def commandType(self):
        if self.current[0]=="@":
            return "A_COMMAND"
        if self.current[0]=="(":
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self):
        if self.commandType() == "A_COMMAND":
            return self.current[1:]
        if self.commandType() == "L_COMMAND":
            return self.current[1:-1]

    def dest(self):
        return self.current[:self.current.index("=")]

    def comp(self):
        if "=" in self.current:
            return self.current[self.current.index("=")+1:]
        return self.current[:self.current.index(";")]

    def jump(self):
        return self.current[self.current.index(";"):]

class Code:
    def dest(self,mnemonic):
        d1,d2,d3 = 0,0,0
        if "M" in mnemonic:
            d3=1
        if "A" in mnemonic:
            d1=1
        if "D" in mnemonic:
            d2=2
        return str(d1)+str(d2)+str(d3)

    def comp(self,mnemonic):
        compDict={'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100','A':'0110000', '!D':'0001101', '!A':'0110001', '-D':'0001111','-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111','D&A':'0000000','D|A':'0010101','':'xxxxxxx','M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111','M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000', 'D|M':'1010101'}
        return compDict[mnemonic]

    def jump(self,mnemonic):
        jumpdict={"JMP":"111","JGT":"001","JGE":"011","JLT":"100","JLE":"110","JNE":"101","JEQ":"010","null":"000"}
        if mnemonic in jumpdict.keys():
            return jumpdict[mnemonic]
        return "000"

class SymbolTable:
    def __init__(self):
        self.st = {}
    def addEntry(self,symbol,address):
        self.st[symbol]=address
    def contains(self,symbol):
        return symbol in self.st.keys()
    def GetAddress(self,symbol):
        return self.st[symbol]

########## Helper Functions

def usage():
    print("usage:", sys.argv[0], "<source-file>.asm")
    print("\tOutput file will be <source-file>.hack")

########## Main

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(-1)
    inFileName = sys.argv[1]
    outFileName = sys.argv[1].split(".")[0]+".hack"

    # Assemble inFileName and write binary commands to output file.
    parser = Parser(inFileName)
    coder = Code()
    symTable = symbolTable()
    romaddress=0
    ramaddress=0
    while parser.hasMoreCommands():
        currentcommand=parser.advance()
        symbol=parser.symbol(currentcommand)
        if parser.commandType(currentcommand)=="L_COMMAND":
            if (not symTable.contains(symbol)):
                symtoadd=romaddress
                romaddress +=1
                symTable.addEntry(symbol,symtoadd)
    parser.code.seek(parser.beginpos)
    writer = open(outFileName,"w")
    while parser.hasMoreCommand():
        currentcommand=parser.advance()
        symbol=parser.symbol(currentcommand)
        ctype=parser.commandType(currentcommand)
        if ctype=="A_COMMAND":
            if symTable.contains(symbol):
                toc=symTable.GetAddress(symbol)
            else:
                symtoadd=ramaddress
                toc = symtoadd
                ramaddress +=1
                symTable.addEntry(symbol,symtoadd)
            writer.write("0"+"{0:15b}".format(int(toc))+"\n")
        elif ctype=="C_COMMAND":
            bitcommand="111"
            destbit = coder.dest(parser.dest())
            compbit = coder.comp(parser.comp())
            jumpbit = coder.jump(parser.jump())
            bitcommand += destbit + compbit + jumpbit
            writer.write(bitcommand+"\n")

if __name__ == "__main__":
    main()
