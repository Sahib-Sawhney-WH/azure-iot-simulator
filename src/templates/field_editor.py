"""Field editor for template fields"""
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from core.logging_config import get_logger

logger = get_logger('field_editor')

class FieldEditorDialog(QDialog):
    field_configured = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Field Editor")
        self.setModal(True)
        self.resize(400, 300)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Field basic info
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        form_layout.addRow("Field Name:", self.name_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["string", "int", "float", "bool", "timestamp", "uuid", "location"])
        form_layout.addRow("Data Type:", self.type_combo)
        
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(["constant", "random", "sine_wave", "linear", "gaussian"])
        form_layout.addRow("Pattern:", self.pattern_combo)
        
        layout.addLayout(form_layout)
        
        # Pattern-specific settings
        self.settings_group = QGroupBox("Pattern Settings")
        self.settings_layout = QFormLayout(self.settings_group)
        
        self.min_value_spin = QDoubleSpinBox()
        self.min_value_spin.setRange(-999999, 999999)
        self.settings_layout.addRow("Min Value:", self.min_value_spin)
        
        self.max_value_spin = QDoubleSpinBox()
        self.max_value_spin.setRange(-999999, 999999)
        self.max_value_spin.setValue(100)
        self.settings_layout.addRow("Max Value:", self.max_value_spin)
        
        layout.addWidget(self.settings_group)
        
        # Preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_label = QLabel("Sample values will appear here")
        preview_layout.addWidget(self.preview_label)
        
        refresh_btn = QPushButton("Refresh Preview")
        refresh_btn.clicked.connect(self._refresh_preview)
        preview_layout.addWidget(refresh_btn)
        
        layout.addWidget(preview_group)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self._accept_field)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _refresh_preview(self):
        """Refresh field preview"""
        # Generate sample values
        self.preview_label.setText("Sample: 42.5, 38.2, 45.1, 39.8, 41.3")
    
    def _accept_field(self):
        """Accept field configuration"""
        field_config = {
            "name": self.name_edit.text(),
            "data_type": self.type_combo.currentText(),
            "pattern": self.pattern_combo.currentText(),
            "min_value": self.min_value_spin.value(),
            "max_value": self.max_value_spin.value()
        }
        
        self.field_configured.emit(field_config)
        self.accept()
