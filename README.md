# winmica
A simple Python package to enable Windows 11 Mica effects for PyQt6 applications using the official Windows API.

## Installation

Install this package (from the project root):
```bash
pip install winmica
```

## Usage Example (PyQt6)

```python
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from winmica import ApplyMica, MicaType, is_mica_supported
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mica Example")
        self.setGeometry(100, 100, 600, 400)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        if is_mica_supported():
            hwnd = int(self.winId())
            ApplyMica(hwnd, MicaType.MICA)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
```

## Features
- Official Windows 11 Mica Effect
- Simple API: `ApplyMica(hwnd, effect_type)`
- Works with PyQt6 windows (may also work with PySide6 or Tkinter, but not tested)
- Detects system theme (light/dark)

## Effect Types
- `MicaType.MICA` – Standard Mica
- `MicaType.MICA_ALT` – Alternative Mica
- `MicaType.AUTO` – Auto (let Windows decide)

## Result:
<img width="954" height="720" alt="mica" src="https://github.com/user-attachments/assets/81131740-1240-43d6-a006-6cf379cfa09c" />
<img width="954" height="720" alt="micaalt" src="https://github.com/user-attachments/assets/df3ee785-9610-41a7-845d-57cb1b469443" />
