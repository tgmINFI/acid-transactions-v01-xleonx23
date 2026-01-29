import sys
from PySide6.QtWidgets import QApplication
import database
from layout import FactoryWindow

if __name__ == "__main__":
    # Ensure DB exists
    database.setup_database()
    
    app = QApplication(sys.argv)
    # sys.argv means command line arguments passed to the app
    # This allows for future extensibility (e.g., debug modes, config files, etc.)
    # Load Stylesheet
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())
        
    window = FactoryWindow()
    # Show the main window
    # FactoryWindow is defined in layout.py

    window.show()
    
    sys.exit(app.exec())
    # Start the event loop
    # This keeps the application running and responsive
    # sys.exit ensures a clean exit when the app is closed
    # exec() starts the Qt event loop