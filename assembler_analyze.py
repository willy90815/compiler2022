from os import listdir
from os import system,_exit
#author 10827240 ??³æ?¯ç??
class Token_Cutter:
    def __init__(self):
        self.instruction_list = []
        self.table1 = [] # delimeters
        self.table2 = [] # Operation
        self.table3 = {} # Interger
        self.table4 = {} # RealNumber
        self.table5 = {} # Identifier
         
        
        self.table1 = self.read_reserved("Table1.table")
        self.table2 = self.read_reserved("Table2.table")
    def clear(self):
        self.table5 = {} # symbol table
        self.table6 = {} # interger table
        self.table7 = {} # string table
    def get_token(self,filename):
        with open(filename) as infile:
            self.instruction_list = infile.readlines()
        
        for i in range(len(self.instruction_list)):
            ins = self.instruction_list[0].removesuffix("\n")
            ins = self.instruction_list[0].split()
            self.polling_delimiter(ins)
            self.get_table_info(ins)
            self.instruction_list.append(ins)
            self.instruction_list.remove(self.instruction_list[0])

        return self.instruction_list

    def polling_delimiter(self,ins):
        for delimeter in self.table1:
            for seg in ins:
                if seg.find(delimeter) != -1:
                    self.cut_with_delimiter(ins,delimeter)
                    break


    def get_table_info(self, ins):
        j= 0
        for i in range(len(ins)):
            if i+j == len(ins):
                break
            token = self.find_table(ins[0])
            ins.append(token)
            ins.remove(ins[0])


    def cut_with_delimiter(self, ins, delimeter):
        for i in range(len(ins)):
            token = ins[0].split(delimeter)
            if token[0] != '':
                ins.append(token.pop(0)) 
            else:
                token.pop(0)
            for i in range(len(token)):
                ins.append(delimeter)
                if token[0] != '':
                    ins.append(token.pop(0)) 
                else:
                    token.pop(0)
            ins.remove(ins[0])



    def find_table(self, token):
        token_l = token.lower()
        for i in range(len(self.table1)):
            if token_l == self.table1[i]:
                return [token,"1",str(i+1)]
        token_up = token.upper()
        for i in range(len(self.table2)):
            if token_up == self.table2[i]:
                return [token,"2",str(i+1)]
        try:
            int(token)
            value = self.count_hash_value(token,self.table3)
            self.table3.update({token:value})
            return [token,"3",str(value)]

        except ValueError:
            try:
                float(token)
                value = self.count_hash_value(token,self.table4)
                self.table4.update({token:value})
                return [token,"4",str(value)]
            except ValueError:
                value = self.count_hash_value(token,self.table5)
                self.table5.update({token:value})
                return [token,"5",str(value)]

#        for i in range(len(self.table3)):
            if token_up == self.table3[i]:
                return [token,"3",str(i+1)]
#        for i in range(len(self.table4)):
            if token_up == self.table4[i]:
                return [token,"4",str(i+1)]
#        if token.isdecimal():
#            return self.define_in_table([token,"6","0"])
        return self.define_in_table([token,"5","0"])


    def count_hash_value(self,token,table):
        value = sum(list(token.encode("ascii"))) %100
        while(1):
            try:
                if table.get(token) is not None:
                    break
                list(table.values()).index(value)
                value+=1
            except ValueError:
                break
        return value

    def read_reserved(self, filename):
        with open("./CompilerTable/"+filename) as table_file:
            table = table_file.readlines()
            for i in range(len(table)):
                table.append(table[0].removesuffix("\n"))
                table.pop(0)
        return table

        
class Analyzer:
    def __init__(self):
        self.instruction_list = []
        self.using_SICXE = False

    def clear(self):
        self.instruction_list = []
        self.using_SICXE = False
    def analze(self):
        for ins in self.instruction_list:
            try:
                self.define_instruction_type(ins)
            except:
                pass
                
        return self.instruction_list


    def define_instruction_type(self,ins):
        #istruction structure[0~1,]
        # [0]:symbol
            # 0: no symbol
            # 1: symbol
        # [1]:operation
            # 0:no
            # 1:op
            # 2:pesudo & Extra
            # 3:format 4 +add +(symbol) is in front of instruction
            # 4:literal define
        # [2]:interaction reg
            # 0:no
            # 1:reg 
            # 2:immd
            # 3:symbol
            # 4:reg reg
            # 5:addr
            # 6: decimal
            # 7:symbol reg
            # 8:string
        # [3]:comment
            # 0:no Comment
            # 1:comment
        # [4]:addressing mode
            # 0:no
            # 1:immediate
            # 2:direct
            # 3:indirect
            # 4:index
            # 5:literal
        ins_struct = ["0","0","0","0","0"]

        if len(ins) == 0:
            ins.insert(0,ins_struct)
            return
                       #start with symbol
        ins_struct[0] = self.is_symbol(0,ins)
        ins_struct[3] = self.is_comment(0,ins)
        if ins_struct[3] == "1":
            pass
        elif ins_struct[0] == "1":                        #ins with symbol
            ins_struct[1],index = self.is_operation(1,ins)
            ins_struct[2],ins_struct[4],index = self.analze_operand(2+index,ins)
            ins_struct[3] = self.is_comment(index+1,ins)
        else:                                       #ins without symbol
            ins_struct[1],index = self.is_operation(0,ins)
            ins_struct[2],ins_struct[4],index = self.analze_operand(1+index,ins)
            ins_struct[3] = self.is_comment(index+1,ins)        
        ins.insert(0,ins_struct)


    def is_symbol(self,index,ins):
        if ins[index][1] == "5":                #start with symbol
            return "1"
        return "0"


    def is_comment(self,index,ins):
        if index >= len(ins):
            return "0"
        if ins[index][1] == "4":
            if ins[0][0] == ".":
                return "1"
            else:
                return "0"
        else:
            return "0"


    def is_operation(self,index,ins):
        if ins[index][1] == "1":        #op
            return "1",0
        elif ins[index][1] == "2":      #pesudo
            return "2",0
        elif ins[index][0] == "+" and ins[index+1][1] == "1":
            return "3",1
        else:
            return "0",0


    def analze_operand(self,index,ins):
        if index >= len(ins):
            return "0","0",0
        if ins[index][1] == "3":                    #register
            if len(ins)>index+2:
                if ins[index+1][0] == ",":
                    if ins[index+2][1] == "3":          #register & register
                        return "4","0",index+2
            return "1","0",index+1
        if ins[index][1] == "4":                                        #delimeter
            if ins[index][0] == "#":                                        #immdiate
                if ins[index+1][1] == "5":
                    return "3", "1", index+1
                elif ins[index+1][1] == "6":
                    return "2", "1", index+1
            if ins[index][0] == "@":                                    #indirect
                if ins[index+1][1] == "6":
                    return "2", "3", index+1
                if ins[index+1][1] == "7":
                    return "8", "3", index+1
                if ins[index+1][1] == "5":
                    return "3", "3", index+1
            if ins[index][0] == "=":                                    #literal
                if ins[index+1][0] == "'" and len(ins)>index+3: 
                    if ins[index+2][1] == "6" and ins[index+3][0] == "'":
                        return "2","5",index+3
                    if ins[index+2][1] == "7" and ins[index+3][0] == "'":       #string
                        return "8","5",index+3
                if ins[index+1][1] == "6":                              
                    return "6","5",index+1
            if ins[index][0] == "'" and len(ins)>index+2:               #immediate
                if ins[index+1][1] == "6" and ins[index+2][0] == "'":
                    return "2","1",index+2
                if ins[index+1][1] == "7" and ins[index+2][0] == "'": #string
                    return "8","1",index+2
        if ins[index][1] == "5":                                        #symbol
            if len(ins)>index+2 and ins[index+1][0] == ",":
                    if ins[index+2][0] == "X" or ins[index+2][0] == "x":          #symbol & index
                        return "7","4",index+2
            return "3","2",index+1
        if ins[index][1] == "6":                                        #immediate addr
            return "2","2",index
        else:
            return "0","0",index


    def show(self):
        for ins in self.instruction_list:
            print(ins)
class Assembler:
    # datastructures
    # [0] : addr
    # [1] : len
    # [2] : obj code
    # [3] : format 
        # 0: not a instruction
        # 1-4: format1-4
        # 5: pesudo
        # 6: standard type


    def __init__(self):
        self.instruction_list = []
        self.op_table ={}
        self.reg_table = {}
        self.symbol_table = {}
        self.literal_table = []
        self.read_op_table()
        self.read_reg_table()
        self.strat = 0x0
        self.pc = 0x0000
        self.base=0x0000
        self.using_SICXE = False
    def clear(self):
        self.instruction_list = []
        self.op_table ={}
        self.reg_table = {}
        self.symbol_table = {}
        self.literal_table = []
        self.strat = 0x0
        self.pc = 0x0000
        self.base=0x0000
        self.using_SICXE = False

    def generate_obj_code(self,using_SICXE):
        self.using_SICXE = using_SICXE
        try:
            self.define_symbol_addr()
        except:
            pass
        self.pc = 0x0000
        for ins in self.instruction_list:
            try:
                if self.using_SICXE:
                    self.get_obj_code_SICXE(ins)
                else:
                    self.get_obj_code_SIC(ins)
            except:
                ins.append(["sytax error"])

        return self.instruction_list


    def define_symbol_addr(self):
        for ins in self.instruction_list:
            if len(ins)>1 and len(ins[1]) == 5 and ins[1][1] =="4":
                pass
            elif self.using_SICXE:
                self.set_ins_len_XE(ins)
            else:
                self.set_ins_len(ins)
            if ins[1][0] == "1":
                self.symbol_table[ins[2][0]] = ins[0][0]


    def read_op_table(self):
        with open("./SIC_table/op_table.table") as in_file:
            temp_table = in_file.readlines()
        for line in temp_table:
            self.op_table[line.split()[0]] = [line.split()[1],line.split()[2]]

    def read_reg_table(self):
        with open("./SIC_table/reg_table.table") as in_file:
            temp_table = in_file.readlines()
        for line in temp_table:
            self.reg_table[line.split()[0]] = line.split()[1]


    def get_obj_code_SIC(self, ins):
        if ins[0][1] != 0:
            if ins[1][0] == "1":              #with symbol
                if ins[1][1] == "1" or ins[1][1] == "3":
                    ins[0][2] = self.operation_obj_SIC(3,ins)
                else:
                    ins[0][2] = self.pesudo_obj(3,ins)

            else:
                if ins[1][1] == "1" or ins[1][1] == "3":
                    ins[0][2] = self.operation_obj_SIC(2,ins)
                else:
                    ins[0][2] = self.pesudo_obj(2,ins)
    def get_obj_code_SICXE(self, ins):
        if ins[0][1] != 0:
            if ins[1][0] == "1":              #with symbol
                if ins[1][1] == "1" or ins[1][1] == "3":
                    ins[0][2] = self.operation_obj_SICXE(3,ins)
                elif ins[1][1] == "4":
                    ins[0][2] = self.literal_obj(3,ins)
                else:
                    ins[0][2] = self.pesudo_obj(3,ins)

            else:
                if ins[1][1] == "1" or ins[1][1] == "3":
                    ins[0][2] = self.operation_obj_SICXE(2,ins)
                else:
                    ins[0][2] = self.pesudo_obj(2,ins)
        else:
            if ins[1][0] == "1":              #with symbol
                if ins[1][1] == "2":
                    ins[0][2] = self.pesudo_obj(3,ins)
            else:
                if ins[1][1] == "2":
                    ins[0][2] = self.pesudo_obj(2,ins)

    def literal_obj(self,index,ins):
        obj_code = 0
        if ins[index+1][1] == "6" and ins[1][2] == "2":
            obj_code = int(ins[index+1][0],16)
        elif ins[index+1][1] == "7":
            for ch in list(ins[index+1][0].encode("ascii")):
                obj_code = obj_code*0x100+int(ch)
        else:
            obj_code = int(ins[index+1][0])
        return hex(obj_code)
    def operation_obj_SIC(self, index, ins):
            op_code = int(self.op_table[ins[index][0].lower()][0],16)
            if ins[1][2] == "3":
                addr = self.symbol_table[ins[index+1][0]]
                return hex(op_code*0x10000+addr)
            elif ins[1][2] == "0":
                return hex(op_code*0x10000)
            elif ins[1][2] == "7":
                if ins[index+3][0] == "X":
                    addr = self.symbol_table[ins[index+1][0]]
                    return hex(op_code*0x10000+0x8000+addr)

    def operation_obj_SICXE(self, index, ins):
        self.get_pc_value(ins)
        if ins[1][0] == "1": # with symbol
            if ins[0][3] == "1":
                return self.format1(3,ins)
            elif ins[0][3] == "2":
                return self.format2(3,ins)
            elif ins[0][3] == "3":
                return self.format3(3,ins)
            elif ins[0][3] == "4":
                return self.format4(4,ins) 
        else:
            if ins[0][3] == "1":
                return self.format1(2,ins)
            elif ins[0][3] == "2":
                return self.format2(2,ins)
            elif ins[0][3] == "3":
                return self.format3(2,ins)
            elif ins[0][3] == "4":
                return self.format4(3,ins)   
    def get_pc_value(self,ins_source):
        for ins in self.instruction_list:
            if ins[0][0]>ins_source[0][0]:
                self.pc = ins[0][0]
                return
    def format1(self,index,ins):
        return hex(int(self.op_table[ins[index][0].lower()][0],16))
    def format2(self,index,ins):
        if ins[1][2] != "4":
            pass
        op_code = int(self.op_table[ins[index][0].lower()][0],16)
        r1 = int(self.reg_table[ins[index+1][0].upper()])
        if index+2<len(ins):
            r2 = int(self.reg_table[ins[index+3][0].upper()])
        else:
            r2 = 0
        return hex(op_code*0x100 + r1*0x10 +r2)
    def format3(self,index,ins):
        # addr
        # 1: immediate ex:#6,#<symbol>
        # 2: direct    ex:<symbol>, 0012
        # 3: indirect  ex:@<symbol>
        # 4: index     ex:<symbol>, X
        # 5: literal   ex:X'F1'
        n=0
        i=0
        x=0
        b=0
        p=0
        e=0
        disp = 0
        if ins[1][4] == "1":
            i=1
            if ins[1][2] == "2":
                disp = int(ins[index+2][0])
            elif ins[1][2] == "3":
                disp = self.symbol_table[ins[index+2][0]]-self.pc
                if -2048<=disp and disp<2047:
                    p=1
                else:
                    b=1
                    disp = self.symbol_table[ins[index+2][0]]-self.base
        elif ins[1][4] == "2":
            n=1
            i=1
            if ins[1][2] == "2":
                disp = int(ins[index+1][0])
            elif ins[1][2] == "3":
                disp = self.symbol_table[ins[index+1][0]]-self.pc
                if -2048<=disp and disp<2047:
                    p=1
                else:
                    b=1
                    disp = self.symbol_table[ins[index+1][0]]-self.base
        elif ins[1][4] == "3":
            n=1
            if ins[1][2] == "2":
                disp = int(ins[index+2][0])
            elif ins[1][2] == "3":
                disp = self.symbol_table[ins[index+2][0]]-self.pc
                if -2048<=disp and disp<2047:
                    p=1
                else:
                    b=1
                    disp = self.symbol_table[ins[index+2][0]]-self.base
        elif ins[1][4] == "4":
            n=1
            i=1
            x=1
            if ins[1][2] == "7":
                disp = self.symbol_table[ins[index+1][0]]-self.pc
                if -2048<=disp and disp<2047:
                    p=1
                else:
                    b=1
                    disp = self.symbol_table[ins[index+1][0]]-self.base
        elif ins[1][4] == "5":
            n=1
            i=1
            p=1
            if ins[1][2] == "2"or ins[1][2] == "8":        
                symbol ="="+ins[index+2][0]+ins[index+3][0]+ins[index+4][0]
            if ins[1][2] == "6":
                symbol ="="+ins[index+2][0]
            disp =self.symbol_table[symbol]-ins[0][0]-ins[0][1]
        elif ins[1][4] == "0":
            n=1
            i=1
        if disp<0:
            disp = 0xFFF+disp+0x1
        op_code = int(self.op_table[ins[index][0].lower()][0],16)

        return hex(op_code*0x10000 + n*0x20000 + i*0x10000 + x*0x8000 + b*0x4000 + p*0x2000 + e*0x1000 + disp)
    def format4(self,index,ins):
        # addr
        # 1: immediate ex:#6,#<symbol>
        # 2: direct    ex:<symbol>, 0012
        # 3: indirect  ex:@<symbol>
        # 4: index     ex:<symbol>, X
        # 5: literal   ex:X'F1'
        n=0
        i=0
        x=0
        b=0
        p=0
        e=1
        addr = 0
        if ins[1][4] == "1":
            i=1
            if ins[1][2] == "2":
                addr = int(ins[index+2][0])
            elif ins[1][2] == "3":
                addr = self.symbol_table[ins[index+2][0]]
        elif ins[1][4] == "3":
            n=1
        elif ins[1][4] == "2":
            n=1
            i=1
            if ins[1][2] == "2":
                addr = int(ins[index+1][0])
            elif ins[1][2] == "3":
                addr = self.symbol_table[ins[index+1][0]]
        elif ins[1][4] == "4":
            n=1
            i=1
            x=1
            if ins[1][2] == "7":
                addr = self.symbol_table[ins[index+1][0]]
        elif ins[1][4] == "5":
            n=1
            i=1
            if ins[1][2] == "2"or ins[1][2] == "8":        
                symbol ="="+ins[index][0]+ins[index+1][0]+ins[index+2][0]
            if ins[1][2] == "6":
                symbol ="="+ins[index][0]
            addr =self.symbol_table[symbol]
        elif ins[1][4] == "0":
            n=1
            i=1
        op_code = int(self.op_table[ins[index][0].lower()][0],16)

        return hex(op_code*0x1000000 + n*0x2000000 + i*0x1000000 + x*0x800000 + b*0x400000 + p*0x200000 + e*0x100000 + addr)
    def pesudo_obj(self,index, ins):
        if ins[index][0] == "BYTE" :
            obj_code = 0
            if index+2<len(ins) and ins[index+2][1] == "6":
                obj_code = int(ins[index+2][0],16)
            elif ins[index+1][1] == "6":
                obj_code = int(ins[index+1][0],16)
            else:
                for ch in list(ins[index+2][0].encode("ascii")):
                    obj_code = obj_code*0x100+int(ch)
            return hex(obj_code)
        elif ins[index][0] == "WORD" :
            return hex(int(ins[index+1][0]))
        elif ins[index][0] == "BASE" :
            self.base = self.symbol_table[ins[index+1][0]]
        return "0"

    def set_ins_len(self, ins):

        ins_info = [0x0,0x0,"0","0"]
        ins_info[0] = self.pc
        if ins[0][0] == "1":
            if ins[0][1] == "1":
                ins_info[3] = "6"
                ins_info[1] = self.get_ins_len(ins_info[3],ins)
                    
            elif ins[0][1] == "2":        #hould be pesudo
                ins_info[1] = self.pesudo_code(2,ins, ins_info)
                ins_info[3] = "5"
        else:
            if ins[0][1] == "1":
                ins_info[3] = "6"
                ins_info[1] = self.get_ins_len(ins_info[3],ins)
                    
            elif ins[0][1] == "2":        #operand
                ins_info[1] = self.pesudo_code(1,ins, ins_info)
                ins_info[3] = "5"
        self.pc = self.pc +ins_info[1]
        ins.insert(0,ins_info)


    def set_ins_len_XE(self,ins):

        ins_info = [0x0,0x0,"0","0"]
        ins_info[0] = self.pc
        if ins[0][0] == "1":              #with symbol
            if ins[0][1] == "1":
                ins_info[3] = self.op_table[ins[2][0].lower()][1]
                if ins[0][4] == "5":
                    if ins[0][2] == "2"or ins[0][2] == "8":
                        self.literal_table.append(self.update_literal_table(4,ins))
                ins_info[1] = self.get_ins_len(ins_info[3],ins)
                    
            elif ins[0][1] == "2":        #pesudo
                ins_info[1] = self.pesudo_code(2,ins, ins_info)
                ins_info[3] = "5"
            elif ins[0][1] == "3": 
                ins_info[3] = self.op_table[ins[3][0].lower()][1]
                if ins_info[3] == "3":
                    if ins[0][1] == "3":
                        ins_info[3] = "4"
                if ins[0][4] == "5":
                    self.literal_table.append(self.update_literal_table(4,ins))
                ins_info[1] = self.get_ins_len(ins_info[3],ins)
        
        else:
            if ins[0][1] == "1":          
                ins_info[3] = self.op_table[ins[1][0].lower()][1]
                if ins[0][4] == "5":
                    self.literal_table.append(self.update_literal_table(3,ins))
                ins_info[1] = self.get_ins_len(ins_info[3],ins)
                    
            elif ins[0][1] == "2":        #pesudo
                ins_info[1] = self.pesudo_code(1,ins, ins_info)
                ins_info[3] = "5"
            elif ins[0][1] == "3": 
                ins_info[3] = self.op_table[ins[2][0].lower()][1]
                if ins_info[3] == "3":
                    if ins[0][1] == "3":
                        ins_info[3] = "4"
                if ins[0][4] == "5":
                    self.literal_table.append(self.update_literal_table(3,ins))
                ins_info[1] = self.get_ins_len(ins_info[3],ins)
        
        
        self.pc = self.pc +ins_info[1]
        ins.insert(0,ins_info)


    def get_ins_len(self,format,ins):
        if format == "0":
            if len(ins) == 1:
                return 0x0
        if format == "1":
            return 0x1
        if format == "2":
            return 0x2
        if format == "3":
            return 0x3
        if format == "4":
            return 0x4
        if format == "6":
            return 3
        return 0


    def pesudo_code(self, index, ins, ins_info):
        ins[index][0] = ins[index][0].upper()
        if ins[index][0] == "START":
            self.pc = int(ins[index+1][0],16)
            self.start = self.pc
            ins_info[0] = self.pc
            return 0
        if ins[index][0] == "END":
            for item in self.literal_table:
                test1 =self.instruction_list.index(ins)+1
                test = self.literal_table.pop(0)
                test[0][0] = self.pc
                if self.symbol_table.get(test[2][0]) is None:
                    self.symbol_table[test[2][0]] = test[0][0]
                    self.instruction_list.insert(self.instruction_list.index(ins)+1,test)
                    self.pc+=test[0][1]
            return 0
        if ins[index][0] == "BYTE":
            if ins[0][2] == "2" or ins[0][2] == "8":
                if ins[index+1][1] == "6":
                    return int((len(ins[index+1][0])+1)/2)
                if ins[index+2][1] == "6":
                    return int((len(ins[index+2][0])+1)/2)
                if ins[index+2][1] == "7":
                    return len(ins[index+2][0])
        if ins[index][0] == "WORD":
            if ins[0][2] == "2" or ins[0][2] == "8":
                return 3
        if ins[index][0] == "RESB":
            self.pc = self.pc + int(ins[index+1][0])
            return 0
        if ins[index][0] == "RESW":
            self.pc = self.pc+int(ins[index+1][0])*3
            return 0
        if ins[index][0] == "EQU":
            if ins[index+1][0] == "*":
                pass
            elif ins[index+1][1] == "6":
                ins_info[0] = int(ins[index+1][0])
            elif ins[index+1][1] == "5":
                if index+2 < len(ins):
                    ins_info[0] = self.symbol_couculate(index+1,ins)
                else :
                    ins_info[0] = self.symbol_table[ins[index+1][0]]

            self.symbol_table[ins[index-1][0]] = ins_info[0]
            return 0
        if ins[index][0] == "BASE":
            return 0
        if ins[index][0] == "LTORG":
            for item in self.literal_table:
                test1 =self.instruction_list.index(ins)+1
                test = self.literal_table.pop(0)
                test[0][0] = self.pc
                if self.symbol_table.get(test[2][0]) is None:
                    self.symbol_table[test[2][0]] = test[0][0]
                    self.instruction_list.insert(self.instruction_list.index(ins)+1,test)
                    self.pc+=test[0][1]
                
            return 0

    def update_literal_table(self,index,ins):
        if ins[0][2] == "2"or ins[0][2] == "8":
            if ins[0][2] == "2":
                ins_temp = [[0,int((len(ins[index+1][0])+1)/2),"0","0"],["1","4","2","0","0"]]
            else:
                ins_temp = [[0,len(ins[index+1][0]),"0","0"],["1","4","8","0","0"]]
            ins_temp.append(["="+ins[index][0]+ins[index+1][0]+ins[index+2][0],"5","0"])
            for item in ins[index:]:
                ins_temp.append(item)
        if ins[0][2] == "6":
            ins_temp = [[0,0,"0","0"],["1","4","6","0","0"],"="+ins[index][0],ins[index]]
        return ins_temp

    def symbol_couculate(self,index,ins):
        if index+1 == len(ins):
            return self.symbol_table[ins[index][0]]
        elif ins[index+1][0] == "+":
            return self.symbol_table[ins[index][0]] + self.symbol_table[ins[index+2][0]]
        elif ins[index+1][0] == "-":
            return self.symbol_table[ins[index][0]] - self.symbol_table[ins[index+2][0]]
        elif ins[index+1][0] == "*":
            return self.symbol_table[ins[index][0]] * self.symbol_table[ins[index+2][0]]
        elif ins[index+1][0] == "/":
            return self.symbol_table[ins[index][0]] / self.symbol_table[ins[index+2][0]]
    def test(self):
        for ins in self.instruction_list:
            if ins[0][3] =="3":
                print(hex(ins[0][0])+"  ",end ="")
                print(ins)
    def print(self):
        line_count = 5
        print("Line  Loc   Source statement                          Object code")
        print("----  ----  -------------------------                 -----------")
        for ins in self.instruction_list:
            temp = ""
            t_num = 0
            if len(ins) == 2:
                print()
                line_count-=5
            elif ins[2][0] == ".":
                print('{0:>4}'.format(line_count),end="")
                for token in ins[2:]:
                    print(" "+token[0],end="")
                print()
            else:
                if ins[1][1] == "4":
                        line_count-=5
                else:
                    print('{0:>4}'.format(line_count),end="")
                if ins[2][0] != "END":
                    print("  "+'{0:0>4}'.format(hex(ins[0][0]).removeprefix("0x").upper()),end="  ")
                else:
                    print("        ",end="")
                if ins[2][1] == "5":
                    print('{0:<15}'.format(ins[2][0]),end="")
                    i = 3
                else:
                    print('{0:<15}'.format(""),end="")
                    i = 2
                if ins[i][0] == "+":
                    print(ins[i][0],end="")
                    t_num = 1
                    i+=1
                print('{0:<{width}}'.format(ins[i][0],width =10-t_num),end="")
                if i+1 < len(ins) and ins[i+1][0] =="\'" and ins[i+2][1] == "6" :
                        temp = temp+"X"
                if i+1 < len(ins) and ins[i+1][0] =="\'" and ins[i+2][1] == "7":
                        temp = temp+"C"
                for token in ins[i+1:]:
                    temp = temp+token[0]
                print('{0:<17}'.format(temp),end="") 
                if ins[0][1] !=0:
                    print('{0:0>{width}}'.format(ins[0][2].removeprefix("0x").upper(),width=ins[0][1]*2),end="")
                print()
            line_count +=5


    def write(self,filename):
        with open(filename,"w") as outfile:
            line_count = 5
            outfile.write("Line  Loc   Source statement                          Object code\n")
            outfile.write("----  ----  -------------------------                 -----------\n")
            for ins in self.instruction_list:
                temp = ""
                t_num = 0
                if len(ins) == 2:
                    outfile.write("\n")
                    line_count-=5
                elif ins[2][0] == ".":
                    outfile.write('{0:>4}'.format(line_count))
                    for token in ins[2:]:
                        outfile.write(" "+token[0])
                    outfile.write("\n")
                else:
                    if ins[1][1] == "4":
                        line_count-=5
                    else:
                        outfile.write('{0:>4}'.format(line_count))
                    if ins[2][0] != "END":
                        outfile.write("  "+'{0:0>4}'.format(hex(ins[0][0]).removeprefix("0x").upper())+"  ")
                    else:
                        outfile.write("        ")
                    if ins[2][1] == "5":
                        outfile.write('{0:<15}'.format(ins[2][0]))
                        i = 3
                    else:
                        outfile.write('{0:<15}'.format(""))
                        i = 2
                    if ins[i][0] == "+":
                        outfile.write(ins[i][0])
                        t_num = 1
                        i+=1
                    outfile.write('{0:<{width}}'.format(ins[i][0],width =10-t_num))
                    if i+1 < len(ins) and ins[i+1][0] =="\'" and ins[i+2][1] == "6" :
                            temp = temp+"X"
                    if i+1 < len(ins) and ins[i+1][0] =="\'" and ins[i+2][1] == "7":
                            temp = temp+"C"
                    for token in ins[i+1:]:
                        temp = temp+token[0]
                    outfile.write('{0:<17}'.format(temp)) 
                    if ins[0][1] !=0:
                        outfile.write('{0:0>{width}}'.format(ins[0][2].removeprefix("0x").upper(),width=ins[0][1]*2))
                    outfile.write("\n")
                line_count +=5




class Interface:
    def __init__(self):
        self.filename = ""
        self.print=False
        self.using_SICXE = False
        self.tc = Token_Cutter()
        self.anal = Analyzer()
        self.assembler = Assembler()

    def clear(self):
        self.tc.clear()
        self.anal.clear()
        self.assembler.clear()
    def select_file(self):
        files = listdir("./")
        for f in files:
            print(f)
        print("Above is files in floder") 
        print("Enter progame filename")
        print("EX: input101(only accept .txt file)")
        self.filename = input(":")
        try:
            open(self.filename+".txt") 
        except:
            print("No such a file")
            system("pause")
            self.select_file() 
        print()

    def choose_screen_print(self):
        print("Choosing print obj code on screen or not")
        print("Enter number( 1, 2 )")
        print("1.YES")
        print("2.NO")
        choose = input(":")
        if choose == "1":
            self.print = True
        else:
            self.print = False
    def select_mode(self):
        print("Choosing instruction type used by programmer")
        print("Enter number( 1, 2 )")
        print("1.SIC")
        print("2.SICXE")
        choose = input(":")
        if choose =="2":
            self.using_SICXE = True
    def continue_or_not(self):
        print("Continue_or_not")
        print("Enter number( 0, 1 )") 
        print("0. To Exit")
        print("1. to continue")
        exit = input(":")

        if exit == "0":
            print(_exit(0))
        elif exit == "1":
            pass
        else:
            self.continue_or_not()
        


    def compile(self):
        self.anal.instruction_list = self.tc.get_token(self.filename+".txt")
        self.assembler.instruction_list = self.anal.analze()
        self.assembler.generate_obj_code(self.using_SICXE)
        if self.print:
            self.assembler.print()
        self.assembler.write(self.filename +"_out.txt")
        self.continue_or_not()
        self.clear()
        
    

# test section
tk = Token_Cutter()


tk.get_token("./Example/input.txt")



entry = Interface()
while(1):
    entry.select_file()
    entry.select_mode()
    entry.choose_screen_print()
    entry.compile()