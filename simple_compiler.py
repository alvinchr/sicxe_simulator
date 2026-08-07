# simple_compiler.py
class SimpleCompiler:
    def __init__(self):
        self.symbol_table = set() # 儲存已宣告的變數名稱
        self.label_idx = 0

    def run(self, high_level_code_str):
        self.symbol_table.clear()
        self.label_idx = 0
        
        raw_lines = high_level_code_str.split('\n')
        asm_body = []
        variables_declaration = []
        
        # 預設產生 SIC/XE 開頭
        asm_body.append("PROG    START   1000")
        
        # 為了滿足測試案例 8：自動注入 INCR 巨集定義
        if "inc " in high_level_code_str:
            asm_body.append("INCR    MACRO   &VAR")
            asm_body.append("LDA     &VAR")
            asm_body.append("ADD     #1")
            asm_body.append("STA     &VAR")
            asm_body.append("MEND")

        for line in raw_lines:
            line = line.strip().replace(';', '')
            if not line:
                continue

            # 1. 處理變數宣告: int a
            if line.startswith("int "):
                var_name = line.split()[1]
                self.symbol_table.add(var_name)
                variables_declaration.append(f"{var_name.upper():8} RESW    1")
                continue

            # 2. 處理輸出敘述: print a
            if line.startswith("print "):
                var_name = line.split()[1]
                # 【測試案例 10】未宣告變數錯誤檢查
                if var_name not in self.symbol_table:
                    raise NameError(f"Error: Undefined variable {var_name}.")
                asm_body.append(f"    JSUB    PRINT")
                continue

            # 3. 處理巨集對應語法: inc x
            if line.startswith("inc "):
                var_name = line.split()[1]
                if var_name not in self.symbol_table:
                    raise NameError(f"Error: Undefined variable {var_name}.")
                asm_body.append(f"    INCR    {var_name.upper()}")
                continue

            # 4. 處理條件判斷: if a > b then
            if line.startswith("if ") and " > " in line and " then" in line:
                self.label_idx += 1
                parts = line.replace("if ", "").replace(" then", "").split(" > ")
                var1, var2 = parts[0].strip(), parts[1].strip()
                
                if var1 not in self.symbol_table or var2 not in self.symbol_table:
                    raise NameError(f"Error: Undefined variable in if condition.")
                
                asm_body.append(f"    LDA     {var1.upper()}")
                asm_body.append(f"    COMP    {var2.upper()}")
                asm_body.append(f"    JGT     THEN{self.label_idx}")
                asm_body.append(f"    J       ENDIF{self.label_idx}")
                asm_body.append(f"THEN{self.label_idx} EQU     *")
                continue

            if line == "endif":
                asm_body.append(f"ENDIF{self.label_idx} EQU     *")
                continue

            # 5. 處理指定敘述與算術運算: sum = a + b
            if "=" in line:
                parts = line.split("=")
                lhs = parts[0].strip()
                rhs = parts[1].strip()
                
                if lhs not in self.symbol_table:
                    raise NameError(f"錯誤: 變數有誤 請注意以定義變數.{lhs}.")

                # 情況 A: 純數值賦值 a = 5
                if rhs.isdigit():
                    asm_body.append(f"    LDA     #{rhs}")
                    asm_body.append(f"    STA     {lhs.upper()}")
                # 情況 B: 加法運算 sum = a + b
                elif "+" in rhs:
                    operands = rhs.split("+")
                    op1, op2 = operands[0].strip(), operands[1].strip()
                    if op1 not in self.symbol_table or op2 not in self.symbol_table:
                        raise NameError("錯誤: 算法變數有誤.")
                    asm_body.append(f"    LDA     {op1.upper()}")
                    asm_body.append(f"    ADD     {op2.upper()}")
                    asm_body.append(f"    STA     {lhs.upper()}")
                # 情況 C: 減法運算 result = a - b
                elif "-" in rhs:
                    operands = rhs.split("-")
                    op1, op2 = operands[0].strip(), operands[1].strip()
                    if op1 not in self.symbol_table or op2 not in self.symbol_table:
                        raise NameError("錯誤: 算法變數有誤.")
                    asm_body.append(f"    LDA     {op1.upper()}")
                    asm_body.append(f"    SUB     {op2.upper()}")
                    asm_body.append(f"    STA     {lhs.upper()}")

    
        asm_body.extend(variables_declaration)
        asm_body.append("END     PROG")
        return '\n'.join(asm_body)