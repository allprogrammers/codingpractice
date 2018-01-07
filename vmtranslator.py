import sys
from os import listdir

class Parser:
    def __init__(self,filename):
        self.arthcoms = ["add","sub","neg","eq","gt","lt","and","or","not"]
        self.pushpop = ["push","pop"]
        self.code = open(filename,"r")
        self.beginpos=self.code.tell()

    def HasMoreCommands(self):
        self.current = ""
        while (self.current ==""):
            self.current = self.code.readline()
            if not self.current:
                return False
            self.current=self.current.strip()
            if "/" in self.current:
                self.current = self.current[:self.current.index("/")]
        return bool(self.current)

    def advance(self):
        return self.current

    def commandType(self):
        self.bcurrent = self.current.split()
        if self.bcurrent[0] in self.arthcoms:
            return "C_ARITHEMATIC"
        if self.bcurrent[0] in self.pushpop:
            return "C_"+self.bcurrent[0].upper()
        return False

    def arg1(self):
            return self.bcurrent[0] if self.commandType() == "C_ARITHEMATIC" else self.bcurrent[1]

    def arg2(self):
        return self.bcurrent[2]

class CodeWriter:
    def __init__(self,outfilename):
        self.ofile = open(filename,"a")
        self.push_d = "@SP\nM=M+1\nA=M-1\nM=D\n"
        self.pop_d = "@SP\nM=M-1\nA=M+1\nD=M\n"
        self.pop_a = "@SP\nM=M-1\nA=M+1\nA=M\n"

    def setFileName(self,filename):
        self.currentClass = filename.split(".")[0]
        self.counter=0

    def writeArithmetic(self,command,writenow=True):
        fornow = self.currentClass+str(self.counter)
        codetowrite=self.pop_d
        if command in ["add","sub","eq","lt","gt","and","or"]:
            codetowrite += self.pop_a
            if command == "add":
                codetowrite += "D=D+A\n"
                codetowrite += self.push_d
            elif command == "sub":
                codetowrite += "D=D-A\n"
            elif command == "and":
                codetowrite += "D=D&A\n"
            elif command == "or":
                codetowrite += "D=D|A\n"
            elif command == "eq":
                codetowrite += "D=D-A\n@"+fornow+".EQUAL\nD;JEQ\nD=0\n@"+fornow+".END\n0;JMP("+fornow+".EQUAL)\nD=-1("+fornow+".END)\n"
            elif command == "lt":
                codetowrite += "D=D-A\n@"+fornow+".LT\nD;JGT\nD=0\n@"+fornow+".END\n0;JMP("+fornow+".LT)\nD=-1("+fornow+".END)\n"
            elif command == "gt":
                codetowrite += "D=D-A\n@"+fornow+".GT\nD;JLT\nD=0\n@"+fornow+".END\n0;JMP("+fornow+".GT)\nD=-1("+fornow+".END)\n"
        else:
            if command == "neg":
                codetowrite+="D=-D\n"
            elif command == "not":
                codetowrite+="D=!D\n"
        codetowrite+=self.push_d
        self.counter +=1
        if writenow:
            self.ofile.write(codetowrite)
        else:
            return codetowrite

    def writePushPop(self,command,segment,index):
        segdict = {"argument":"ARG","static":self.currentClass+"."+str(index),"local":"LCL","this":"THIS","that":"THAT"}
        codetowrite = ""
        if command == "push":
            seg_load_d = ""
            if segment in ["local","argument","this","that","static"]:
                seg_load_d = "@"+segdict[segment]+"\nD=M\n@"+str(index)+"\nA=A+D\nD=M\n"
            elif segment in ["pointer","temp"]:
                ramaddress = (3+index) if segment==pointer else (5+index)
                seg_load_d = "@"+str(ramaddress)+"\nD=M\n"
            elif segment == "constant":
                seg_load_d = "@"+str(index)+"\nD=A\n"
            codetowrite = seg_load_d+self.push_d
        else:
            pop_d="@SP\nM=M-1\nA=M+1\nD=M\n"
            load_to_seg = ""
            if segment in ["local","argument","this","that","static"]:
                load_to_seg = "@"+segdict[segment]
            elif segment in ["pointer","temp"]:
                ramaddress = (3+index) if segment==pointer else (5+index)
                load_to_seg = "@"+str(ramaddress)
            load_to_seg +="\nM=D"
            codetowrite = self.pop_d+load_to_seg
        self.ofile.write(codetowrite)

    def close(self):
        return
def usage():
    print("usage:", sys.argv[0], "<source-file>.vm or <source-dir>")
    print("\tOutput file will be <source-file>.asm or <source-dir>/<source-dir>.asm")

def main():
    if len(sys.argv) !=2:
        usage()
        sys.exit(-1)
    outFilename = sys.argv[1].split(".")[0]+".asm"
    codewrite = CodeWriter(outFilename)
    inFilesnames = [i for i in listdir(sys.argv[1])] if not ".vm" in sys.argv[1] else sys.argv[1]
    for inFilename in inFilesnames:
        inFilename = sys.argv[1]
        parsed = Parse(inFilename)
        codewrite.setFileName(sys.argv[1].split(".")[0])
        while parsed.HasMoreCommands():
            toparse = parsed.advance()
            if parsed.commandType() == "C_ARITHEMATIC":
                codewrite.writeArithematic(parsed.arg1())
            elif parsed.commandType() in ["C_PUSH","C_POP"]:
                codewrite.writePushPop(toparse[:toparse.index(" ")],parsed.arg1(),parsed.arg2())

if __name__ == "__main__":
    main()
