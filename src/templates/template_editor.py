"""Template editor dialog"""
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from core.logging_config import get_logger

logger = get_logger('template_editor')

class TemplateEditorDialog(QDialog):
    template_saved = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Message Template Editor")
        self.setModal(True)
        self.resize(800, 600)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Template info
        info_group = QGroupBox("Template Information")
        info_layout = QFormLayout(info_group)
        
        self.name_edit = QLineEdit()
        info_layout.addRow("Template Name:", self.name_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        info_layout.addRow("Description:", self.description_edit)
        
        layout.addWidget(info_group)
        
        # Fields
        fields_group = QGroupBox("Message Fields")
        fields_layout = QVBoxLayout(fields_group)
        
        self.fields_list = QListWidget()
        fields_layout.addWidget(self.fields_list)
        
        buttons_layout = QHBoxLayout()
        add_field_btn = QPushButton("Add Field")
        add_field_btn.clicked.connect(self._add_field)
        buttons_layout.addWidget(add_field_btn)
        
        edit_field_btn = QPushButton("Edit Field")
        edit_field_btn.clicked.connect(self._edit_field)
        buttons_layout.addWidget(edit_field_btn)
        
        remove_field_btn = QPushButton("Remove Field")
        remove_field_btn.clicked.connect(self._remove_field)
        buttons_layout.addWidget(remove_field_btn)
        
        fields_layout.addLayout(buttons_layout)
        layout.addWidget(fields_group)
        
        # Preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Template")
        save_btn.clicked.connect(self._save_template)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _add_field(self):
        """Add a new field"""
        # This would open a field editor dialog
        pass
    
    def _edit_field(self):
        """Edit selected field"""
        pass
    
    def _remove_field(self):
        """Remove selected field"""
        pass
    
    def _save_template(self):
        """Save the template"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Template name is required")
            return
        
        self.template_saved.emit(name)
        self.accept()
