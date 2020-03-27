##############################################################################
#                         SIC Assembler - Pass 1                             #
#                               3/20/2020                                    #
#                    By: Aseel Arafeh && Shaima Wazwaz                       #
##############################################################################

import sys

# for arg in sys.argv:
#     print("hi " + arg)

print(sys.argv[0])
print(sys.argv[1])

sicFile = open(sys.argv[0], "r")
intermediateFile = open(sys.argv[1], "w")

SYMPTAB = []
LITTAB = {}
lineNumber = 0
LOCCTR = 0
isStart = 0
labelMap = {}

for line in sicFile:
    isRESB = 0
    isRESW = 0
    isBYTE = 0
    isLTORG = 0

    lineNumber = lineNumber + 1
    instructionSize = 3

    if line.strip() == "":
        continue

    if line.strip()[0] == '.':
        continue

    else:
        # write the line on list file
        intermediateFile.write(line)
        # 1-8 Label
        label = line[0:8]
        label = label.strip()

        if labelMap.get(label) != None:
            errorMessage = "At line " + str(lineNumber) +" : Symbol " + label + " already exists!\n"
            print(errorMessage)
            exit()

        # 10-15 Operation code (or Assembler directive)
        opCode = line[9:15]
        opCode = opCode.strip()

        if opCode == "START":
            isStart = 1
        elif opCode == "RESW":
            isRESW = 1
        elif opCode == "RESB":
            isRESB = 1
        elif opCode == "BYTE":
            isBYTE = 1
        elif opCode == "LTORG":
            isLTORG = 1

        # 18-35 Operand
        operand = line[17:35]
        operand = operand.strip()

        if isStart == 1:
            LOCCTR = operand
            startAddress = operand
            PROGNAME = label
            isStart = 0
            continue
        elif isRESW == 1:
            if operand == "":
                errorMessage = "At line " + str(lineNumber) + " : Directive " + opCode + " needs an operand\n"
                print(errorMessage)
                exit()
            instructionSize = int(operand)*3
        elif isRESB == 1:
            if operand == "":
                errorMessage = "At line " + str(lineNumber) + " : Directive " + opCode + " needs an operand\n"
                print(errorMessage)
                exit()
            instructionSize = operand
        elif isBYTE:
            if operand == "":
                errorMessage = "At line " + str(lineNumber) + " : Directive " + opCode + " needs an operand\n"
                print(errorMessage)
                exit()
            instructionSize = 1
        elif isLTORG or opCode == "END":
            for literal in LITTAB:
                if LITTAB[literal][2] == -1:
                    LITTAB[literal][2] = hex(LOCCTR).lstrip("0x")
                    LOCCTR += int(LITTAB[literal][1])
        elif len(operand) > 1 and operand[0]  == '=' and LITTAB.get(operand) == None:
            value = operand[3:len(operand) - 1]
            conv = ""
            address = -1
            if(operand[1] == 'C'):
                for ch in value:
                    conv +=hex(ord(ch)).lstrip("0x")
            else:
                conv = operand[3:len(operand) - 1]
            length = len(conv) / 2
            LITTAB[operand] = [conv, length, address]

        if label != "":
            temp = hex(int(LOCCTR)).replace("0x", "")
            SYMPTAB.append([label, temp])
            labelMap[label] = 1
        if opCode != "END":
            LOCCTR = int(LOCCTR) + int(instructionSize)

intermediateFile.close()

PROGLEN = LOCCTR - int(startAddress)
PROGLEN = hex(int(PROGLEN)).replace("0x", "")

print("Program Name : " + PROGNAME)
print("Program Length : " + PROGLEN)
print(SYMPTAB)
print(LITTAB)

# cmd
# test real example