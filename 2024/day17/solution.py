import sys

A = 'a'
B = 'b'
C = 'c'

class Computer:
    def __init__(self, a=0, b=0, c=0):
        self.registers = {
            'a': a,
            'b': b,
            'c': c,
        }
        
        self.pointer = 0
        self.output = []
    
    def get_combo(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.registers['a']
        elif operand == 5:
            return self.registers['b']
        elif operand == 6:
            return self.registers['c']
        else:
            raise ValueError("Invalid combo operand")
    
    def adv(self, operand):
        operand = self.get_combo(operand)
        self.registers[A] = self.registers[A] // (2 ** operand)
    
    def bxl(self, operand):
        self.registers[B] = self.registers[B] ^ self.get_combo(operand)
    
    def bst(self, operand):
        self.registers[B] = self.get_combo(operand) % 8
    
    def jnz(self, operand):
        if self.registers[A] != 0:
            self.pointer = operand
        else:
            self.pointer += 2

    def bxc(self, operand):
        self.registers[B] = self.registers[B] ^ self.registers[C]

    def out(self, operand):
        value = self.get_combo(operand) % 8
        self.output.append(value)

    def bdv(self, operand):
        denominator = 2 ** self.get_combo(operand)
        self.registers[B] = self.registers[A] // denominator

    def cdv(self, operand):
        denominator = 2 ** self.get_combo(operand)
        self.registers[C] = self.registers[A] // denominator

    def run(self, program, a=None, opcodes=None):
        if a is not None:
            self.registers[A] = a
        self.registers[B] = 0
        self.registers[C] = 0
        self.output = []
        self.pointer = 0

        if opcodes is None:
            opcodes = list(map(int, program.strip().split(',')))
        while self.pointer < len(opcodes):
            opcode = opcodes[self.pointer]
            operand = opcodes[self.pointer + 1] if self.pointer + 1 < len(opcodes) else 0
            self.execute(opcode, operand)

            if opcode != 3 or self.registers[A] == 0:
                self.pointer += 2
        
        return self.output

    def execute(self, opcode, operand):
        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            self.jnz(operand)
        elif opcode == 4:
            self.bxc(operand)
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)
        else:
            raise ValueError("Unknown opcode")

def part1(a, instructions) -> str:
    computer = Computer(a)
    computer.run(instructions)
    return ','.join(map(str, computer.output))

def part2(a, instructions) -> int:
    pre_parsed_opcodes = list(map(int, instructions.split(',')))
    test_instructions = pre_parsed_opcodes.copy()
    
    print(test_instructions)
    
    test_value = 0
    
    computer = Computer()
    
    
    while computer.run(None, test_value, opcodes=pre_parsed_opcodes) != test_instructions:
        #print(test_value)
        test_value += 1
    
    return test_value
    
    

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()
    a = int(lines[0].split(':')[1].strip())
    program_line = next((line for line in lines if line.startswith('Program:')), None)
    if program_line:
        program = program_line.split(':')[1].strip()
    else:
        program = ''
    
    print(part1(a, program))
    print(part2(a, program))

