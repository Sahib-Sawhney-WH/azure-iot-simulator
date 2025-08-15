#!/usr/bin/env python3
"""
Minimal Azure IoT Hub Device Simulator
This is a simplified version that can be used to test if the basic framework works
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
    from PySide6.QtCore import Qt
except ImportError:
    print("ERROR: PySide6 not installed. Run: pip install PySide6")
    sys.exit(1)


class MinimalMainWindow(QMainWindow):
    """Minimal main window for testing"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure IoT Hub Device Simulator - Minimal Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add widgets
        title_label = QLabel("Azure IoT Hub Device Simulator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        status_label = QLabel("✓ Application started successfully!")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("font-size: 16px; color: green; margin: 10px;")
        layout.addWidget(status_label)
        
        info_label = QLabel(
            "This is a minimal test version to verify the GUI framework works.\n\n"
            "If you can see this window, the basic framework is working correctly.\n"
            "The full application with all features should work as well."
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 14px; margin: 20px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Test button
        test_button = QPushButton("Test Button - Click Me!")
        test_button.setStyleSheet("font-size: 14px; padding: 10px; margin: 10px;")
        test_button.clicked.connect(self.on_test_button_clicked)
        layout.addWidget(test_button)
        
        # Status label for button clicks
        self.click_status = QLabel("Button not clicked yet")
        self.click_status.setAlignment(Qt.AlignCenter)
        self.click_status.setStyleSheet("font-size: 12px; color: blue; margin: 10px;")
        layout.addWidget(self.click_status)
        
        # System info
        system_info = QLabel(
            f"Python: {sys.version}\n"
            f"Platform: {sys.platform}\n"
            f"Working Directory: {os.getcwd()}"
        )
        system_info.setAlignment(Qt.AlignCenter)
        system_info.setStyleSheet("font-size: 10px; color: gray; margin: 20px;")
        layout.addWidget(system_info)
    
    def on_test_button_clicked(self):
        """Handle test button click"""
        self.click_status.setText("✓ Button clicked! GUI is working correctly.")
        self.click_status.setStyleSheet("font-size: 12px; color: green; margin: 10px;")


def main():
    """Main entry point for minimal app"""
    print("Starting minimal Azure IoT Hub Device Simulator...")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Azure IoT Hub Device Simulator - Minimal")
    
    # Create and show main window
    window = MinimalMainWindow()
    window.show()
    
    print("✓ Minimal application window created and shown")
    print("If you can see the application window, the GUI framework is working!")
    
    # Start event loop
    exit_code = app.exec()
    
    print(f"Application exited with code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

