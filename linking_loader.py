class LinkingLoader:
    def load_to_memory(self, machine, object_code, start_addr):
        """Writes the object code into the machine's memory array."""
        for i in range(0, len(object_code), 2):
            byte = int(object_code[i:i+2], 16)
            machine.memory[start_addr + (i // 2)] = byte
        

        machine.registers['PC'] = start_addr
        print(f"Loader: Program linked at address {hex(start_addr)}.")