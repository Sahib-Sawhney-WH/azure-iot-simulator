"""Batch operations for bulk device management"""
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal, QThread
from typing import List, Dict, Any
from core.logging_config import get_logger

logger = get_logger('batch_operations')

class BatchOperationThread(QThread):
    progress_updated = Signal(int, str)
    operation_completed = Signal(dict)
    
    def __init__(self, operation: str, device_ids: List[str], parameters: Dict[str, Any] = None):
        super().__init__()
        self.operation = operation
        self.device_ids = device_ids
        self.parameters = parameters or {}
    
    def run(self):
        """Execute batch operation"""
        total_devices = len(self.device_ids)
        successful = 0
        failed = 0
        
        for i, device_id in enumerate(self.device_ids):
            try:
                # Simulate operation
                self.progress_updated.emit(
                    int((i + 1) / total_devices * 100),
                    f"Processing {device_id}..."
                )
                
                # Here would be the actual operation
                if self.operation == "connect":
                    self._connect_device(device_id)
                elif self.operation == "disconnect":
                    self._disconnect_device(device_id)
                elif self.operation == "start_simulation":
                    self._start_simulation(device_id)
                elif self.operation == "stop_simulation":
                    self._stop_simulation(device_id)
                elif self.operation == "update_config":
                    self._update_config(device_id)
                
                successful += 1
                
            except Exception as e:
                logger.error(f"Batch operation failed for device {device_id}: {e}")
                failed += 1
            
            # Small delay to show progress
            self.msleep(100)
        
        self.operation_completed.emit({
            "operation": self.operation,
            "total": total_devices,
            "successful": successful,
            "failed": failed
        })
    
    def _connect_device(self, device_id: str):
        """Connect a device"""
        logger.info(f"Connecting device: {device_id}")
    
    def _disconnect_device(self, device_id: str):
        """Disconnect a device"""
        logger.info(f"Disconnecting device: {device_id}")
    
    def _start_simulation(self, device_id: str):
        """Start simulation for device"""
        logger.info(f"Starting simulation for device: {device_id}")
    
    def _stop_simulation(self, device_id: str):
        """Stop simulation for device"""
        logger.info(f"Stopping simulation for device: {device_id}")
    
    def _update_config(self, device_id: str):
        """Update device configuration"""
        logger.info(f"Updating configuration for device: {device_id}")

class BatchOperationsDialog(QDialog):
    operation_requested = Signal(str, list, dict)
    
    def __init__(self, device_ids: List[str], parent=None):
        super().__init__(parent)
        self.device_ids = device_ids
        self.setWindowTitle(f"Batch Operations ({len(device_ids)} devices)")
        self.setModal(True)
        self.resize(500, 400)
        
        self.operation_thread = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize user interface"""
        layout = QVBoxLayout(self)
        
        # Device list
        devices_group = QGroupBox(f"Selected Devices ({len(self.device_ids)})")
        devices_layout = QVBoxLayout(devices_group)
        
        self.devices_list = QListWidget()
        self.devices_list.addItems(self.device_ids)
        self.devices_list.setMaximumHeight(100)
        devices_layout.addWidget(self.devices_list)
        
        layout.addWidget(devices_group)
        
        # Operations
        operations_group = QGroupBox("Batch Operations")
        operations_layout = QVBoxLayout(operations_group)
        
        # Connection operations
        conn_layout = QHBoxLayout()
        connect_btn = QPushButton("Connect All")
        connect_btn.clicked.connect(lambda: self._start_operation("connect"))
        conn_layout.addWidget(connect_btn)
        
        disconnect_btn = QPushButton("Disconnect All")
        disconnect_btn.clicked.connect(lambda: self._start_operation("disconnect"))
        conn_layout.addWidget(disconnect_btn)
        
        operations_layout.addLayout(conn_layout)
        
        # Simulation operations
        sim_layout = QHBoxLayout()
        start_sim_btn = QPushButton("Start All Simulations")
        start_sim_btn.clicked.connect(lambda: self._start_operation("start_simulation"))
        sim_layout.addWidget(start_sim_btn)
        
        stop_sim_btn = QPushButton("Stop All Simulations")
        stop_sim_btn.clicked.connect(lambda: self._start_operation("stop_simulation"))
        sim_layout.addWidget(stop_sim_btn)
        
        operations_layout.addLayout(sim_layout)
        
        # Configuration operations
        config_layout = QHBoxLayout()
        update_config_btn = QPushButton("Update Configurations")
        update_config_btn.clicked.connect(self._show_config_options)
        config_layout.addWidget(update_config_btn)
        
        operations_layout.addLayout(config_layout)
        
        layout.addWidget(operations_group)
        
        # Progress
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("Ready")
        progress_layout.addWidget(self.progress_label)
        
        layout.addWidget(progress_group)
        
        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(100)
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
    def _start_operation(self, operation: str, parameters: Dict[str, Any] = None):
        """Start batch operation"""
        if self.operation_thread and self.operation_thread.isRunning():
            QMessageBox.warning(self, "Operation in Progress", "Please wait for the current operation to complete.")
            return
        
        self.progress_bar.setValue(0)
        self.progress_label.setText(f"Starting {operation}...")
        self.results_text.clear()
        
        # Start operation thread
        self.operation_thread = BatchOperationThread(operation, self.device_ids, parameters)
        self.operation_thread.progress_updated.connect(self._update_progress)
        self.operation_thread.operation_completed.connect(self._operation_completed)
        self.operation_thread.start()
        
        logger.info(f"Started batch operation: {operation} for {len(self.device_ids)} devices")
    
    def _update_progress(self, percentage: int, message: str):
        """Update progress display"""
        self.progress_bar.setValue(percentage)
        self.progress_label.setText(message)
    
    def _operation_completed(self, result: Dict[str, Any]):
        """Handle operation completion"""
        operation = result["operation"]
        total = result["total"]
        successful = result["successful"]
        failed = result["failed"]
        
        self.progress_label.setText("Operation completed")
        
        result_text = f"Batch {operation} completed:\n"
        result_text += f"  Total devices: {total}\n"
        result_text += f"  Successful: {successful}\n"
        result_text += f"  Failed: {failed}\n"
        
        if failed > 0:
            result_text += f"  Success rate: {(successful/total)*100:.1f}%"
        else:
            result_text += "  Success rate: 100%"
        
        self.results_text.setText(result_text)
        
        logger.info(f"Batch operation completed: {result}")
    
    def _show_config_options(self):
        """Show configuration update options"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Configuration")
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Configuration options
        options_group = QGroupBox("Configuration Updates")
        options_layout = QFormLayout(options_group)
        
        interval_spin = QSpinBox()
        interval_spin.setRange(1, 3600)
        interval_spin.setValue(10)
        interval_spin.setSuffix(" seconds")
        options_layout.addRow("Message Interval:", interval_spin)
        
        jitter_spin = QSpinBox()
        jitter_spin.setRange(0, 50)
        jitter_spin.setValue(10)
        jitter_spin.setSuffix("%")
        options_layout.addRow("Timing Jitter:", jitter_spin)
        
        protocol_combo = QComboBox()
        protocol_combo.addItems(["MQTT", "AMQP", "HTTPS"])
        options_layout.addRow("Protocol:", protocol_combo)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        apply_btn = QPushButton("Apply Changes")
        apply_btn.clicked.connect(lambda: self._apply_config_changes(
            dialog,
            {
                "message_interval": interval_spin.value(),
                "jitter_percent": jitter_spin.value(),
                "protocol": protocol_combo.currentText()
            }
        ))
        button_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def _apply_config_changes(self, dialog: QDialog, config: Dict[str, Any]):
        """Apply configuration changes"""
        dialog.accept()
        self._start_operation("update_config", config)
