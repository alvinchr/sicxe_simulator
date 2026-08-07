# macro_processor.py
import re

class MacroProcessor:
    def __init__(self):
        self.namtab = {}  # {'MACRONAME': {'args': ['&ARG1'], 'start': 0, 'end': 0}}
        self.deftab = []  # 儲存巨集定義內容的行陣列
        self.argtab = {}  # {'&ARG1': 'ACTUAL_VAL'}
        self.label_counter = 0

    def run(self, source_code_str):
        lines = [line.strip() for line in source_code_str.split('\n') if line.strip()]
        expanded_lines = []
        
        in_definition = False
        current_macro_name = None
        
        i = 0
        while i < len(lines):
            line = lines[i]
            # 移除註解
            if line.startswith('.'):
                i += 1
                continue
                
            tokens = line.split()
            if not tokens:
                i += 1
                continue

            # 偵測 MACRO 定義開始
            if len(tokens) >= 2 and tokens[1] == 'MACRO':
                in_definition = True
                current_macro_name = tokens[0]
                args = tokens[2].split(',') if len(tokens) > 2 else []
                
                self.namtab[current_macro_name] = {
                    'args': args,
                    'start_idx': len(self.deftab)
                }
                i += 1
                continue

            # 偵測 MEND 定義結束
            if tokens[0] == 'MEND':
                in_definition = False
                self.namtab[current_macro_name]['end_idx'] = len(self.deftab)
                i += 1
                continue

            # 如果正在讀取定義體，存入 DEFTAB
            if in_definition:
                self.deftab.append(line)
                i += 1
                continue

            # 檢查是否為巨集呼叫
            # 格式可能為: [Label] MACRONAME ARGS 或 MACRONAME ARGS
            macro_called = None
            actual_args_str = ""
            
            if tokens[0] in self.namtab:
                macro_called = tokens[0]
                actual_args_str = tokens[1] if len(tokens) > 1 else ""
            elif len(tokens) >= 2 and tokens[1] in self.namtab:
                macro_called = tokens[1]
                actual_args_str = tokens[2] if len(tokens) > 2 else ""

            if macro_called:
                macro_info = self.namtab[macro_called]
                expected_args = macro_info['args']
                actual_args = actual_args_str.split(',') if actual_args_str else []
                
                # 【測試案例 9】參數數量檢查錯誤機制
                if len(actual_args) != len(expected_args):
                    raise ValueError(f"Error: Macro {macro_called} expects {len(expected_args)} arguments, but got {len(actual_args)}.")

                # 建立 ARGTAB
                self.argtab = {expected_args[j]: actual_args[j] for j in range(len(expected_args))}
                
                # 進階加分功能：處理 Local Label ($開頭) 重複問題
                self.label_counter += 1
                local_label_map = {}

                # 從 DEFTAB 複製並展開
                for idx in range(macro_info['start_idx'], macro_info['end_idx']):
                    def_line = self.deftab[idx]
                    
                    # 替換參數
                    for param, val in self.argtab.items():
                        def_line = def_line.replace(param, val)
                    
                    # 替換 $開頭的 Local Label (例如 $LOOP -> $LOOP001)
                    local_labels = re.findall(r'\$[A-Za-z0-9]+', def_line)
                    for lbl in local_labels:
                        if lbl not in local_label_map:
                            local_label_map[lbl] = f"{lbl}{self.label_counter:03d}"
                        def_line = def_line.replace(lbl, local_label_map[lbl])
                        
                    expanded_lines.append(def_line)
                i += 1
                continue

            # 普通組語指令，直接保留
            expanded_lines.append(line)
            i += 1

        return '\n'.join(expanded_lines)