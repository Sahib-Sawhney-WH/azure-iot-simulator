"""
Device creation and configuration dialog
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QCheckBox, QTextEdit, QGroupBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from core.logging_config import get_logger

logger = get_logger('device_dialog')


class DeviceDialog(QDialog):
    """Device creation and configuration dialog"""
    
    device_created = Signal(dict)  # Emitted when device is created
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Device")
        self.setModal(True)
        self.resize(500, 400)
        
        self._init_ui()
        self._populate_defaults()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_basic_tab()
        self._create_connection_tab()
        self._create_simulation_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("Create Device")
        self.ok_button.clicked.connect(self._create_device)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def _create_basic_tab(self):
        """Create basic information tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Device ID
        self.device_id_edit = QLineEdit()
        self.device_id_edit.setPlaceholderText("e.g., sensor-001")
        layout.addRow("Device ID:", self.device_id_edit)
        
        # Device Name
        self.device_name_edit = QLineEdit()
        self.device_name_edit.setPlaceholderText("e.g., Temperature Sensor 1")
        layout.addRow("Device Name:", self.device_name_edit)
        
        # Device Type
        self.device_type_combo = QComboBox()
        self.device_type_combo.addItems([
            "Temperature Sensor",
            "Motion Sensor", 
            "GPS Tracker",
            "Industrial Sensor",
            "Custom Device"
        ])
        layout.addRow("Device Type:", self.device_type_combo)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("Optional description...")
        layout.addRow("Description:", self.description_edit)
        
        self.tab_widget.addTab(widget, "Basic Info")
    
    def _create_connection_tab(self):
        """Create connection settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Connection method
        connection_group = QGroupBox("Connection Method")
        connection_layout = QVBoxLayout(connection_group)
        
        self.use_global_connection = QCheckBox("Use global Azure IoT Hub connection")
        self.use_global_connection.setChecked(True)
        self.use_global_connection.toggled.connect(self._on_connection_method_changed)
        connection_layout.addWidget(self.use_global_connection)
        
        # Custom connection string
        custom_layout = QFormLayout()
        self.connection_string_edit = QLineEdit()
        self.connection_string_edit.setPlaceholderText("HostName=...;DeviceId=...;SharedAccessKey=...")
        self.connection_string_edit.setEnabled(False)
        custom_layout.addRow("Connection String:", self.connection_string_edit)
        
        connection_layout.addLayout(custom_layout)
        layout.addWidget(connection_group)
        
        # Protocol settings
        protocol_group = QGroupBox("Protocol Settings")
        protocol_layout = QFormLayout(protocol_group)
        
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["MQTT", "AMQP", "HTTPS"])
        protocol_layout.addRow("Protocol:", self.protocol_combo)
        
        self.auto_reconnect_check = QCheckBox("Auto-reconnect on connection loss")
        self.auto_reconnect_check.setChecked(True)
        protocol_layout.addRow("", self.auto_reconnect_check)
        
        layout.addWidget(protocol_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Connection")
    
    def _create_simulation_tab(self):
        """Create simulation settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Message template
        template_group = QGroupBox("Message Template")
        template_layout = QFormLayout(template_group)
        
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "temperature_sensor",
            "motion_sensor",
            "gps_tracker",
            "industrial_sensor"
        ])
        template_layout.addRow("Template:", self.template_combo)
        
        layout.addWidget(template_group)
        
        # Simulation timing
        timing_group = QGroupBox("Simulation Timing")
        timing_layout = QFormLayout(timing_group)
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 3600)
        self.interval_spin.setValue(10)
        self.interval_spin.setSuffix(" seconds")
        timing_layout.addRow("Message Interval:", self.interval_spin)
        
        self.jitter_spin = QSpinBox()
        self.jitter_spin.setRange(0, 50)
        self.jitter_spin.setValue(10)
        self.jitter_spin.setSuffix("%")
        timing_layout.addRow("Timing Jitter:", self.jitter_spin)
        
        layout.addWidget(timing_group)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.burst_mode_check = QCheckBox("Burst mode (send multiple messages at once)")
        advanced_layout.addWidget(self.burst_mode_check)
        
        burst_layout = QFormLayout()
        self.burst_count_spin = QSpinBox()
        self.burst_count_spin.setRange(2, 20)
        self.burst_count_spin.setValue(5)
        self.burst_count_spin.setEnabled(False)
        burst_layout.addRow("Burst Count:", self.burst_count_spin)
        
        self.burst_mode_check.toggled.connect(self.burst_count_spin.setEnabled)
        advanced_layout.addLayout(burst_layout)
        
        layout.addWidget(advanced_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Simulation")
    
    def _populate_defaults(self):
        """Populate default values"""
        import random
        
        # Generate default device ID
        device_num = random.randint(1, 999)
        self.device_id_edit.setText(f"device-{device_num:03d}")
        self.device_name_edit.setText(f"Device {device_num}")
    
    def _on_connection_method_changed(self, use_global: bool):
        """Handle connection method change"""
        self.connection_string_edit.setEnabled(not use_global)
    
    def _create_device(self):
        """Create the device with current settings"""
        # Validate inputs
        device_id = self.device_id_edit.text().strip()
        if not device_id:
            QMessageBox.warning(self, "Validation Error", "Device ID is required.")
            return
        
        device_name = self.device_name_edit.text().strip()
        if not device_name:
            device_name = device_id
        
        # Build device configuration
        device_config = {
            "device_id": device_id,
            "device_name": device_name,
            "device_type": self.device_type_combo.currentText(),
            "description": self.description_edit.toPlainText().strip(),
            "use_global_connection": self.use_global_connection.isChecked(),
            "connection_string": self.connection_string_edit.text().strip(),
            "protocol": self.protocol_combo.currentText(),
            "auto_reconnect": self.auto_reconnect_check.isChecked(),
            "template_name": self.template_combo.currentText(),
            "message_interval": self.interval_spin.value(),
            "jitter_percent": self.jitter_spin.value(),
            "burst_mode": self.burst_mode_check.isChecked(),
            "burst_count": self.burst_count_spin.value()
        }
        
        # Emit signal and close
        self.device_created.emit(device_config)
        self.accept()
        
        logger.info(f"Device configuration created: {device_id}")
