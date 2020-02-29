#ECE_366
#Project 2
#Group 17
#Spring 2020

#Written By:
#aibarr23
#spate511
#vorteg6

import numpy as np
import pandas as pd

from pandas import Series, DataFrame


register_Name2 = [
	'$zero',
	'$at',
	'$v0',
	'$v1',
	'$a0',
	'$a1',
	'$a2',
	'$a3',
	'$t0',
	'$t1',
	'$t2',
	'$t3',
	'$t4',
	'$t5',
	'$t6',
	'$t7',
	'$s0',
	'$s1',
	'$s2',
	'$s3',
	'$s4',
    '$s5',
	'$s6',
	'$s7',
	'$t8',
	'$t9',
	'$k0',
	'$k1',
    '$gp',
	'$sp',
	'$fp',
    '$ra',
]
Register_Num = []
Reg_Val= np.zeros(35)
count = 0
while(count <= 34):
  Register_Num.append(count)
  #Reg_Val[count] = 0
  count += 1

register_Name2.append("pc")
register_Name2.append("hi")
register_Name2.append("lo")

Data_Seg_T = [
 "Value(+0)"
,"Value(+4)" 
,"Value(+8)"
,"Value(+C)" 
,"Value(+10)" 
,"Value(+12)"
,"Value(+14)"
,"Value(+18)"
,"Value(+1c)"] 

arr= np.linspace(2020,3000,num=50,dtype=int)
Address_List=[] 
for x in np.nditer(arr):
    Address_List.append('0x0000' + str(x))
    


# hex to binary conversion function
def hex_to_bin(instr):
    integer = int(instr, 16)
    binary = '{:032b}'.format(integer)
    return binary


# binary to hex conversion
def bin_to_hex(instr):
    integer = int(instr,2)
    hexadecimal = hex(integer).replace("0x","")
    hexadecimal = hexadecimal.zfill(8)
    return hexadecimal


# the value 255 is not fixed feel free to change it to any other value
def large_val_limiter(strVal):
    if(strVal>255):
        strVal = hex(strVal)
    return str(strVal)


# twos_complement
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
        lineCount += 1


def formatChecker(instr):
    checker = False
    if any(c>'f' for c in instr):
        print("Illegal characters")
    if not instr.isalnum():
        print("Special characters are not allowed")
    elif len(instr)!=8:
        print("Hex instruction must contain 8 characters")
    else:
        checker = True
    return checker


functions = {}
functions["100010"] = "sub"     # R-type
functions["100000"] = "add"     # R-type
functions["101010"] = "slt"     # R-type
functions["011000"] = "mult"    # R-type
functions["001100"] = "andi"    # I-type
functions["001000"] = "addi"    # I-type
functions["100011"] = "lw"      # I-type
functions["101011"] = "sw"      # I-type
functions["000100"] = "beq"     # I-type
functions["000101"] = "bne"     # I-type
functions["000010"] = "j"       # J-type


def disassembler(instr, functions):          # supports addi, andi, sub, add, lw, sw and slt

    if instr[0:6] == "000000":
        rs = instr[6:11]
        rt = instr[11:16]
        rd = instr[16:21]
        func = instr[26:32]
        assembly_code = functions[func] + " $" + str(int(rd, 2)) + ", $" + str(int(rs, 2)) + ", $" + str(int(rt, 2))
    else:
          func = instr[0:6]
          rs = instr[6:11]
          rt = instr[11:16]
          imm = twos_comp(int(instr[16:32], 2), 16)
          imm = large_val_limiter(imm)
          assembly_code = functions[func] + " $" + str(int(rt, 2)) + ", $" + str(int(rs, 2)) + ", " + imm

    return assembly_code

Code_Hex=[]
def assembler(dataFile, labelName, labelIndex, w):  # supports addi and j
    for line in dataFile:
        index = line.find('#')  # finds comments and removes them for easier processing
        if index != -1:
            line = line[0:index - 1]
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")  # Removes extra chars
        line = line.replace(" ", "")  # Removes extra chars
        line = line.replace("zero", "0")  # can use both $zero and $0
        #aline.replace('0x','')
        if (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            if('x' in  line):
                line = line.replace('0x','')
                print(line)
            line = line.split(",")
            if (int(line[2]) >= 0):
                imm = format(int(line[2]), '016b')
            else:
                imm = format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "001000" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:4] == "andi"):  # ANDI
            line = line.replace("andi", "")
            line = line.split(",")
            if (int(line[2]) >= 0):
                imm = format(int(line[2]), '016b')
            else:
                imm = format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "001100" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:3] == "beq"):  # BEQ
            line = line.replace("beq", "")
            line = line.split(",")
            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                    imm = str(format(int(labelIndex[i]), '016b'))
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000100" + str(rt) + str(rs) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:3] == "bne"):  # BNE
            line = line.replace("bne", "")
            line = line.split(",")
            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                    imm = str(format(int(labelIndex[i]), '016b'))
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000101" + str(rt) + str(rs) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:2] == "lw"):  # LW
            line = line.replace("lw", "")
            line = line.split(",")
            line[1] = line[1].split('(')
            line[1][1] = line[1][1].replace(")", "")
            if (int(line[1][0]) >= 0):
                imm = format(int(line[1][0]), '016b')
            else:
                imm = format(65536 + int(line[1][0]), '016b')
            rs = format(int(line[1][1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "100011" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:2] == "sw"):  # SW
            line = line.replace("sw", "")
            line = line.split(",")
            line[1] = line[1].split('(')
            line[1][1] = line[1][1].replace(")", "")
            line[1][0] = line[1][0].replace("0x", "")
            line[1][0] = int(line[1][0], 16)
            if (int(line[1][0]) >= 0):
                imm = format(int(line[1][0]), '016b')
            else:
                imm = format(65536 + int(line[1][0]), '016b')
            rs = format(int(line[1][1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "101011" + str(rs) + str(rt) + str(imm)
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:3] == "add"):  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000000" + str(rd) + str(rs) + str(rt) + "00000" + "100000"
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:3] == "sub"):  # SUB
            line = line.replace("sub", "")
            line = line.split(",")
            rd = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000000" + str(rd) + str(rs) + str(rt) + "00000" + "100010"
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:3] == "slt"):  # SLT
            line = line.replace("slt", "")
            line = line.split(",")
            rd = format(int(line[2]), '05b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "000000" + str(rd) + str(rs) + str(rt) + "00000" + "101010"
            hex_file.write(bin_to_hex(binary) + "\n")

        elif (line[0:1] == 'j'):  # Jump
            line = line.replace("j", "")
            line = line.split(",")
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            if (line[0].isdigit()):  # First,test to see if it's a label or an immediate (this won't support labels like ex: 1loop or 2exit)
                binary = '000010' + str(format(int(line[0]), '026b'))
                hex_file.write(bin_to_hex(binary) + "\n")
            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        binary = '000010' + str(format(int(labelIndex[i]), '026b'))
                        hex_file.write(bin_to_hex(binary) + '\n')
        print(bin_to_hex(binary) + '\n')
        Code_Hex.append('0x'+bin_to_hex(binary))               

#print("For disassembler press: 'd'\nFor assembler press:    'a'\nFor exit press:         'e' ")
#program = input(">")
#if (program == 'd'):
#    while (program != 'e'):
#        instr = input("Enter instruction in hex: ")
#        instr = instr.lower()
#        if (instr == 'e'):
#            exit()
#        if (formatChecker(instr)):
#            binIstr = hex_to_bin(instr)
#            out = disassembler(binIstr, functions)
#            print(out + "\n")

#Testtxt2="Perception Algorithm.txt"
Testtxt2="ECE_366_Project1.txt"

program = 'a'
if (program == 'a'):
    assembly_file = open("ECE_366_Project1.txt", "r")
    hex_file = open("hex.txt", "a+")
    labelIndex = []
    labelName = []
    dataFile = assembly_file.readlines()

    for data in range(dataFile.count('\n')):
        dataFile.remove("\n")

    for i in range(2):
        for data in dataFile:
            if (data.startswith('#')):
                dataFile.remove(data)

    saveJumpLabel(dataFile, labelIndex, labelName)

    assembler(dataFile, labelName, labelIndex, hex_file)

    print("Done! Hex_file consists of translated instructions in HEX.")
    hex_file.close()
    assembly_file.close()
    
    
Register_Window = pd.DataFrame(np.column_stack([register_Name2, Register_Num, Reg_Val]), 
                               columns=['Name', 'Number', 'Value'])
    
count=0
four=4
num_lines = sum(1 for line in open(Testtxt2))
Text_Address = []
while count != num_lines+1:
    integer = four
    temp = hex(integer)
    temp = temp.replace("0x", "")
    Text_Address.append("0x" + temp.zfill(9-len(temp)))
    count=count+1
    four=four+4


#Need to find out why codes arent the same length as address
Code_Hex.extend(np.zeros(len(Text_Address)-len(Code_Hex)))
dataFile.extend(np.zeros(len(Text_Address)-len(dataFile)))

Text_Segment_Window = pd.DataFrame(np.column_stack([Text_Address, Code_Hex, dataFile]), 
                               columns=['Address', 'Code', 'Source'])

np.random.seed(len(Address_List)*len(Data_Seg_T))

Address_Window = DataFrame(np.random.rand(len(Address_List)*len(Data_Seg_T)).reshape(len(Address_List),len(Data_Seg_T)),
index=[Address_List],
columns=[Data_Seg_T])


Label_Address = []
count=0
while count != 15:
    Label_Address.append(Text_Address[labelIndex[count]-1])
    count=count+1

Label_Window = pd.DataFrame(np.column_stack([labelName, Label_Address]), 
                               columns=['Label', 'Address'])

