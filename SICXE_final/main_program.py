import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel)

# Import the A-D modules
from assembler_pass1 import AssemblerPass1
from assembler_pass2 import AssemblerPass2
from linking_loader import LinkingLoader
from cpu_execution import CPUExecution

class MachineState:
    def __init__(self):
        # 1MB Memory bytearray
        self.memory = bytearray(1024 * 1024) 
        # Register definitions
        self.registers = {'A':0, 'X':0, 'L':0, 'PC':0, 'SW':0, 'B':0, 'S':0, 'T':0}

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.machine = MachineState()
        self.a = AssemblerPass1()
        self.b = AssemblerPass2()
        self.c = LinkingLoader()
        self.d = CPUExecution()
        self.init_ui()

    def init_ui(self):
        # Exact Mandarin labels from your previous version
        self.setWindowTitle("SIC/XE System Simulator (模擬器)")
        self.resize(550, 650)
        layout = QVBoxLayout()

        self.table = QTableWidget(8, 2)
        self.table.setHorizontalHeaderLabels(["Register", "Value"])
        layout.addWidget(QLabel("CPU Registers 暫存器 (Hex 16進位):"))
        layout.addWidget(self.table)

        self.log_label = QLabel("目前指令: 無")
        self.log_label.setStyleSheet("font-weight: bold; color: blue; font-size: 14px;")
        layout.addWidget(self.log_label)

        self.btn_load = QPushButton("載入 'COPY' 程式")
        self.btn_load.clicked.connect(self.process_pipeline)
        layout.addWidget(self.btn_load)

        self.btn_step = QPushButton("執行步驟")
        self.btn_step.clicked.connect(self.run_step)
        layout.addWidget(self.btn_step)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.update_display()

    def process_pipeline(self):
        """Module A -> Module B -> Module C"""
        syms = self.a.run("COPY START 1000")
        code = self.b.run(syms)
        self.c.load_to_memory(self.machine, code, 0x1000)
        self.update_display()
        self.log_label.setText("系統:已載入。準備執行。")

    def run_step(self):
        """Module D execution"""
        inst = self.d.execute_step(self.machine)
        self.log_label.setText(f"目前指令: {inst}")
        self.update_display()

    def update_display(self):
        """Refresh the register table"""
        for i, reg in enumerate(self.machine.registers.keys()):
            self.table.setItem(i, 0, QTableWidgetItem(reg))
            val = f"{self.machine.registers[reg]:06X}" # Format as 6-digit hex
            self.table.setItem(i, 1, QTableWidgetItem(val))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())