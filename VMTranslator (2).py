import sys
from os import listdir

class Parser:
    def __init__(self,filename):
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
        if self.bcurrent[0] in ["add","sub","neg","eq","gt","lt","and","or","not"]:
            return "C_ARITHMETIC"
        if self.bcurrent[0] in ["push","pop"]:
            return "C_"+self.bcurrent[0].upper()
        if self.bcurrent[0] in ["goto","label","call","return","function"]:
            return "C_"+self.bcurrent[0].upper()
        return "C_IF"

    def arg1(self):
            return self.bcurrent[0] if self.commandType() == "C_ARITHMETIC" else self.bcurrent[1]

    def arg2(self):
        return self.bcurrent[2]

class CodeWriter:
    def __init__(self,outfilename):
        self.ofile = open(outfilename,"w")
        self.push_d = "@SP\nM=M+1\nA=M-1\nM=D\n"
        self.pop_d = "@SP\nAM=M-1\nD=M\n"
        self.pop_a = "@SP\nAM=M-1\nA=M\n"
        self.fname = ""

    def setFileName(self,filename):
        self.currentClass = filename.split(".")[0]
        self.counter=0

    def writeInit(self):
        self.ofile.write("@256\nD=A\n@SP\nM=D\n")
        self.writeCall("Sys.init",0)

    def writeLabel(self,label):
        self.ofile.write("("self.fname+"$"+label+")\n")

    def writeGoto(self,label):
        codetowrite = "@"+label+"\n0;JMP\n"

    def writeIf(self,label):
        self.ofile.write(self.pop_d + "@"+label+"\nD;JLT\n")

    def writeFunction(functionName,numLocals):
        self.fname = functionName
        codetowrite = "("+functionName+")\n"
        codetowrite +="@"+numLocals+"\nD=A\n@tempo\nM=D\n"
        codetowrite += "("+functionName+".init)\n"
        codetowrite += "@tempo\nM=M-1\n@SP\nAM=M+1\nA=A-1\nM=0\n@tempo\nD=M\n@"+functionName+".init\nD;JGT\n"
        self.ofile.write(codetowrite)

    def writeCall(self,functionName,numArgs):
        codetowrite = "@"+functionName+"."+self.counter+".return\nD=A\n"+self.push_d
        for i in ["LCL","ARG","THIS","THAT"]:
            codetowrite += "@"+i+"\nD=M\n"+self.push_d
        codetowrite += "@SP\nD=A\n@LCL\nM=D\n@"+str(numArgs+5)+"\nD=A\n@SP\nD=A-D\n@ARG\nM=D\n"
        self.ofile.write(codetowrite)
        self.writeLabel(functionName)
        self.ofile.write("("functionName+"."+self.counter+")\n")
        self.count+=1

    def writeReturn(self):
        codetowrite = "@LCL\nD=A\n@tempo\nM=D\n@5\nD=D-A\nA=D\nD=M\n@returnvalue\nM=D\n"
        self.ofile.write(codetowrite)
        self.writePushPop("pop","argument",0)
        codetowrite = "@ARG\nD=A+1\n@SP\nM=D\n"
        for i in ["THAT","THIS","ARG","LCL"]:
            codetowrite +="@tempo\nAM=M-1\nD=M\n@"+i+"\nM=D\n"
        codetowrite = "@returnvalue\n0;JMP\n"
        self.ofile.write(codetowrite)

    def writeArithmetic(self,command):
        fornow = self.currentClass+str(self.counter)
        codetowrite=self.pop_d
        if command in ["add","sub","eq","lt","gt","and","or"]:
            codetowrite += self.pop_a
            if command == "add":
                codetowrite += "D=D+A\n"
            elif command == "sub":
                codetowrite += "D=A-D\n"
            elif command == "and":
                codetowrite += "D=D&A\n"
            elif command == "or":
                codetowrite += "D=D|A\n"
            elif command == "eq":
                codetowrite += "D=D-A\n@"+fornow+".EQUAL\nD;JEQ\nD=0\n@"+fornow+".END\n0;JMP\n("+fornow+".EQUAL)\nD=-1\n("+fornow+".END)\n"
            elif command == "lt":
                codetowrite += "D=D-A\n@"+fornow+".LT\nD;JGT\nD=0\n@"+fornow+".END\n0;JMP\n("+fornow+".LT)\nD=-1\n("+fornow+".END)\n"
            elif command == "gt":
                codetowrite += "D=D-A\n@"+fornow+".GT\nD;JLT\nD=0\n@"+fornow+".END\n0;JMP\n("+fornow+".GT)\nD=-1\n("+fornow+".END)\n"
        else:
            if command == "neg":
                codetowrite+="D=-D\n"
            elif command == "not":
                codetowrite+="D=!D\n"
        codetowrite+=self.push_d
        self.counter +=1
        self.ofile.write(codetowrite)

    def writePushPop(self,command,segment,index):
        segdict = {"argument":"ARG","static":self.currentClass+"."+str(index),"local":"LCL","this":"THIS","that":"THAT"}
        codetowrite = ""
        if command == "push":
            seg_load_d = ""
            if segment in ["local","argument","this","that","static"]:
                seg_load_d = "@"+segdict[segment]+"\nD=M\n@"+str(index)+"\nA=A+D\nD=M\n"
            elif segment in ["pointer","temp"]:
                ramaddress = (3+index) if segment=="pointer" else (5+index)
                seg_load_d = "@"+str(ramaddress)+"\nD=M\n"
            elif segment == "constant":
                seg_load_d = "@"+str(index)+"\nD=A\n"
            codetowrite = seg_load_d+self.push_d
        else:
            load_to_seg = ""
            if segment in ["local","argument","this","that","static"]:
                codetowrite = "@"+str(index)+"\nD=A\n@"+segdict[segment]+"\nA=M\nD=D+A\n@tempo\nM=D\n"+self.pop_d+"@tempo\nA=M\nM=D\n"
            elif segment in ["pointer","temp"]:
                ramaddress = (3+index) if segment=="pointer" else (5+index)
                codetowrite = self.pop_d+"@"+str(ramaddress)+"\nM=D\n"
        self.ofile.write(codetowrite)

    def close(self):
        ending = "@ENDING\n(ENDING)\n0;JMP\n"
        self.ofile.write(ending)
def usage():
    print("usage:", sys.argv[0], "<source-file>.vm or <source-dir>")
    print("\tOutput file will be <source-file>.asm or <source-dir>/<source-dir>.asm")

def main():
    if len(sys.argv) !=2:
        usage()
        sys.exit(-1)
    outFilename = sys.argv[1]
    filenametowrite = outFilename
    while "\\" in filenametowrite :
        filenametowrite = filenametowrite[filenametowrite.index("\\")+1:]
    finalname = outFilename+"\\"+filenametowrite+".asm"
    print(finalname)
    codewrite = CodeWriter(finalname)
    inFilesnames = [i for i in listdir(sys.argv[1]) if ".vm" in i] if not ".vm" in sys.argv[1] else sys.argv[1]
    if type(inFilesnames) != list:
        inFilesnames =[inFilesnames]
    for inFilename in inFilesnames:
        parsed = Parser(sys.argv[1]+"\\"+inFilename)
        codewrite.setFileName(inFilename)
        while parsed.HasMoreCommands():
            toparse = parsed.advance()
            if parsed.commandType() == "C_ARITHMETIC":
                codewrite.writeArithmetic(parsed.arg1())
            elif parsed.commandType() in ["C_PUSH","C_POP"]:
                codewrite.writePushPop(toparse[:toparse.index(" ")],parsed.arg1(),int(parsed.arg2()))
            elif parsed.commandType() in []
    codewrite.close()

if __name__ == "__main__":
    main()
