#ECE_366
#Project 2
#Group 17
#Spring 2020

#Written By:
#abaran6
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
Register_Window = pd.DataFrame(np.column_stack([register_Name2, Register_Num, Reg_Val]), 
                               columns=['Name', 'Number', 'Value'])
Register_Window['Value'] ='0x00000000'


functions = {}
functions["100010"] = "sub "
functions["001100"] = "andi"
functions["001000"] = "addi"
functions["100000"] = "add "
functions["011000"] = "mult"    # R-type
functions["101010"] = "slt "
functions["100011"] = "lw  "
functions["101011"] = "sw  "
functions["000100"] = "beq "     # I-type
functions["000101"] = "bne "     # I-type
functions["000010"] = "j   "       # J-type
functions["100101"] = "or  "
functions["011010"] = "div "
functions["010000"] = "mfhi"
functions["011100"] = "mul "
functions["010010"] = "mflo"

functions_to_bin = {}
functions_to_bin["sub"] = "100010"
functions_to_bin["add"] = "100000"
functions_to_bin["slt"] = "101010"

functions_to_bin["andi"] = "001100"
functions_to_bin["addi"] = "001000"
functions_to_bin["lw"] = "100011"
functions_to_bin["sw"] = "101011"



instruction_table = {
    
        'add'   : ['00','rs','rt','rd','shamt','0x20'],
        'sub'   : ['00','rs','rt','rd','shamt','0x22'],
        'slt'   : ['00','rs','rt','rd','shamt','0x2A'],
        
        'sw'    : ['2B','rs','rt','imm'],
        'andi'  : ['0C','rs','rt','imm'],
        'addi'  : ['08','rs','rt','imm'],
        'lw'    : ['23','rs','rt','imm'],
        'beq'   : ['04','rs','rt','imm'],
        'bne'   : ['05','rs','rt','imm'],

         'j'     : ['02', 'add']
        }

binary_table = {}
binary_table["0"] = "0000"
binary_table["1"] = "0001"
binary_table["2"] = "0010"
binary_table["3"] = "0011"
binary_table["4"] = "0100"
binary_table["5"] = "0101"
binary_table["6"] = "0110"
binary_table["7"] = "0111"
binary_table["8"] = "1000"
binary_table["9"] = "1001"
binary_table["10"] = "1010"
binary_table["11"] = "1011"
binary_table["12"] = "1100"
binary_table["13"] = "1101"
binary_table["14"] = "1110"
binary_table["15"] = "1111"

hex_table = {}
hex_table["0000"] = "0"
hex_table["0001"] = "1"
hex_table["0010"] = "2"
hex_table["0011"] = "3"
hex_table["0100"] = "4"
hex_table["0101"] = "5"
hex_table["0110"] = "6"
hex_table["0111"] = "7"
hex_table["1000"] = "8"
hex_table["1001"] = "9"
hex_table["1010"] = "a"
hex_table["1011"] = "b"
hex_table["1100"] = "c"
hex_table["1101"] = "d"
hex_table["1110"] = "e"
hex_table["1111"] = "f"

Testtxt = "ECE_366_Proj1_mem_Dump.txt"
Testtxt2 = "ECE_366_Project1.txt"

#Testtxt = "hex.txt"
#Testtxt2 = "hex.txt"

def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    count = 0
    for line in asm:          
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(hex(count*4))  # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
            count-=1
        count+=1
        lineCount += 1
        
#hex to binary conversion function
def hex_to_bin(instr):
    integer = int(instr, 16)
    binary = '{:032b}'.format(integer)
    return binary
#binary to hex conversion
def bin_to_hex(instr):
    integer = int(instr,2)
    hexadecimal = hex(integer).replace("0x","")
    hexadecimal="0x"+hexadecimal.zfill(8)
    return hexadecimal

def twos_complement(hexstr,bits):
     value = int(hexstr,16)
     if value & (1 << (bits-1)):
         value -= 1 << bits
     return value

    
def instructions(hex_,nun):
                pc = nun            
                #print(hex_.replace("0x", ''))
                Bin = hex_to_bin(hex_.replace("0x", ''))
                #print(Bin)
                #print(Bin[26:32])
                if(Bin[0:6]=='000000'):
                       rs=Bin[6:11]
                       rt=Bin[11:16]
                       rd=Bin[16:21]
                       func=Bin[26:32]
                       if(functions[func] == "add "):
                               #assembly = functions[func] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
                               #print(assembly)
                               loc=int(rd,2)
                               Register_Window.iloc[loc,2] = Register_Window.iloc[int(rt,2),2] + Register_Window.iloc[int(rs,2),2]
        
                       assembly = functions[Bin[26:32]] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
                               #print(assembly,'hi')
                       pc=0
                       if(functions[Bin[26:32]] == "slt "):
                                   assembly =functions[Bin[26:32]] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
                                   #print(assembly)
                                   if(int(rs,2) < int(rt,2)):
                                       Register_Window.iloc[int(rd,2),2] = 1
                                       pc=0
                                   else:
                                        Register_Window.iloc[int(rd,2),2] = 0
                                        pc=0
                       if(functions[Bin[26:32]] == "or  "):
                                assembly = functions[Bin[26:32]] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
#                                j=0
#                                while j != 5:
#                                    rs[j] == 1 or rt[j] == 1):
#                                    result[j] == 1
#
#                                    j+=1
                                result = rd + rs
                                Register_Window.iloc[int(rd,2),2] = int(result,2)
                                pc=0
                                #print(assembly)
                        
                       elif(Bin[26:32] == "mfhi"):
                             assembly = functions[Bin[26:32]] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
                             
                             pc=0#print(assembly)
                       elif(Bin[26:32] == "mflo"):
                             Register_Window.iloc[int(rt,2),2] = Register_Window.iloc[34,2]
                            
                             assembly = functions[func] + ", $" + str(int(rt,2))
                             pc=0#print(assembly)
                             

                else:
                    func=Bin[0:6]
                    rs=Bin[6:11]
                    rt=Bin[11:16]
                    imm=twos_complement(hex_[6:10],16)
                    #print(imm)
                    
                    if(functions[func] == "addi"):
                        if(Bin[16:20]=='0010'):
                            assembly = functions[func] + " $" + str(int(rt,2)) + ", $"+str(int(rs,2))  + ", 0x" + (hex_[6:10])
                            loc=int(rt,2)
                            val = int(Register_Window.iloc[int(rs,2),2])
                            if(int(val) == 0):
                               Register_Window.iloc[loc,2]= hex_[6:10]
                               pc=0
                            else:
                                Register_Window.iloc[loc,2]= hex(imm + int(hex(val)).replace('0x',''))
                                pc=0    
                        else:
                              #assembly = functions[func] + " $" +str(int(rt,2)) + ", $"+str(int(rs,2))+ "," + str(int(imm,2))
                              loc=int(rt,2)
                              Register_Window.iloc[loc,2] = imm + int(Register_Window.iloc[int(rs,2),2])
                              #print(Register_Window.iloc[loc,0],Register_Window.iloc[loc,1],Register_Window.iloc[loc,2])
                              assembly = functions[func] + " $" +str(int(rt,2)) + ", $"+str(int(rs,2))+ ", " + str(imm)
                              pc=0
                    if(functions[func] == "lw  "):
                        assembly = functions[func] + " $" + str(int(rt,2)) + ", 0x" + (hex_[6:10]) + "($" + str(int(rs,2))+")"
                        pointer = int(Register_Window.iloc[int(rs,2),2]) + int(hex_[6:10])
                        x = pointer%200
                        x= int(x%20)
                        y = x/2
                        val = Address_Window.iloc[x,int(y)]
                        Register_Window.iloc[int(rt,2),2]=val
                        pc=0
                    if(functions[func] == "sw  "):
                        #assembly = functions[func] + " $" + str(int(rt,2)) + ", 0x" + (hex_data[4:8]) + "($" + str(int(rs,2))+")"
                        loc = int(rs,2)
                        if(Register_Window.iloc[loc,2] is str):
                            pointer = int(Register_Window.iloc[loc,2],10)
                            pc=0
                        elif(Register_Window.iloc[loc,2] is int):
                            pointer = Register_Window.iloc[loc,2]
                            pc=0
                        else: pointer = int(Register_Window.iloc[loc,2])
                        x = pointer%200
                        x = x % 20
                        y = x / 2
                        val = Register_Window.iloc[int(rt,2),2]
                        
                        Address_Window.iloc[int(x),int(y)]= val
                        print(int(x),int(y),val)
                        assembly = functions[func] + " $" + str(int(rt,2)) + ", 0x" + (hex_[6:10]) + "($" + str(int(rs,2))+")"
                        pc=0
                    if(functions[func] == "bne "):                    
                        assembly = functions[func] + " $" +str(int(rs,2)) + ", $"+str(int(rt,2))+ ", " + str(imm)
                        if(Register_Window.iloc[int(rs,2),2] != Register_Window.iloc[int(rt,2),2]):
                            target = pc               
                            pc = target + imm + 1
                            #print(hex_, 'jump to', pc, Register_Window.iloc[int(rs,2),2], '!=', Register_Window.iloc[int(rt,2),2])
                        else:
                            pc=0
                    if(functions[func] == "beq "):
                        assembly = functions[func] + " $ $" +str(int(rs,2)) + ", $"+str(int(rt,2))+ ", " + str(imm)                        
                        if(Register_Window.iloc[int(rs,2),2] == Register_Window.iloc[int(rt,2),2]):
                            target = pc
                            pc = target + imm + 1
                        else:
                             pc=0
                    if(functions[func] == "mul "):
                        rd = Bin[16:21]
                        assembly = functions[func] + " $" +str(int(rd,2)) + ", $"+str(int(rs,2))+ ", $" + str(int(rt,2))
                        ##print(assembly)
                        result =  Register_Window.iloc[int(rs,2),2] *  Register_Window.iloc[int(rt,2),2]
                        result_bi = int(result)
                        #print(Register_Window.iloc[int(rs,2),2],'rs * ',Register_Window.iloc[int(rt,2),2],'rt =', result_bi)
                        if(result_bi==0):                               
                            
                                lo=0                               
                                hi=0
                                pc=0
                        else:
                                lo=bin(int(result))
                                hi=bin(int(result))
                        Register_Window.iloc[int(rd,2),2] = result
                        Register_Window.iloc[34,2] = result
                        mult_reg=int(rd,2)
                        pc=0

                    

                print(assembly)
                return pc

arr= np.linspace(2020,4000,num=90,dtype=int)
Address_List=[] 
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
Register_Window = pd.DataFrame(np.column_stack([register_Name2, Register_Num, Reg_Val]), 
                           columns=['Name', 'Number', 'Value'])
Register_Window['Value'] = 0
Register_Window.iloc[32:35,1]=''

for x in np.nditer(arr):
    Address_List.append('0x0000' + str(x))
num_lines = sum(1 for line in open(Testtxt))


np.random.seed(len(Address_List)*len(Data_Seg_T))
Address_Window = DataFrame(np.random.rand(len(Address_List)*len(Data_Seg_T)).reshape(len(Address_List),len(Data_Seg_T)),
                           index=[Address_List],
                           columns=[Data_Seg_T])
Address_Window[0:90] = 0

isNeg = False
labelIndex = []
labelName = []
f = open(Testtxt, "r")
f2 = open(Testtxt2, 'r')
Code_Hex=[]
dataFile = [line for line in f2.readlines() if line.strip()]                                
for line in dataFile:
    if (line.startswith('#')):
                        dataFile.remove(line)
                        
    
saveJumpLabel(dataFile, labelIndex, labelName)

dataFile2 = [line for line in dataFile if line.strip()] 
                              

count=0
four=0
num_lines = len(dataFile2)
Text_Address = []
while count != num_lines:
    integer = four
    temp = hex(integer)
    temp = temp.replace("0x", "")
    Text_Address.append("0x" + temp.zfill(9-len(temp)))
    count=count+1
    four=four+4  
   

for num_lines1 in f:              
    hex_data = num_lines1
    Code_Hex.append('0x' + hex_data.replace('\n',''))
                
i=0
num=0

while i != len(Code_Hex):
    Register_Window.iloc[32,2] = hex(i*4)
    assembly_instr = Code_Hex[int(i)]
    num = instructions(assembly_instr,i)
    if num > 0:
        i=num
    else:
        i+=1 
     
### UNCOMMENT LINES 445-448 FOR STEP BY STEP EXECUTION


#    print("For step press: 'Enter' key\n")
#    program = input('>')
#    if(program=='a'):
#            continue
        
                
#Code_Hex.extend(np.zeros(len(dataFile2)-len(Code_Hex)))
#dataFile.extend(np.zeros(len(Text_Address)-len(dataFile)))

Text_Segment_Window = pd.DataFrame(np.column_stack([Text_Address, Code_Hex, dataFile2]), 
                               columns=['Address', 'Code', 'Source'])  
Label_Window = pd.DataFrame(np.column_stack([labelName, labelIndex]), 
                               columns=['Label', 'Address'])

                    
print(Register_Window,'\n',Address_Window,'\n',Label_Window,'\n\n',Text_Segment_Window)
     
                                                                                                                                  

                                                                                                                                                        
