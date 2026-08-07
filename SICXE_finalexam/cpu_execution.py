class CPUExecution:
    def execute_step(self, machine):
        """Fetches the next instruction and executes it."""
        pc = machine.registers['PC']
        opcode = machine.memory[pc]
        target = (machine.memory[pc+1] << 8) | machine.memory[pc+2]

        
        if opcode == 0x14: 
            machine.registers['L'] = target  # STL
        elif opcode == 0x48: 
            machine.registers['S'] = target  # JSUB
        elif opcode == 0x00: 
            machine.registers['A'] = target  # LDA
        
       
        machine.registers['PC'] += 3
        return f"{opcode:02X}{target:04X}"