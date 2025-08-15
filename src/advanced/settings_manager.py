"""Comprehensive settings management"""
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from typing import Dict, Any
from core.logging_config import get_logger

logger = get_logger('settings_manager')

class SettingsManagerDialog(QDialog):
    settings_changed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Settings")
        self.setModal(True)
        self.resize(600, 500)
        
        self.settings = {}
        self._init_ui()
        self._load_settings()
    
    def _init_ui(self):
        """Initialize user interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_general_tab()
        self._create_azure_tab()
        self._create_simulation_tab()
        self._create_monitoring_tab()
        self._create_appearance_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self._ok_clicked)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self):
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Application settings
        app_group = QGroupBox("Application Settings")
        app_layout = QFormLayout(app_group)
        
        self.auto_save_check = QCheckBox("Auto-save configuration changes")
        self.auto_save_check.setChecked(True)
        app_layout.addRow("", self.auto_save_check)
        
        self.confirm_exit_check = QCheckBox("Confirm before exiting application")
        self.confirm_exit_check.setChecked(True)
        app_layout.addRow("", self.confirm_exit_check)
        
        self.startup_check_check = QCheckBox("Check for updates on startup")
        app_layout.addRow("", self.startup_check_check)
        
        layout.addWidget(app_group)
        
        # Logging settings
        log_group = QGroupBox("Logging Settings")
        log_layout = QFormLayout(log_group)
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText("INFO")
        log_layout.addRow("Log Level:", self.log_level_combo)
        
        self.log_to_file_check = QCheckBox("Save logs to file")
        self.log_to_file_check.setChecked(True)
        log_layout.addRow("", self.log_to_file_check)
        
        self.max_log_files_spin = QSpinBox()
        self.max_log_files_spin.setRange(1, 100)
        self.max_log_files_spin.setValue(10)
        log_layout.addRow("Max Log Files:", self.max_log_files_spin)
        
        layout.addWidget(log_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "General")
    
    def _create_azure_tab(self):
        """Create Azure settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Connection settings
        conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout(conn_group)
        
        self.connection_timeout_spin = QSpinBox()
        self.connection_timeout_spin.setRange(5, 300)
        self.connection_timeout_spin.setValue(30)
        self.connection_timeout_spin.setSuffix(" seconds")
        conn_layout.addRow("Connection Timeout:", self.connection_timeout_spin)
        
        self.retry_attempts_spin = QSpinBox()
        self.retry_attempts_spin.setRange(1, 10)
        self.retry_attempts_spin.setValue(3)
        conn_layout.addRow("Retry Attempts:", self.retry_attempts_spin)
        
        self.retry_delay_spin = QSpinBox()
        self.retry_delay_spin.setRange(1, 60)
        self.retry_delay_spin.setValue(5)
        self.retry_delay_spin.setSuffix(" seconds")
        conn_layout.addRow("Retry Delay:", self.retry_delay_spin)
        
        layout.addWidget(conn_group)
        
        # Protocol settings
        protocol_group = QGroupBox("Protocol Settings")
        protocol_layout = QFormLayout(protocol_group)
        
        self.default_protocol_combo = QComboBox()
        self.default_protocol_combo.addItems(["MQTT", "AMQP", "HTTPS"])
        protocol_layout.addRow("Default Protocol:", self.default_protocol_combo)
        
        self.keep_alive_spin = QSpinBox()
        self.keep_alive_spin.setRange(10, 3600)
        self.keep_alive_spin.setValue(60)
        self.keep_alive_spin.setSuffix(" seconds")
        protocol_layout.addRow("Keep Alive Interval:", self.keep_alive_spin)
        
        layout.addWidget(protocol_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Azure IoT")
    
    def _create_simulation_tab(self):
        """Create simulation settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Default simulation settings
        sim_group = QGroupBox("Default Simulation Settings")
        sim_layout = QFormLayout(sim_group)
        
        self.default_interval_spin = QSpinBox()
        self.default_interval_spin.setRange(1, 3600)
        self.default_interval_spin.setValue(10)
        self.default_interval_spin.setSuffix(" seconds")
        sim_layout.addRow("Message Interval:", self.default_interval_spin)
        
        self.default_jitter_spin = QSpinBox()
        self.default_jitter_spin.setRange(0, 50)
        self.default_jitter_spin.setValue(10)
        self.default_jitter_spin.setSuffix("%")
        sim_layout.addRow("Timing Jitter:", self.default_jitter_spin)
        
        self.auto_start_check = QCheckBox("Auto-start simulation for new devices")
        sim_layout.addRow("", self.auto_start_check)
        
        layout.addWidget(sim_group)
        
        # Performance settings
        perf_group = QGroupBox("Performance Settings")
        perf_layout = QFormLayout(perf_group)
        
        self.max_devices_spin = QSpinBox()
        self.max_devices_spin.setRange(1, 10000)
        self.max_devices_spin.setValue(1000)
        perf_layout.addRow("Max Devices:", self.max_devices_spin)
        
        self.thread_pool_size_spin = QSpinBox()
        self.thread_pool_size_spin.setRange(1, 100)
        self.thread_pool_size_spin.setValue(10)
        perf_layout.addRow("Thread Pool Size:", self.thread_pool_size_spin)
        
        self.message_queue_size_spin = QSpinBox()
        self.message_queue_size_spin.setRange(100, 100000)
        self.message_queue_size_spin.setValue(10000)
        perf_layout.addRow("Message Queue Size:", self.message_queue_size_spin)
        
        layout.addWidget(perf_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Simulation")
    
    def _create_monitoring_tab(self):
        """Create monitoring settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Monitoring settings
        monitor_group = QGroupBox("Monitoring Settings")
        monitor_layout = QFormLayout(monitor_group)
        
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(1, 60)
        self.refresh_interval_spin.setValue(2)
        self.refresh_interval_spin.setSuffix(" seconds")
        monitor_layout.addRow("Refresh Interval:", self.refresh_interval_spin)
        
        self.history_retention_spin = QSpinBox()
        self.history_retention_spin.setRange(1, 168)
        self.history_retention_spin.setValue(24)
        self.history_retention_spin.setSuffix(" hours")
        monitor_layout.addRow("History Retention:", self.history_retention_spin)
        
        self.enable_performance_monitoring_check = QCheckBox("Enable performance monitoring")
        self.enable_performance_monitoring_check.setChecked(True)
        monitor_layout.addRow("", self.enable_performance_monitoring_check)
        
        layout.addWidget(monitor_group)
        
        # Alert settings
        alert_group = QGroupBox("Alert Settings")
        alert_layout = QFormLayout(alert_group)
        
        self.enable_alerts_check = QCheckBox("Enable performance alerts")
        self.enable_alerts_check.setChecked(True)
        alert_layout.addRow("", self.enable_alerts_check)
        
        self.cpu_threshold_spin = QSpinBox()
        self.cpu_threshold_spin.setRange(50, 95)
        self.cpu_threshold_spin.setValue(80)
        self.cpu_threshold_spin.setSuffix("%")
        alert_layout.addRow("CPU Alert Threshold:", self.cpu_threshold_spin)
        
        self.memory_threshold_spin = QSpinBox()
        self.memory_threshold_spin.setRange(50, 95)
        self.memory_threshold_spin.setValue(85)
        self.memory_threshold_spin.setSuffix("%")
        alert_layout.addRow("Memory Alert Threshold:", self.memory_threshold_spin)
        
        layout.addWidget(alert_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Monitoring")
    
    def _create_appearance_tab(self):
        """Create appearance settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Theme settings
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        theme_layout.addRow("Theme:", self.theme_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(10)
        self.font_size_spin.setSuffix(" pt")
        theme_layout.addRow("Font Size:", self.font_size_spin)
        
        layout.addWidget(theme_group)
        
        # Window settings
        window_group = QGroupBox("Window Settings")
        window_layout = QFormLayout(window_group)
        
        self.remember_window_size_check = QCheckBox("Remember window size and position")
        self.remember_window_size_check.setChecked(True)
        window_layout.addRow("", self.remember_window_size_check)
        
        self.minimize_to_tray_check = QCheckBox("Minimize to system tray")
        window_layout.addRow("", self.minimize_to_tray_check)
        
        layout.addWidget(window_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Appearance")
    
    def _load_settings(self):
        """Load current settings"""
        # This would load from configuration manager
        # For now, just use defaults
        pass
    
    def _apply_settings(self):
        """Apply current settings"""
        settings = self._collect_settings()
        self.settings_changed.emit(settings)
        logger.info("Settings applied")
    
    def _ok_clicked(self):
        """Handle OK button click"""
        self._apply_settings()
        self.accept()
    
    def _collect_settings(self) -> Dict[str, Any]:
        """Collect all settings from UI"""
        return {
            "general": {
                "auto_save": self.auto_save_check.isChecked(),
                "confirm_exit": self.confirm_exit_check.isChecked(),
                "startup_check": self.startup_check_check.isChecked(),
                "log_level": self.log_level_combo.currentText(),
                "log_to_file": self.log_to_file_check.isChecked(),
                "max_log_files": self.max_log_files_spin.value()
            },
            "azure": {
                "connection_timeout": self.connection_timeout_spin.value(),
                "retry_attempts": self.retry_attempts_spin.value(),
                "retry_delay": self.retry_delay_spin.value(),
                "default_protocol": self.default_protocol_combo.currentText(),
                "keep_alive": self.keep_alive_spin.value()
            },
            "simulation": {
                "default_interval": self.default_interval_spin.value(),
                "default_jitter": self.default_jitter_spin.value(),
                "auto_start": self.auto_start_check.isChecked(),
                "max_devices": self.max_devices_spin.value(),
                "thread_pool_size": self.thread_pool_size_spin.value(),
                "message_queue_size": self.message_queue_size_spin.value()
            },
            "monitoring": {
                "refresh_interval": self.refresh_interval_spin.value(),
                "history_retention": self.history_retention_spin.value(),
                "enable_performance_monitoring": self.enable_performance_monitoring_check.isChecked(),
                "enable_alerts": self.enable_alerts_check.isChecked(),
                "cpu_threshold": self.cpu_threshold_spin.value(),
                "memory_threshold": self.memory_threshold_spin.value()
            },
            "appearance": {
                "theme": self.theme_combo.currentText(),
                "font_size": self.font_size_spin.value(),
                "remember_window_size": self.remember_window_size_check.isChecked(),
                "minimize_to_tray": self.minimize_to_tray_check.isChecked()
            }
        }
