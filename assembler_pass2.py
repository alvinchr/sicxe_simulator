# assembler_pass2.py
class AssemblerPass2:
    def run(self, source_code, symtab):
        # 建立簡單指令對應的基底機器碼映射 (OPTAB)
        optab = {'LDA': '00', 'STA': '0C', 'ADD': '18', 'SUB': '1C', 'COMP': '28', 'JGT': '34', 'J': '3C', 'JSUB': '48'}
        object_code_list = []
        lines = source_code.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('.') or 'START' in line or 'END' in line or 'RESW' in line or 'EQU' in line or 'MACRO' in line:
                continue
            tokens = line.split()
            
            # 取得目前的指令和參數
            if not line.startswith(' ') and len(tokens) >= 3:
                opcode, operand = tokens[1], tokens[2]
            else:
                opcode = tokens[0]
                operand = tokens[1] if len(tokens) > 1 else ""
                
            if opcode in optab:
                op_hex = optab[opcode]
                # 處理立即定址 (如 #5)
                if operand.startswith('#'):
                    val = int(operand[1:])
                    addr_hex = f"{val:04X}"
                # 處理變數符號定址
                elif operand in symtab:
                    addr_hex = symtab[operand][-4:]
                else:
                    addr_hex = "0000"
                object_code_list.append(f"{op_hex}{addr_hex}")
                
        return ''.join(object_code_list)