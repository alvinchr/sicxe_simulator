# main_program.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QTextEdit, QTabWidget, QMessageBox)

from simple_compiler import SimpleCompiler
from macro_processor import MacroProcessor
from assembler_pass1 import AssemblerPass1
from assembler_pass2 import AssemblerPass2
from linking_loader import LinkingLoader
from cpu_execution import CPUExecution

class MachineState:
    def __init__(self):
        self.memory = bytearray(1024 * 1024) 
        self.registers = {'A':0, 'X':0, 'L':0, 'PC':0, 'SW':0, 'B':0, 'S':0, 'T':0}

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
   
        self.compiler = SimpleCompiler()
        self.macro_processor = MacroProcessor()
        self.machine = MachineState()
        self.pass1 = AssemblerPass1()
        self.pass2 = AssemblerPass2()
        self.loader = LinkingLoader()
        self.cpu = CPUExecution()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SIC/XE 整合型編譯與模擬系統")
        self.resize(900, 700)
        
        tabs = QTabWidget()
        
        # --- 分頁一：高階語言編譯與管線流水線展示 ---
        pipeline_widget = QWidget()
        pipeline_layout = QHBoxLayout()
        
        # 左側：高階語言輸入
        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("1. 高階語言輸入區 (High-Level Language Input):"))
        self.hl_input = QTextEdit()
        self.hl_input.setText("int a;\nint b;\nint sum;\n\na = ;\nb = ;\nsum = a + b;\nprint sum;")
        left_box.addWidget(self.hl_input)
        
        self.btn_pipeline = QPushButton("執行完整 Pipeline 轉譯工作流 🚀")
        self.btn_pipeline.setStyleSheet("font-weight: bold; font-size: 14px; background-color: #4CAF50; color: white; padding: 10px;")
        self.btn_pipeline.clicked.connect(self.process_pipeline)
        left_box.addWidget(self.btn_pipeline)
        pipeline_layout.addLayout(left_box, 1)
        
        # 右側：各階段輸出展示
        right_box = QVBoxLayout()
        right_box.addWidget(QLabel("2. Compiler 輸出 (Assembly with Macro):"))
        self.txt_compiler_out = QTextEdit()
        self.txt_compiler_out.setReadOnly(True)
        right_box.addWidget(self.txt_compiler_out)
        
        right_box.addWidget(QLabel("3. Macro Processor 展開結果 (Expanded Assembly):"))
        self.txt_macro_out = QTextEdit()
        self.txt_macro_out.setReadOnly(True)
        right_box.addWidget(self.txt_macro_out)
        
        right_box.addWidget(QLabel("4. Assembler 產生之目的碼 (Object Program):"))
        self.txt_object_out = QTextEdit()
        self.txt_object_out.setReadOnly(True)
        right_box.addWidget(self.txt_object_out)
        
        pipeline_layout.addLayout(right_box, 1)
        pipeline_widget.setLayout(pipeline_layout)
        
        # --- 分頁二：Simulator 執行狀態監控面板 ---
        sim_widget = QWidget()
        sim_layout = QHBoxLayout()
        
        # 左：暫存器表格
        sim_left = QVBoxLayout()
        sim_left.addWidget(QLabel("CPU 暫存器狀態 (Registers):"))
        self.table = QTableWidget(8, 2)
        self.table.setHorizontalHeaderLabels(["Register", "Value"])
        sim_left.addWidget(self.table)
        
        self.log_label = QLabel("系統狀態: 尚未載入程式")
        self.log_label.setStyleSheet("color: blue; font-weight: bold;")
        sim_left.addWidget(self.log_label)
        
        self.btn_step = QPushButton("單步執行 (Step)")
        self.btn_step.clicked.connect(self.run_step)
        sim_left.addWidget(self.btn_step)
        sim_layout.addLayout(sim_left, 1)
        
        sim_widget.setLayout(sim_layout)
        
        tabs.addTab(pipeline_widget, "編譯與管線流水線展示")
        tabs.addTab(sim_widget, "Simulator 執行面板")
        
        self.setCentralWidget(tabs)
        self.update_display()

    def process_pipeline(self):
        try:
            # Step 1: 簡易高階語言編譯
            hl_code = self.hl_input.toPlainText()
            asm_with_macro = self.compiler.run(hl_code)
            self.txt_compiler_out.setText(asm_with_macro)
            
            # Step 2: 巨集展開處理
            expanded_asm = self.macro_processor.run(asm_with_macro)
            self.txt_macro_out.setText(expanded_asm)
            
            # Step 3: 二階段組譯
            symtab = self.pass1.run(expanded_asm)
            object_code = self.pass2.run(expanded_asm, symtab)
            self.txt_object_out.setText(object_code)
            
            # Step 4: 載入器載入記憶體
            self.loader.load_to_memory(self.machine, object_code, 0x1000)
            self.update_display()
            self.log_label.setText("系統狀態: 載入完成，隨時可以執行！")
            
            QMessageBox.information(self, "成功", "Pipeline 各階段轉譯已順利完成！請切換至『Simulator 執行面板』進行單步測試。")
            
        except (ValueError, NameError) as error:
            # 完美對應測試案例 9 與 10 的異常處理彈窗機制
            QMessageBox.critical(self, "編譯或轉譯錯誤", str(error))
            self.log_label.setText(f"系統狀態：發生致命錯誤！")

    def run_step(self):
        inst = self.cpu.execute_step(self.machine)
        self.log_label.setText(f"目前執行指令機器碼: {inst}")
        self.update_display()

    def update_display(self):
        for i, (reg, val) in enumerate(self.machine.registers.items()):
            self.table.setItem(i, 0, QTableWidgetItem(reg))
            self.table.setItem(i, 1, QTableWidgetItem(f"{val:06X}"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())