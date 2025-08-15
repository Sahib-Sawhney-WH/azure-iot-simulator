"""Template browser dialog"""
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from core.logging_config import get_logger

logger = get_logger('template_browser')

class TemplateBrowserDialog(QDialog):
    template_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Message Template Browser")
        self.setModal(True)
        self.resize(600, 400)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Template list
        self.template_list = QListWidget()
        layout.addWidget(self.template_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        new_btn = QPushButton("New Template")
        new_btn.clicked.connect(self._new_template)
        button_layout.addWidget(new_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self._edit_template)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._delete_template)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self._select_template)
        button_layout.addWidget(select_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self._load_templates()
    
    def _load_templates(self):
        """Load templates into list"""
        # This would load from template manager
        built_in_templates = [
            "Temperature Sensor",
            "Motion Sensor", 
            "GPS Tracker",
            "Industrial Sensor"
        ]
        
        for template in built_in_templates:
            self.template_list.addItem(template)
    
    def _new_template(self):
        """Create new template"""
        pass
    
    def _edit_template(self):
        """Edit selected template"""
        pass
    
    def _delete_template(self):
        """Delete selected template"""
        pass
    
    def _select_template(self):
        """Select template"""
        current_item = self.template_list.currentItem()
        if current_item:
            self.template_selected.emit(current_item.text())
            self.accept()
