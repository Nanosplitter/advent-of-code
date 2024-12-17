import sys

A = 'a'
B = 'b'
C = 'c'

class Computer:
    def __init__(self):
        self.registers = {
            A: 0,
            B: 0,
            C: 0,
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

    def bxc(self):
        self.registers[B] = self.registers[B] ^ self.registers[C]

    def out(self, operand):
        self.output.append(self.get_combo(operand) % 8)

    def bdv(self, operand):
        denominator = 2 ** self.get_combo(operand)
        self.registers[B] = self.registers[A] // denominator

    def cdv(self, operand):
        denominator = 2 ** self.get_combo(operand)
        self.registers[C] = self.registers[A] // denominator

    def run(self, program, a=None):
        if a is not None:
            self.registers[A] = a
        self.registers[B] = 0
        self.registers[C] = 0
        
        self.output = []
        self.pointer = 0

        while self.pointer < len(program):
            opcode = program[self.pointer]
            operand = program[self.pointer + 1]
            
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
            self.bxc()
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)

def part1(a, program) -> str:
    computer = Computer()
    
    return ','.join(map(str, computer.run(program, a)))

def part2(program) -> int:
    computer = Computer()
    a = 0
    
    for current_instruction in range(1, len(program) + 1):
        target = program[len(program) - current_instruction:]
        a *= 8
        while True:
            if computer.run(program, a) == target:
                print(a, computer.output)
                break
            
            a += 1
            
    return a

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()
    
    a = int(lines[0].split(':')[1].strip())
    program = list(map(int, lines[4].split(":")[1].strip().split(',')))
    
    print(part1(a, program))
    print(part2(program))

