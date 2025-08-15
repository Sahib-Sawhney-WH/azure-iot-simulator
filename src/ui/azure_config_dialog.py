"""
Azure IoT Hub configuration dialog
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar,
    QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt, QThread, Signal

from core.logging_config import get_logger

logger = get_logger('azure_config_dialog')


class ConnectionTestThread(QThread):
    """Background thread for testing Azure connection"""
    
    test_completed = Signal(dict)  # Emitted when test is complete
    
    def __init__(self, connection_string):
        super().__init__()
        self.connection_string = connection_string
    
    def run(self):
        """Run connection test in background"""
        try:
            from azure_integration.connection_manager import ConnectionManager
            
            manager = ConnectionManager()
            result = manager.parse_connection_string(self.connection_string)
            
            if result:
                self.test_completed.emit({
                    "success": True,
                    "message": f"Connection string parsed successfully for device: {result.device_id}",
                    "connection_info": result
                })
            else:
                self.test_completed.emit({
                    "success": False,
                    "message": "Invalid connection string format"
                })
                
        except Exception as e:
            self.test_completed.emit({
                "success": False,
                "message": f"Error testing connection: {str(e)}"
            })


class AzureConfigDialog(QDialog):
    """Azure IoT Hub configuration dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Azure IoT Hub Configuration")
        self.setModal(True)
        self.resize(600, 400)
        
        self.test_thread = None
        
        self._init_ui()
        self._load_current_settings()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Connection string group
        connection_group = QGroupBox("Azure IoT Hub Connection")
        connection_layout = QVBoxLayout(connection_group)
        
        # Instructions
        instructions = QLabel(
            "Enter your Azure IoT Hub connection string. You can find this in the "
            "Azure portal under IoT Hub > Shared access policies > iothubowner."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 10px;")
        connection_layout.addWidget(instructions)
        
        # Connection string input
        form_layout = QFormLayout()
        
        self.connection_string_edit = QTextEdit()
        self.connection_string_edit.setMaximumHeight(80)
        self.connection_string_edit.setPlaceholderText(
            "HostName=your-hub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=..."
        )
        form_layout.addRow("Connection String:", self.connection_string_edit)
        
        connection_layout.addLayout(form_layout)
        
        # Test connection button and progress
        test_layout = QHBoxLayout()
        
        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self._test_connection)
        test_layout.addWidget(self.test_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        test_layout.addWidget(self.progress_bar)
        
        test_layout.addStretch()
        connection_layout.addLayout(test_layout)
        
        # Test result
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setVisible(False)
        connection_layout.addWidget(self.result_label)
        
        layout.addWidget(connection_group)
        
        # Device settings group
        device_group = QGroupBox("Default Device Settings")
        device_layout = QFormLayout(device_group)
        
        self.default_protocol_combo = QComboBox()
        self.default_protocol_combo.addItems(["MQTT", "AMQP", "HTTPS"])
        device_layout.addRow("Default Protocol:", self.default_protocol_combo)
        
        self.default_interval_spin = QSpinBox()
        self.default_interval_spin.setRange(1, 3600)
        self.default_interval_spin.setValue(10)
        self.default_interval_spin.setSuffix(" seconds")
        device_layout.addRow("Default Message Interval:", self.default_interval_spin)
        
        layout.addWidget(device_group)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self._save_configuration)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def _load_current_settings(self):
        """Load current Azure settings"""
        try:
            from core.config import ConfigManager
            
            config_manager = ConfigManager()
            azure_config = config_manager.get_azure_config()
            
            if azure_config.connection_string:
                self.connection_string_edit.setPlainText(azure_config.connection_string)
            
            # Set default protocol
            protocol_index = self.default_protocol_combo.findText(azure_config.default_protocol)
            if protocol_index >= 0:
                self.default_protocol_combo.setCurrentIndex(protocol_index)
            
            self.default_interval_spin.setValue(azure_config.default_message_interval)
            
        except Exception as e:
            logger.error(f"Error loading Azure settings: {e}")
    
    def _test_connection(self):
        """Test the Azure IoT Hub connection"""
        connection_string = self.connection_string_edit.toPlainText().strip()
        
        if not connection_string:
            QMessageBox.warning(self, "Validation Error", "Please enter a connection string.")
            return
        
        # Show progress
        self.test_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.result_label.setVisible(False)
        
        # Start test in background thread
        self.test_thread = ConnectionTestThread(connection_string)
        self.test_thread.test_completed.connect(self._on_test_completed)
        self.test_thread.start()
    
    def _on_test_completed(self, result):
        """Handle connection test completion"""
        # Hide progress
        self.test_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Show result
        self.result_label.setVisible(True)
        
        if result["success"]:
            self.result_label.setText(f"✓ {result['message']}")
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.result_label.setText(f"✗ {result['message']}")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")
        
        logger.info(f"Connection test result: {result}")
    
    def _save_configuration(self):
        """Save the Azure configuration"""
        connection_string = self.connection_string_edit.toPlainText().strip()
        
        if not connection_string:
            QMessageBox.warning(self, "Validation Error", "Please enter a connection string.")
            return
        
        try:
            from core.config import ConfigManager
            
            config_manager = ConfigManager()
            azure_config = config_manager.get_azure_config()
            
            # Update configuration
            azure_config.connection_string = connection_string
            azure_config.default_protocol = self.default_protocol_combo.currentText()
            azure_config.default_message_interval = self.default_interval_spin.value()
            
            # Save configuration
            config_manager.save_azure_config(azure_config)
            
            QMessageBox.information(self, "Success", "Azure configuration saved successfully.")
            self.accept()
            
            logger.info("Azure configuration saved")
            
        except Exception as e:
            logger.error(f"Error saving Azure configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
