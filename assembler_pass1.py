# assembler_pass1.py
class AssemblerPass1:
    def __init__(self):
        self.symtab = {}

    def run(self, source_code):
        self.symtab = {}
        locctr = 0x1000  # 預設起始位址
        lines = source_code.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('.'):
                continue
            tokens = line.split()
            
            # 處理 START directive
            if len(tokens) >= 3 and tokens[1] == 'START':
                locctr = int(tokens[2], 16)
                continue
            
            # 如果這行有 Label
            if len(tokens) > 0 and not line.startswith(' '):
                label = tokens[0]
                if label not in ['END', 'BASE']:
                    self.symtab[label] = f"{locctr:06X}"
                
            # 計算定址增量 (LOCCTR)
            if len(tokens) >= 2:
                opcode = tokens[1] if not line.startswith(' ') else tokens[0]
                if opcode == 'RESW':
                    size = int(tokens[2] if not line.startswith(' ') else tokens[1])
                    locctr += 3 * size
                elif opcode == 'RESB':
                    size = int(tokens[2] if not line.startswith(' ') else tokens[1])
                    locctr += size
                elif opcode in ['WORD', 'BYTE']:
                    locctr += 3
                elif opcode not in ['START', 'END', 'BASE', 'MACRO', 'MEND', 'EQU']:
                    locctr += 3
        return self.symtab