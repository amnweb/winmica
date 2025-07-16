"""
Demonstrates different Mica effects.
"""

import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from winmica import (
    ApplyMica,
    MicaType,
    is_mica_supported,
    is_windows_dark_mode,
)


class MicaTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mica Effects Test")
        self.setGeometry(100, 100, 900, 700)

        # Enable transparency
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Setup UI
        self.setup_ui()

        # Auto-apply Mica when window is shown
        self.current_effect = MicaType.MICA

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Mica Effects Test Suite")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        # System info group
        info_group = QGroupBox("System Information")
        info_layout = QVBoxLayout(info_group)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(120)
        self.info_text.setReadOnly(True)
        self.update_system_info()
        info_layout.addWidget(self.info_text)

        layout.addWidget(info_group)

        # Effect controls group
        controls_group = QGroupBox("Backdrop Effects")
        controls_layout = QVBoxLayout(controls_group)

        # Quick effect buttons only
        buttons_layout = QHBoxLayout()

        mica_btn = QPushButton("Standard Mica")
        mica_btn.clicked.connect(lambda: self.apply_effect(MicaType.MICA))
        buttons_layout.addWidget(mica_btn)

        mica_alt_btn = QPushButton("Mica Alt")
        mica_alt_btn.clicked.connect(lambda: self.apply_effect(MicaType.MICA_ALT))
        buttons_layout.addWidget(mica_alt_btn)

        auto_btn = QPushButton("Auto")
        auto_btn.clicked.connect(lambda: self.apply_effect(MicaType.AUTO))
        buttons_layout.addWidget(auto_btn)

        controls_layout.addLayout(buttons_layout)
        layout.addWidget(controls_group)

        # Status group
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)

        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Segoe UI", 12))
        status_layout.addWidget(self.status_label)

        self.theme_label = QLabel()
        self.theme_label.setFont(QFont("Segoe UI", 10))
        status_layout.addWidget(self.theme_label)

        layout.addWidget(status_group)

        self.update_theme()

    def update_system_info(self):
        """Update the system information display"""
        # Capture system info
        from winmica import get_windows_build

        build = get_windows_build()
        dark_mode = is_windows_dark_mode()
        supported = is_mica_supported()
        effects = [e.name for e in MicaType]

        system_info = f"""Windows Build: {build}
Dark Mode: {"Enabled" if dark_mode else "Disabled"}
Mica Supported: {"Yes" if supported else "No"}
Supported Effects: {", ".join(effects) if effects else "None"}

"""
        if build >= 22621:
            system_info += "Using official documented API"
        elif build >= 22000:
            system_info += "Using legacy fallback method"
        else:
            system_info += "Mica effects not supported on this Windows version"

        self.info_text.setText(system_info)

    def apply_effect(self, effect_type: MicaType):
        """Apply a specific Mica effect"""
        if not is_mica_supported():
            self.status_label.setText("Status: Mica effects not supported on this system")
            return

        hwnd = int(self.winId())

        try:
            result = ApplyMica(hwnd, effect_type)
            self.current_effect = effect_type

            if result == 0:
                self.status_label.setText(f"Status: Successfully applied {effect_type.name}")
                self.status_label.setStyleSheet("color: green;")
            else:
                self.status_label.setText(f"Status: Effect applied with code {result}")
                self.status_label.setStyleSheet("color: orange;")

        except Exception as e:
            self.status_label.setText(f"Status: Error - {str(e)}")
            self.status_label.setStyleSheet("color: red;")

    def update_theme(self):
        """Update the window theme based on system settings"""
        dark_mode = is_windows_dark_mode()

        # Update theme label
        theme_status = "Dark Mode" if dark_mode else "Light Mode"
        self.theme_label.setText(f"Current Theme: {theme_status}")

        # Update window colors
        if dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: rgba(32, 32, 32, 0.0);
                }
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #555;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QPushButton {
                    background-color: #404040;
                    border: 1px solid #606060;
                    border-radius: 4px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #303030;
                }
                QTextEdit {
                    background-color: rgba(64, 64, 64, 0.4);
                    border: 1px solid #606060;
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: rgba(248, 248, 248, 0.8);
                    color: black;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                    color: black;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 8px;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QTextEdit {
                    background-color: rgba(255, 255, 255, 0.8);
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    color: black;
                }
                QLabel {
                    color: black;
                }
            """)

    def showEvent(self, event):
        """Apply Mica effect when window is shown"""
        super().showEvent(event)

        # Small delay to ensure window is fully created
        QTimer.singleShot(100, lambda: self.apply_effect(self.current_effect))

    def closeEvent(self, event):
        """Clean up when window is closed"""
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Mica Effects Test")
    window = MicaTestWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
