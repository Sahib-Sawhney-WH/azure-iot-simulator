"""
Main window for Azure IoT Hub Device Simulator
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QToolBar, QStatusBar, QLabel, QProgressBar,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QPushButton,
    QGroupBox, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QKeySequence, QAction

from core.logging_config import get_logger
from core.config import config_manager
from core.events import EventMixin, EventType, Event

logger = get_logger('main_window')


class MainWindow(QMainWindow, EventMixin):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure IoT Hub Device Simulator")
        self.setMinimumSize(1000, 700)
        
        # Initialize UI components
        self._init_ui()
        self._init_menu_bar()
        self._init_tool_bar()
        self._init_status_bar()
        
        # Setup event handlers
        self._setup_event_handlers()
        
        # Start update timer
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_status)
        self._update_timer.start(2000)  # Update every 2 seconds
        
        logger.info("Main window initialized")
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Device Explorer
        self._create_device_panel(splitter)
        
        # Right panel - Tabbed content area
        self._create_content_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 900])
    
    def _create_device_panel(self, parent):
        """Create the device explorer panel"""
        device_widget = QWidget()
        device_layout = QVBoxLayout(device_widget)
        
        # Device explorer header
        header_layout = QHBoxLayout()
        device_layout.addLayout(header_layout)
        
        device_label = QLabel("Device Explorer")
        device_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(device_label)
        
        # Device control buttons
        add_button = QPushButton("Add Device")
        add_button.clicked.connect(self._add_device)
        header_layout.addWidget(add_button)
        
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self._remove_device)
        header_layout.addWidget(remove_button)
        
        # Device tree
        self.device_tree = QTreeWidget()
        self.device_tree.setHeaderLabel("Devices")
        device_layout.addWidget(self.device_tree)
        
        # Simulation controls
        controls_group = QGroupBox("Simulation Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        start_button = QPushButton("Start All")
        start_button.clicked.connect(self._start_simulation)
        controls_layout.addWidget(start_button)
        
        stop_button = QPushButton("Stop All")
        stop_button.clicked.connect(self._stop_simulation)
        controls_layout.addWidget(stop_button)
        
        pause_button = QPushButton("Pause All")
        pause_button.clicked.connect(self._pause_simulation)
        controls_layout.addWidget(pause_button)
        
        device_layout.addWidget(controls_group)
        
        parent.addWidget(device_widget)
    
    def _create_content_panel(self, parent):
        """Create the main content panel with tabs"""
        self.tab_widget = QTabWidget()
        
        # Overview tab
        overview_tab = self._create_overview_tab()
        self.tab_widget.addTab(overview_tab, "Overview")
        
        # Monitoring tab
        monitoring_tab = self._create_monitoring_tab()
        self.tab_widget.addTab(monitoring_tab, "Monitoring")
        
        # Configuration tab
        config_tab = self._create_configuration_tab()
        self.tab_widget.addTab(config_tab, "Configuration")
        
        parent.addWidget(self.tab_widget)
    
    def _create_overview_tab(self):
        """Create the overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Welcome message
        welcome_label = QLabel("Welcome to Azure IoT Hub Device Simulator")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Status information
        status_group = QGroupBox("System Status")
        status_layout = QVBoxLayout(status_group)
        
        self.connection_status = QLabel("Azure IoT Hub: Not Connected")
        status_layout.addWidget(self.connection_status)
        
        self.device_count = QLabel("Active Devices: 0")
        status_layout.addWidget(self.device_count)
        
        self.simulation_status = QLabel("Simulation: Stopped")
        status_layout.addWidget(self.simulation_status)
        
        layout.addWidget(status_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        configure_azure_btn = QPushButton("Configure Azure IoT Hub")
        configure_azure_btn.clicked.connect(self._configure_azure)
        actions_layout.addWidget(configure_azure_btn)
        
        add_device_btn = QPushButton("Add New Device")
        add_device_btn.clicked.connect(self._add_device)
        actions_layout.addWidget(add_device_btn)
        
        start_simulation_btn = QPushButton("Start Simulation")
        start_simulation_btn.clicked.connect(self._start_simulation)
        actions_layout.addWidget(start_simulation_btn)
        
        layout.addWidget(actions_group)
        
        layout.addStretch()
        return widget
    
    def _create_monitoring_tab(self):
        """Create the monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Monitoring dashboard placeholder
        dashboard_label = QLabel("Real-time Monitoring Dashboard")
        dashboard_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        dashboard_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dashboard_label)
        
        # Metrics display
        metrics_group = QGroupBox("Metrics")
        metrics_layout = QVBoxLayout(metrics_group)
        
        self.messages_sent = QLabel("Messages Sent: 0")
        metrics_layout.addWidget(self.messages_sent)
        
        self.messages_failed = QLabel("Messages Failed: 0")
        metrics_layout.addWidget(self.messages_failed)
        
        self.data_transferred = QLabel("Data Transferred: 0 KB")
        metrics_layout.addWidget(self.data_transferred)
        
        layout.addWidget(metrics_group)
        
        layout.addStretch()
        return widget
    
    def _create_configuration_tab(self):
        """Create the configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Configuration options
        config_label = QLabel("Application Configuration")
        config_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(config_label)
        
        # Theme selection
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout(theme_group)
        
        light_theme_btn = QPushButton("Light Theme")
        light_theme_btn.clicked.connect(lambda: self._change_theme("light"))
        theme_layout.addWidget(light_theme_btn)
        
        dark_theme_btn = QPushButton("Dark Theme")
        dark_theme_btn.clicked.connect(lambda: self._change_theme("dark"))
        theme_layout.addWidget(dark_theme_btn)
        
        layout.addWidget(theme_group)
        
        layout.addStretch()
        return widget
    
    def _init_menu_bar(self):
        """Initialize the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Device", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._add_device)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        azure_config_action = QAction("Azure Configuration", self)
        azure_config_action.triggered.connect(self._configure_azure)
        tools_menu.addAction(azure_config_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _init_tool_bar(self):
        """Initialize the tool bar"""
        toolbar = self.addToolBar("Main")
        
        # Add device action
        add_device_action = QAction("Add Device", self)
        add_device_action.triggered.connect(self._add_device)
        toolbar.addAction(add_device_action)
        
        toolbar.addSeparator()
        
        # Simulation controls
        start_action = QAction("Start", self)
        start_action.triggered.connect(self._start_simulation)
        toolbar.addAction(start_action)
        
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self._stop_simulation)
        toolbar.addAction(stop_action)
        
        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self._pause_simulation)
        toolbar.addAction(pause_action)
    
    def _init_status_bar(self):
        """Initialize the status bar"""
        self.status_bar = self.statusBar()
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Connection indicator
        self.connection_indicator = QLabel("Disconnected")
        self.connection_indicator.setStyleSheet("color: red;")
        self.status_bar.addPermanentWidget(self.connection_indicator)
    
    def _setup_event_handlers(self):
        """Setup event handlers"""
        self.subscribe_to_event(EventType.DEVICE_ADDED, self._on_device_added)
        self.subscribe_to_event(EventType.DEVICE_REMOVED, self._on_device_removed)
        self.subscribe_to_event(EventType.SIMULATION_STARTED, self._on_simulation_started)
        self.subscribe_to_event(EventType.SIMULATION_STOPPED, self._on_simulation_stopped)
    
    def _add_device(self):
        """Add a new device"""
        # Placeholder for device addition
        item = QTreeWidgetItem(self.device_tree)
        item.setText(0, f"Device {self.device_tree.topLevelItemCount()}")
        
        self.emit_event(EventType.DEVICE_ADDED, {"device_id": item.text(0)})
        logger.info(f"Device added: {item.text(0)}")
    
    def _remove_device(self):
        """Remove selected device"""
        current_item = self.device_tree.currentItem()
        if current_item:
            device_id = current_item.text(0)
            self.device_tree.takeTopLevelItem(
                self.device_tree.indexOfTopLevelItem(current_item)
            )
            self.emit_event(EventType.DEVICE_REMOVED, {"device_id": device_id})
            logger.info(f"Device removed: {device_id}")
    
    def _start_simulation(self):
        """Start simulation"""
        self.emit_event(EventType.SIMULATION_STARTED)
        logger.info("Simulation started")
    
    def _stop_simulation(self):
        """Stop simulation"""
        self.emit_event(EventType.SIMULATION_STOPPED)
        logger.info("Simulation stopped")
    
    def _pause_simulation(self):
        """Pause simulation"""
        self.emit_event(EventType.SIMULATION_PAUSED)
        logger.info("Simulation paused")
    
    def _configure_azure(self):
        """Configure Azure IoT Hub connection"""
        # Placeholder for Azure configuration dialog
        QMessageBox.information(self, "Azure Configuration", 
                              "Azure IoT Hub configuration dialog would open here.")
    
    def _change_theme(self, theme: str):
        """Change application theme"""
        config_manager.update_app_config(theme=theme)
        QMessageBox.information(self, "Theme Changed", 
                              f"Theme changed to {theme}. Restart the application to apply changes.")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About", 
                         "Azure IoT Hub Device Simulator v1.0.0\n"
                         "Professional IoT device simulation tool\n"
                         "Built with Python and PySide6")
    
    def _update_status(self):
        """Update status information"""
        # Update device count
        device_count = self.device_tree.topLevelItemCount()
        self.device_count.setText(f"Active Devices: {device_count}")
        
        # Update status bar
        self.status_label.setText(f"Ready - {device_count} devices")
    
    def _on_device_added(self, event: Event):
        """Handle device added event"""
        self._update_status()
    
    def _on_device_removed(self, event: Event):
        """Handle device removed event"""
        self._update_status()
    
    def _on_simulation_started(self, event: Event):
        """Handle simulation started event"""
        self.simulation_status.setText("Simulation: Running")
        self.connection_indicator.setText("Connected")
        self.connection_indicator.setStyleSheet("color: green;")
    
    def _on_simulation_stopped(self, event: Event):
        """Handle simulation stopped event"""
        self.simulation_status.setText("Simulation: Stopped")
        self.connection_indicator.setText("Disconnected")
        self.connection_indicator.setStyleSheet("color: red;")

