from hardware import Memory, RegisterFile, Register, MUX_2_1, ALU_32, AND_2
import utilities
from signals import Signals

class Core_SC:
    def __init__(self):
        self.I_Mem = Memory()
        self.D_Mem = Memory()
        self.RF = RegisterFile()
        self.RegPC = Register()
        self.signals = Signals()
        self.cycle_num = 0
        self.mode = 0

    def set_PC(self, pc):
        self.RegPC.set_data(pc)
        self.RegPC.set_write(1)

    def set_mode(self, mode):
        self.mode = mode

    def run(self, n_cycles):
        i_cycles = 0
        ending_PC = self.I_Mem.get_ending_address()

        self.I_Mem.set_memread(1)
        self.I_Mem.set_memwrite(0)

        while (n_cycles == 0 or i_cycles < n_cycles):
            i_cycles += 1
            self.cycle_num += 1
            if ((self.mode & 2) == 0): utilities.print_new_cycle(self.cycle_num)

            # clock changes
            self.RegPC.clock()
            self.RF.clock()

            # read PC
            self.signals.PC = self.RegPC.read()
            self.signals.PC_4 = self.signals.PC_new = self.signals.PC + 4
            if ((self.mode & 2) == 0): utilities.println_int("PC", self.signals.PC)
            if (self.signals.PC > ending_PC):
                if ((self.mode & 2) == 0): print("No More Instructions")
                i_cycles -= 1
                break

            self.I_Mem.set_address(self.signals.PC)
            self.I_Mem.run()
            self.signals.instruction = self.I_Mem.get_data()

            if ((self.mode & 2) == 0): utilities.println_int("instruction", self.signals.instruction)

            # Now you have PC and the instruction
            # Some signals' value can be extracted from instruction directly
            self.signals_from_instruction(self.signals.instruction, self.signals)

            # call main_control
            self.main_control(self.signals.opcode, self.signals)

            # call sign_extend
            self.signals.Sign_extended_immediate = self.sign_extend(self.signals.immediate)

            # Write_register. Also an example of using MUX
            self.signals.Write_register = MUX_2_1(self.signals.rt, self.signals.rd, self.signals.RegDst)

            # ALU control
            self.signals.ALU_operation = self.ALU_control(self.signals.ALUOp, self.signals.funct)

            # Calculate branch address
            self.signals.Branch_address = self.calculate_branch_address(self.signals.PC_4, self.signals.Sign_extended_immediate)
            self.signals.Jump_address = self.calculate_jump_address(self.signals.PC_4, self.signals.instruction)

            # Print out signals generated in Phase 1.
            if ((self.mode & 4) == 0): utilities.print_signals_1(self.signals)

            # If phase 1 only, continue to the next instruction.
            if ((self.mode & 1) != 0):
                self.RegPC.set_data(self.signals.PC_4)
                self.RegPC.set_write(1)
                continue

### PHASE 2 CHANGES ###
            # You will continue to complete the core in phase 2
            # Use RF, ALU, D_Mem
            # Preapre RF write
            # Compute PC_new

            #EW: reading the register RegisterFile
            self.RF.set_read_registers(self.signals.rs,self.signals.rt)
            #reading data from both registers
            self.signals.RF_read_data_1 = self.RF.get_read_data_1()
            self.signals.RF_read_data_2 = self.RF.get_read_data_2()

            #EW: using the ALU - calling with proper input
            self.signals.ALU_input_2 = MUX_2_1(self.signals.RF_read_data_2,self.signals.Sign_extended_immediate,self.signals.ALUSrc)
            #EW: retrieving the output, preivously imported at top: ALU_32
            self.signals.ALU_returned_value = ALU_32(self.signals.RF_read_data_1,self.signals.ALU_input_2,self.ALU_control(self.signals.ALUOp,self.signals.funct))

            #EW: ALU Results
            self.signals.ALU_result = self.signals.ALU_returned_value[0]
            self.signals.Zero = self.signals.ALU_returned_value[1]

            #EW: Accessing Data Memory - takes in two inputs: (address, write data)
            self.D_Mem.set_address(self.signals.ALU_result)
            #error here
            self.D_Mem.set_data(self.signals.RF_read_data_2)

            #EW:  set signals - Data Memory
            self.D_Mem.set_memread(self.signals.MemRead)
            self.D_Mem.set_memwrite(self.signals.MemWrite)

            #EW: call D_MEM using run()
            self.D_Mem.run()
            #EW:  Output from call
            self.signals.MEM_read_data = self.D_Mem.get_data()
            self.signals.Write_data = MUX_2_1(self.signals.ALU_result,self.signals.MEM_read_data,self.signals.MemtoReg)

            #EW: Preparing - write back with RF.set_write
            self.RF.set_write_register(self.signals.Write_register)
            self.RF.set_write_data(self.signals.Write_data)
            self.RF.set_regwrite(self.signals.RegWrite)

            #EW: compute PC_new
            self.signals.PCSrc = AND_2(self.signals.Branch, self.signals.Zero)
            self.signals.PC_branch = MUX_2_1(self.signals.PC_4, self.signals.Branch_address, self.signals.PCSrc)
            self.signals.PC_new = MUX_2_1(self.signals.PC_branch, self.signals.Jump_address, self.signals.Jump)

            #EW: set_data & set_write before print and return
            self.RegPC.set_data(self.signals.PC_new)
            self.RegPC.set_write(1)

            # Print out signals generated in Phase 2.
            if ((self.mode & 8) == 0): utilities.print_signals_2(self.signals)
        return i_cycles
        

### PHASE 1 CHANGES ###

    def signals_from_instruction (self, instruction, sig):
        """
        Extract the following signals from instruction.
            opcode, rs, rt, rd, funct, immediate
        """
        sig.opcode = (instruction >> 26) & 0x3F     # opcode bits 31-26, 6 bits
        sig.rs = (instruction >> 21) & 0x1F         # rs bits 25-21, 5 bits
        sig.rt = (instruction >> 16) & 0x1F         # rt bits 20-16 5 bits
        sig.rd = (instruction >> 11) & 0x1F         # rd bits 15-11 5 bits
        sig.shamt = (instruction >> 6) & 0x1F       # shamt bits 10-6 5 bits
        sig.funct = instruction & 0x3F              # func bits 5-0 6 bits
        sig.immediate = instruction & 0xFFFF        # if none R-Type, load immediate

    def main_control(self, opcode, sig):
        """
        Check the type of input instruction
        """
        #set defaults for control signals
        sig.RegDst = sig.Jump = sig.Branch = sig.MemRead = sig.MemtoReg = sig.ALUOp = sig.MemWrite = sig.ALUSrc = sig.RegWrite = 0
        #determine control signals
        if opcode == 0:             # R-Type 000000
            sig.RegWrite = 1
            sig.RegDst = 1
            sig.ALUOp = 2
        elif opcode == 8:
            sig.RegWrite = 1
            sig.ALUOp = 0
            sig.ALUSrc = 1
        elif opcode == 35:
            sig.RegWrite = 1
            sig.MemRead = 1
            sig.MemtoReg = 1
            sig.ALUSrc = 1
            sig.ALUOp = 0
        elif opcode == 43:
            sig.ALUSrc = 1
            sig.MemWrite = 1
            sig.ALUOp = 0
        elif opcode == 4:
            sig.Branch = 1
            sig.ALUOp = 1
        elif opcode == 2:
            sig.Jump = 1
        else:
            raise ValueError("Unknown opcode 0x%02X" % opcode)
        return

    def ALU_control(self, alu_op, funct):
        """
        Get alu_control from func field of instruction
        Input: function field of instruction
        Output: alu_control_out

        """
        alu_control_out = 0
        # One example is given, continue to finish other cases.
        if alu_op == 0:             # 00
            alu_control_out = 2     # 0010
        elif alu_op == 1:
            alu_control_out = 6
        elif alu_op == 2:
            if funct == 32:
                alu_control_out = 2
            elif funct == 34:
                alu_control_out = 6
            elif funct == 36:
                alu_control_out = 0
            elif funct == 37:
                alu_control_out = 1
            elif funct == 42:
                alu_control_out = 7
        else:
            raise ValueError("Unknown opcode code 0x%02X" % alu_op)
        return alu_control_out

    def sign_extend(self, immd):
        """
        Sign extend module.
        Convert 16-bit to an int.
        Extract the lower 16 bits.
        If bit 15 of immd is 1, compute the correct negative value (immd - 0x10000).
        """
        immd = immd & 0xFFFF #first 16 bits
        if immd & 0x8000: #if it is negative
            immd = immd - 0x10000

        return immd

    def calculate_branch_address(self, pc_4, extended):
        addr = 0
        extended = extended << 2                    # the calculated addresses is the jump immedate SL2 + PC+4
        addr = pc_4 + extended
        return addr

    def calculate_jump_address(self, pc_4, instruction):
        addr = 0
        instruction = instruction & 0x3FFFFFF       # the jump immediate
        instruction = instruction << 2
        pc_4 =  pc_4 & 0XF0000000                   # first 4 bits from next line for new PC
        addr  = pc_4 + instruction                  # SL2, convert to word
        return addr

def __main__():
    pass
