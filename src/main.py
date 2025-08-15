"""
Main entry point for Azure IoT Hub Device Simulator
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from core.logging_config import setup_logging, get_logger
from core.config import config_manager
from core.events import event_bus, EventType
from ui.main_window import MainWindow


class Application:
    """Main application class"""
    
    def __init__(self):
        self.logger = None
        self.qt_app = None
        self.main_window = None
    
    def initialize(self):
        """Initialize the application"""
        # Setup logging
        app_config = config_manager.get_app_config()
        self.logger = setup_logging(
            log_level=app_config.log_level,
            console_output=True,
            file_output=True
        )
        
        self.logger.info("Starting Azure IoT Hub Device Simulator")
        
        # Create Qt application
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName(app_config.app_name)
        self.qt_app.setApplicationVersion(app_config.version)
        self.qt_app.setOrganizationName("Manus AI")
        
        # Apply theme
        self._apply_theme(app_config.theme)
        
        # Emit application started event
        event_bus.emit(EventType.APP_STARTED, "Application", {
            "version": app_config.version,
            "theme": app_config.theme
        })
        
        self.logger.info("Application initialized successfully")
    
    def _apply_theme(self, theme: str):
        """Apply the specified theme to the application"""
        if theme == "dark":
            # Dark theme stylesheet
            dark_style = """
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: #ffffff;
                padding: 8px 16px;
                border: 1px solid #555555;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            """
            self.qt_app.setStyleSheet(dark_style)
        else:
            # Light theme (default Qt style)
            self.qt_app.setStyleSheet("")
    
    def create_main_window(self):
        """Create and show the main window"""
        self.main_window = MainWindow()
        
        # Set window size from config
        app_config = config_manager.get_app_config()
        self.main_window.resize(app_config.window_width, app_config.window_height)
        
        self.main_window.show()
        self.logger.info("Main window created and shown")
    
    def run(self):
        """Run the application"""
        try:
            self.initialize()
            self.create_main_window()
            
            # Start the Qt event loop
            exit_code = self.qt_app.exec()
            
            self.logger.info(f"Application exiting with code: {exit_code}")
            return exit_code
            
        except Exception as e:
            if self.logger:
                self.logger.critical(f"Critical error in application: {e}", exc_info=True)
            else:
                print(f"Critical error: {e}")
            return 1
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources before exit"""
        try:
            # Emit application closing event
            event_bus.emit(EventType.APP_CLOSING, "Application")
            
            # Save configuration
            config_manager.save_config()
            
            if self.logger:
                self.logger.info("Application cleanup completed")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point"""
    app = Application()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())

