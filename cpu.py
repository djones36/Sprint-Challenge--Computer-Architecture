"""CPU functionality."""

import sys

# Hardcode variables for branch table
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
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
        self.ir = "00000000"
        # instruction set
        self.instruction = {}
        self.instruction[LDI] = self.handle_LDI
        self.instruction[PRN] = self.handle_PRN
        self.instruction[MUL] = self.handle_MUL

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0

            with open(program) as f:
                for line in f:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    value = int(num, 2)
                    self.ram_write(address, value)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.arg[0]}: {sys.arg[1]} not found")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self, operand_a, operand_b):
        print(f"Print to Console - {self.reg[operand_a]}")
        self.pc += 2

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def run(self):
        """Run the CPU."""

        running = True  # REPL  execution

        self.reg[SP] = 0xF4
        while running:
            # Start the CPU store instructions in IR
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if self.ir == HLT:
                running = False
                break
            # excecute instructions
            try:
                self.instruction[self.ir](operand_a, operand_b)
            except:
                print(f"Error: Unknown Command {self.ir}")
                sys.exit(1)
