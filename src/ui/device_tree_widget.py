"""
Enhanced device tree widget
"""

from PySide6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QMenu, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QIcon, QColor

from core.logging_config import get_logger

logger = get_logger('device_tree_widget')


class DeviceTreeWidget(QTreeWidget):
    """Enhanced device tree widget with real-time updates"""
    
    device_selected = Signal(str)  # Emitted when device is selected
    device_action_requested = Signal(str, str)  # device_id, action
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._init_ui()
        self._setup_context_menu()
        self._setup_refresh_timer()
        
        # Device groups
        self.device_groups = {}
        self._create_device_groups()
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Setup headers
        self.setHeaderLabels(["Device", "Status", "Messages", "Errors"])
        
        # Configure tree
        self.setRootIsDecorated(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        
        # Resize columns
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Connect signals
        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)
    
    def _create_device_groups(self):
        """Create device group categories"""
        groups = [
            ("Sensors", "Temperature, humidity, motion sensors"),
            ("Gateways", "IoT gateways and edge devices"),
            ("Industrial", "Industrial equipment and machinery"),
            ("Mobile", "GPS trackers and mobile devices"),
            ("Custom", "Custom device types")
        ]
        
        for group_name, tooltip in groups:
            group_item = QTreeWidgetItem(self, [group_name, "", "", ""])
            group_item.setToolTip(0, tooltip)
            group_item.setExpanded(True)
            
            # Style group items
            font = group_item.font(0)
            font.setBold(True)
            group_item.setFont(0, font)
            
            self.device_groups[group_name] = group_item
    
    def _setup_context_menu(self):
        """Setup context menu for devices"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    def _setup_refresh_timer(self):
        """Setup timer for refreshing device status"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._refresh_device_status)
        self.refresh_timer.start(2000)  # Refresh every 2 seconds
    
    def _show_context_menu(self, position):
        """Show context menu for selected item"""
        item = self.itemAt(position)
        if not item or item in self.device_groups.values():
            return
        
        device_id = item.data(0, Qt.UserRole)
        if not device_id:
            return
        
        menu = QMenu(self)
        
        # Device actions
        connect_action = menu.addAction("Connect")
        disconnect_action = menu.addAction("Disconnect")
        menu.addSeparator()
        
        start_sim_action = menu.addAction("Start Simulation")
        stop_sim_action = menu.addAction("Stop Simulation")
        menu.addSeparator()
        
        configure_action = menu.addAction("Configure...")
        menu.addSeparator()
        
        remove_action = menu.addAction("Remove Device")
        
        # Execute action
        action = menu.exec(self.mapToGlobal(position))
        
        if action == connect_action:
            self.device_action_requested.emit(device_id, "connect")
        elif action == disconnect_action:
            self.device_action_requested.emit(device_id, "disconnect")
        elif action == start_sim_action:
            self.device_action_requested.emit(device_id, "start_simulation")
        elif action == stop_sim_action:
            self.device_action_requested.emit(device_id, "stop_simulation")
        elif action == configure_action:
            self.device_action_requested.emit(device_id, "configure")
        elif action == remove_action:
            self.device_action_requested.emit(device_id, "remove")
    
    def _on_selection_changed(self):
        """Handle selection change"""
        selected_items = self.selectedItems()
        if selected_items:
            item = selected_items[0]
            device_id = item.data(0, Qt.UserRole)
            if device_id:
                self.device_selected.emit(device_id)
    
    def _on_item_double_clicked(self, item, column):
        """Handle item double click"""
        device_id = item.data(0, Qt.UserRole)
        if device_id:
            self.device_action_requested.emit(device_id, "configure")
    
    def add_device(self, device_config):
        """Add a device to the tree"""
        device_id = device_config["device_id"]
        device_name = device_config.get("device_name", device_id)
        device_type = device_config.get("device_type", "Custom Device")
        
        # Determine group
        group_name = self._get_device_group(device_type)
        group_item = self.device_groups.get(group_name, self.device_groups["Custom"])
        
        # Create device item
        device_item = QTreeWidgetItem(group_item, [device_name, "Disconnected", "0", "0"])
        device_item.setData(0, Qt.UserRole, device_id)
        device_item.setToolTip(0, f"Device ID: {device_id}\nType: {device_type}")
        
        # Set status color
        self._update_device_status_color(device_item, "Disconnected")
        
        logger.info(f"Added device to tree: {device_id}")
    
    def remove_device(self, device_id):
        """Remove a device from the tree"""
        item = self._find_device_item(device_id)
        if item:
            parent = item.parent()
            if parent:
                parent.removeChild(item)
                logger.info(f"Removed device from tree: {device_id}")
    
    def update_device_status(self, device_id, status_data):
        """Update device status in the tree"""
        item = self._find_device_item(device_id)
        if not item:
            return
        
        # Update status text
        connected = status_data.get("connected", False)
        simulating = status_data.get("simulating", False)
        
        if simulating:
            status_text = "Simulating"
        elif connected:
            status_text = "Connected"
        else:
            status_text = "Disconnected"
        
        item.setText(1, status_text)
        
        # Update message counts
        message_count = status_data.get("message_count", 0)
        error_count = status_data.get("error_count", 0)
        
        item.setText(2, str(message_count))
        item.setText(3, str(error_count))
        
        # Update status color
        self._update_device_status_color(item, status_text)
    
    def _find_device_item(self, device_id):
        """Find device item by ID"""
        for group_item in self.device_groups.values():
            for i in range(group_item.childCount()):
                child_item = group_item.child(i)
                if child_item.data(0, Qt.UserRole) == device_id:
                    return child_item
        return None
    
    def _get_device_group(self, device_type):
        """Get appropriate group for device type"""
        device_type_lower = device_type.lower()
        
        if any(sensor in device_type_lower for sensor in ["temperature", "humidity", "motion", "sensor"]):
            return "Sensors"
        elif "gateway" in device_type_lower or "edge" in device_type_lower:
            return "Gateways"
        elif "industrial" in device_type_lower or "equipment" in device_type_lower:
            return "Industrial"
        elif "gps" in device_type_lower or "tracker" in device_type_lower or "mobile" in device_type_lower:
            return "Mobile"
        else:
            return "Custom"
    
    def _update_device_status_color(self, item, status):
        """Update device status color"""
        if status == "Simulating":
            color = QColor(0, 150, 0)  # Green
        elif status == "Connected":
            color = QColor(0, 100, 200)  # Blue
        else:
            color = QColor(150, 150, 150)  # Gray
        
        item.setForeground(1, color)
    
    def _refresh_device_status(self):
        """Refresh device status (placeholder for real implementation)"""
        # This would be connected to the actual device manager
        # For now, it's just a placeholder
        pass
    
    def get_selected_device_ids(self):
        """Get selected device IDs"""
        device_ids = []
        for item in self.selectedItems():
            device_id = item.data(0, Qt.UserRole)
            if device_id:
                device_ids.append(device_id)
        return device_ids
    
    def select_device(self, device_id):
        """Select a specific device"""
        item = self._find_device_item(device_id)
        if item:
            self.setCurrentItem(item)
            self.scrollToItem(item)
