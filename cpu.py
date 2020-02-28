"""CPU functionality."""

import sys

# Hardcode variables for branch table
# LDI = 0b10000010
# PRN = 0b01000111
# HLT = 0b00000001
# MUL = 0b10100010
# CMP = 0b10100111

# R7 Stack Pointer
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Ram 256 byte size
        self.ram = [0] * 256
        self.reg = [0] * 8
        # Internal Registers
        self.pc = 0  # counter
        self.sp = 7
        self.fl = 0b00000000  # Holds current flag status
        self.running = True

        def LDI(operand_a, operand_b):
            # Insert a decimal integer into a register
            self.reg[operand_a] = operand_b
            self.pc += 3

        def PRN(operand_a, operand_b):
            # Print to the console the decimal integer value that is
            # stored in the given register.
            print(self.reg[operand_a])
            self.pc += 2

        def HLT(operand_a, operand_b):
            # Halt the CPU (and exit the emulator)
            self.running = False

        def CALL(operand_a, operand_b):
            # Push return address onto the stack
            return_address = self.pc + 2
            self.reg[self.sp] -= 1
            self.ram[self.reg[self.sp]] = return_address
            # Set PC to the value in the register
            self.pc = self.reg[operand_a]

        def MUL(operand_a, operand_b):
            self.alu('MUL', operand_a, operand_b)
            self.pc += 3

        def JMP(operand_a, operand_b):
            # go to the address stored in the given register .Set to address stored in the given register.
            self.pc = self.reg[operand_a]

        def JEQ(operand_a, operand_b):
                # If equal flag is set (true), jump to the address stored in the
            if self.fl == 0b00000001:
                JMP(operand_a, operand_b)
            else:
                self.pc += 2

        def JNE(operand_a, operand_b):
            # If E flag is clear (false, 0), jump to the address stored in
            if self.fl != 0b00000001:
                JMP(operand_a, operand_b)
            else:
                self.pc += 2

        def CMP(operand_a, operand_b):
            self.alu('CMP', operand_a, operand_b)
            self.pc += 3
        self.op_codes = {
            0b10000010: LDI,
            0b01000111: PRN,
            0b00000001: HLT,
            0b10100010: MUL,
            0b01010000: CALL,
            0b10100111: CMP,
            0b01010100: JMP,
            0b01010101: JEQ,
            0b01010110: JNE,
        }

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print('Usage: file.py <filename>', file=sys.stderr)
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split('#')
                    num = comment_split[0].strip()

                    if num == '':
                        # Ignore blank lines
                        continue

                    value = int(num, 2)
                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found.')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:
                # Set to 1 if A is less than B else 0
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                # Set to 1 if A is greater than B else 0
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                # Set to 1 if A is equal to B else 0
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        while self.running:
            # Instruction Register (IR)
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # Find opcode name of IR
            opcode = self.op_codes[IR]

            if opcode:
                opcode(operand_a, operand_b)
            else:
                print(f'Error: Unknown command: {IR}')
                sys.exit(1)
