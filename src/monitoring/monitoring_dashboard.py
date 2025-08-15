"""Monitoring dashboard widget"""
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from datetime import datetime
from core.logging_config import get_logger

logger = get_logger('monitoring_dashboard')

class MonitoringDashboard(QWidget):
    export_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._setup_refresh_timer()
    
    def _init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("System Monitoring Dashboard")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Create tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Overview tab
        self._create_overview_tab()
        
        # Performance tab
        self._create_performance_tab()
        
        # Devices tab
        self._create_devices_tab()
        
        # Export button
        export_btn = QPushButton("Export Metrics")
        export_btn.clicked.connect(self.export_requested.emit)
        layout.addWidget(export_btn)
    
    def _create_overview_tab(self):
        """Create overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # System metrics
        metrics_group = QGroupBox("System Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        # Create metric labels
        self.total_devices_label = QLabel("0")
        self.connected_devices_label = QLabel("0")
        self.active_devices_label = QLabel("0")
        self.total_messages_label = QLabel("0")
        self.messages_per_sec_label = QLabel("0.0")
        self.total_errors_label = QLabel("0")
        self.uptime_label = QLabel("00:00:00")
        
        # Style metric labels
        for label in [self.total_devices_label, self.connected_devices_label, 
                     self.active_devices_label, self.total_messages_label,
                     self.messages_per_sec_label, self.total_errors_label, self.uptime_label]:
            font = label.font()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #2196F3; background: #f5f5f5; padding: 5px; border-radius: 3px;")
        
        # Add to layout
        metrics_layout.addWidget(QLabel("Total Devices:"), 0, 0)
        metrics_layout.addWidget(self.total_devices_label, 0, 1)
        
        metrics_layout.addWidget(QLabel("Connected:"), 0, 2)
        metrics_layout.addWidget(self.connected_devices_label, 0, 3)
        
        metrics_layout.addWidget(QLabel("Simulating:"), 1, 0)
        metrics_layout.addWidget(self.active_devices_label, 1, 1)
        
        metrics_layout.addWidget(QLabel("Total Messages:"), 1, 2)
        metrics_layout.addWidget(self.total_messages_label, 1, 3)
        
        metrics_layout.addWidget(QLabel("Messages/sec:"), 2, 0)
        metrics_layout.addWidget(self.messages_per_sec_label, 2, 1)
        
        metrics_layout.addWidget(QLabel("Total Errors:"), 2, 2)
        metrics_layout.addWidget(self.total_errors_label, 2, 3)
        
        metrics_layout.addWidget(QLabel("Uptime:"), 3, 0)
        metrics_layout.addWidget(self.uptime_label, 3, 1)
        
        layout.addWidget(metrics_group)
        
        # Status
        status_group = QGroupBox("System Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("System running normally")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        self.last_update_label = QLabel("Last updated: Never")
        self.last_update_label.setStyleSheet("color: #666; font-size: 11px;")
        status_layout.addWidget(self.last_update_label)
        
        layout.addWidget(status_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Overview")
    
    def _create_performance_tab(self):
        """Create performance tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Performance metrics
        perf_group = QGroupBox("Performance Metrics")
        perf_layout = QGridLayout(perf_group)
        
        # Create performance labels
        self.cpu_label = QLabel("0.0%")
        self.memory_label = QLabel("0.0%")
        self.disk_label = QLabel("0.0%")
        
        # Style performance labels
        for label in [self.cpu_label, self.memory_label, self.disk_label]:
            font = label.font()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #4CAF50; background: #f5f5f5; padding: 5px; border-radius: 3px;")
        
        perf_layout.addWidget(QLabel("CPU Usage:"), 0, 0)
        perf_layout.addWidget(self.cpu_label, 0, 1)
        
        perf_layout.addWidget(QLabel("Memory Usage:"), 0, 2)
        perf_layout.addWidget(self.memory_label, 0, 3)
        
        perf_layout.addWidget(QLabel("Disk Usage:"), 1, 0)
        perf_layout.addWidget(self.disk_label, 1, 1)
        
        layout.addWidget(perf_group)
        
        # Alerts
        alerts_group = QGroupBox("Performance Alerts")
        alerts_layout = QVBoxLayout(alerts_group)
        
        self.alerts_list = QListWidget()
        self.alerts_list.addItem("No active alerts")
        alerts_layout.addWidget(self.alerts_list)
        
        layout.addWidget(alerts_group)
        
        self.tab_widget.addTab(widget, "Performance")
    
    def _create_devices_tab(self):
        """Create devices tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Device list
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(5)
        self.device_table.setHorizontalHeaderLabels([
            "Device ID", "Status", "Messages", "Errors", "Last Message"
        ])
        
        # Configure table
        header = self.device_table.horizontalHeader()
        header.setStretchLastSection(True)
        
        layout.addWidget(self.device_table)
        
        self.tab_widget.addTab(widget, "Devices")
    
    def _setup_refresh_timer(self):
        """Setup refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(1000)  # Refresh every second
    
    def refresh_data(self):
        """Refresh dashboard data"""
        # This would be connected to actual metrics collectors
        # For now, just update the timestamp
        self.last_update_label.setText(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_system_metrics(self, metrics: dict):
        """Update system metrics display"""
        self.total_devices_label.setText(str(metrics.get("total_devices", 0)))
        self.connected_devices_label.setText(str(metrics.get("connected_devices", 0)))
        self.active_devices_label.setText(str(metrics.get("active_devices", 0)))
        self.total_messages_label.setText(str(metrics.get("total_messages", 0)))
        self.messages_per_sec_label.setText(f"{metrics.get('messages_per_second', 0.0):.1f}")
        self.total_errors_label.setText(str(metrics.get("total_errors", 0)))
        
        # Format uptime
        uptime_seconds = metrics.get("uptime_seconds", 0)
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        self.uptime_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def update_performance_metrics(self, metrics: dict):
        """Update performance metrics display"""
        if "cpu" in metrics:
            self.cpu_label.setText(f"{metrics['cpu']['percent']:.1f}%")
        
        if "memory" in metrics:
            self.memory_label.setText(f"{metrics['memory']['percent']:.1f}%")
        
        if "disk" in metrics:
            self.disk_label.setText(f"{metrics['disk']['percent']:.1f}%")
    
    def update_device_list(self, devices: list):
        """Update device list"""
        self.device_table.setRowCount(len(devices))
        
        for row, device in enumerate(devices):
            self.device_table.setItem(row, 0, QTableWidgetItem(device.get("device_id", "")))
            self.device_table.setItem(row, 1, QTableWidgetItem(device.get("status", "Unknown")))
            self.device_table.setItem(row, 2, QTableWidgetItem(str(device.get("message_count", 0))))
            self.device_table.setItem(row, 3, QTableWidgetItem(str(device.get("error_count", 0))))
            self.device_table.setItem(row, 4, QTableWidgetItem(device.get("last_message_time", "Never")))
    
    def add_alert(self, alert_message: str):
        """Add a performance alert"""
        if self.alerts_list.count() == 1 and self.alerts_list.item(0).text() == "No active alerts":
            self.alerts_list.clear()
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.alerts_list.addItem(f"[{timestamp}] {alert_message}")
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts_list.clear()
        self.alerts_list.addItem("No active alerts")
