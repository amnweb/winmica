"""
Simple example demonstrating Windows Mica effects.
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from winmica import ApplyMica, MicaType, is_mica_supported


class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Mica Example")
        self.setGeometry(200, 200, 800, 600)

        # Enable transparency for better Mica effect
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Windows Mica Effect Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold")
        layout.addWidget(title)

        # Info
        info = QLabel("This window demonstrates the Mica backdrop effect on Windows 11.")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(info)
        layout.addStretch()

        # Buttons
        mica_btn = QPushButton("Apply Mica Effect")
        mica_btn.clicked.connect(self.apply_mica)
        mica_btn.setStyleSheet("""
            QPushButton {
                padding: 5px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: rgba(0, 120, 212, 0.8);
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 1.0);
            }
        """)
        layout.addWidget(mica_btn)

        mica_alt_btn = QPushButton("Apply Mica Alt Effect")
        mica_alt_btn.clicked.connect(self.apply_mica_alt)
        mica_alt_btn.setStyleSheet("""
            QPushButton {
                padding: 5px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: rgba(140, 140, 140, 0.8);
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(140, 140, 140, 1.0);
            }
        """)
        layout.addWidget(mica_alt_btn)

        auto_btn = QPushButton("Apply Auto Effect")
        auto_btn.clicked.connect(self.apply_auto)
        auto_btn.setStyleSheet("""
            QPushButton {
                padding: 5px 20px;
                font-size: 14px;
                border-radius: 6px;
                background-color: rgba(0, 200, 83, 0.8);
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 200, 83, 1.0);
            }
        """)
        layout.addWidget(auto_btn)

        # Remove Effect button and handler as per the updated requirements

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; margin: 10px")
        layout.addWidget(self.status_label)

    def apply_mica(self):
        """Apply standard Mica effect"""
        if not is_mica_supported():
            self.status_label.setText("Mica effects not supported on this system")
            return

        hwnd = int(self.winId())
        result = ApplyMica(hwnd, MicaType.MICA)

        if result == 0:
            self.status_label.setText("✓ Mica effect applied successfully")
            self.status_label.setStyleSheet("color: green; font-size: 12px; margin: 10px;")
        else:
            self.status_label.setText(f"Mica effect applied (code: {result})")
            self.status_label.setStyleSheet("color: orange; font-size: 12px; margin: 10px;")

    def apply_mica_alt(self):
        """Apply Mica Alt effect"""
        if not is_mica_supported():
            self.status_label.setText("Mica effects not supported on this system")
            return

        hwnd = int(self.winId())
        result = ApplyMica(hwnd, MicaType.MICA_ALT)

        if result == 0:
            self.status_label.setText("✓ Mica Alt effect applied successfully")
            self.status_label.setStyleSheet("color: green; font-size: 12px; margin: 10px;")
        else:
            self.status_label.setText(f"Mica Alt effect applied (code: {result})")
            self.status_label.setStyleSheet("color: orange; font-size: 12px; margin: 10px;")

    def apply_auto(self):
        """Apply Auto effect"""
        if not is_mica_supported():
            self.status_label.setText("Mica effects not supported on this system")
            return

        hwnd = int(self.winId())
        result = ApplyMica(hwnd, MicaType.AUTO)

        if result == 0:
            self.status_label.setText("✓ Auto effect applied successfully")
            self.status_label.setStyleSheet("color: green; font-size: 12px; margin: 10px;")
        else:
            self.status_label.setText(f"Auto effect applied (code: {result})")
            self.status_label.setStyleSheet("color: orange; font-size: 12px; margin: 10px;")

    # Remove the apply_acrylic method as per the updated requirements


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Mica Example")

    # Check if Mica is supported
    if not is_mica_supported():
        print("Warning: Mica effects are not supported on this system.")
        print("The example will still run but effects will not be applied.")

    window = SimpleWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
