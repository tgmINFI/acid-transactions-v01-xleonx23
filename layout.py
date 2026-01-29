from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QSpinBox, QPushButton, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QGroupBox, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QTimer
import database
from processor import ShipmentProcessor

class FactoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        # FactoryWindow inherits from QWidget
        # This is the main window for the Factory Control System GUI
        self.setWindowTitle("MES: Factory Control System v1.0")
        self.resize(900, 600)
        
        # Initialize Logic
        self.processor = ShipmentProcessor(database.DB_NAME)
        
        self.setup_ui()
        self.refresh_tables()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        # Main vertical layout for the entire window
        # Contains the top and bottom sections
        
        
        # --- Top Section: Two Columns ---
        top_layout = QHBoxLayout()
        
        # LEFT: Inventory Table
        inv_group = QGroupBox("Live Warehouse Inventory")
        # QGroupBox to visually group the inventory table
        # This helps in organizing the UI and provides a titled border
        inv_layout = QVBoxLayout()
        # QVBoxLayout for vertical stacking inside the group box
        # although we only have one widget now, this allows for future additions
        self.inv_table = QTableWidget()
        self.inv_table.setColumnCount(2)
        self.inv_table.setHorizontalHeaderLabels(["Item", "Stock Qty"])
        self.inv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        inv_layout.addWidget(self.inv_table)
        inv_group.setLayout(inv_layout)
        
        # RIGHT: Controls
        control_group = QGroupBox("Shipment Control Panel")
        control_layout = QVBoxLayout()
        
        control_layout.addWidget(QLabel("Select Material:"))
        self.item_combo = QComboBox()
        control_layout.addWidget(self.item_combo)
        
        control_layout.addWidget(QLabel("Quantity to Ship:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 100)
        control_layout.addWidget(self.qty_spin)
        
        control_layout.addStretch()
        
        self.btn_process = QPushButton("EXECUTE SHIPMENT")
        self.btn_process.setCursor(Qt.PointingHandCursor)
        self.btn_process.clicked.connect(self.run_transaction)
        control_layout.addWidget(self.btn_process)

        self.btn_reset = QPushButton("RESET DATABASE")
        self.btn_reset.setStyleSheet("background-color: #444; color: white;")
        self.btn_reset.clicked.connect(self.reset_app)
        control_layout.addWidget(self.btn_reset)
        
        control_group.setLayout(control_layout)
        
        top_layout.addWidget(inv_group, 2)
        top_layout.addWidget(control_group, 1)
        
        # --- Bottom Section: Logs & Console ---
        bottom_layout = QHBoxLayout()
        
        # Log Table
        log_group = QGroupBox("Shipment History Logs")
        log_layout = QVBoxLayout()
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["Time", "Item", "Qty"])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        log_layout.addWidget(self.log_table)
        log_group.setLayout(log_layout)
        
        # System Console
        console_group = QGroupBox("System Events / Debug Console")
        console_layout = QVBoxLayout()
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        console_layout.addWidget(self.console)
        console_group.setLayout(console_layout)
        
        bottom_layout.addWidget(log_group, 1)
        bottom_layout.addWidget(console_group, 1)

        main_layout.addLayout(top_layout, 1)
        main_layout.addLayout(bottom_layout, 1)
        
        self.setLayout(main_layout)

    def log_message(self, message):
        """Helper to write to the GUI Console"""
        self.console.append(message)

    def refresh_tables(self):
        """Reloads data from DB into Tables"""
        conn = database.get_connection()
        cur = conn.cursor()
        
        # 1. Update Inventory Table
        cur.execute("SELECT item_name, stock_qty FROM inventory")
        rows = cur.fetchall()
        self.inv_table.setRowCount(0)
        self.item_combo.clear()
        
        for row_idx, row_data in enumerate(rows):
            self.inv_table.insertRow(row_idx)
            self.inv_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.inv_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
            self.item_combo.addItem(row_data[0])
            
        # 2. Update Log Table
        cur.execute("SELECT timestamp, item_name, qty_moved FROM shipment_log ORDER BY id DESC")
        logs = cur.fetchall()
        self.log_table.setRowCount(0)
        for row_idx, row_data in enumerate(logs):
            self.log_table.insertRow(row_idx)
            self.log_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.log_table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
            self.log_table.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2])))
            
        conn.close()

    def run_transaction(self):
        item = self.item_combo.currentText()
        qty = self.qty_spin.value()
        
        self.console.clear()
        
        # Call the student's logic
        self.processor.process_shipment(item, qty, self.log_message)
        
        # Refresh UI to show results (and potential errors)
        self.refresh_tables()

    def reset_app(self):
        database.setup_database()
        self.refresh_tables()
        self.console.append(">> DATABASE RESET TO DEFAULT.")