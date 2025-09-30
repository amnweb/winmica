import ctypes
import sys
import winreg
from enum import IntEnum

__version__ = "1.0.3"


class BackdropType(IntEnum):
    """Supported Mica backdrop options based on the official Windows API."""

    AUTO = 0  # DWMSBT_AUTO - Let DWM decide
    MICA = 2  # DWMSBT_MAINWINDOW - Standard Mica
    MICA_ALT = 4  # DWMSBT_TABBEDWINDOW - Mica Alt


def is_windows_dark_mode() -> bool:
    """Check if Windows is in dark mode by reading the registry."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
    except Exception:
        return False


def get_windows_build() -> int:
    """Get the current Windows build number."""
    try:
        return sys.getwindowsversion().build
    except Exception:
        return 0


def EnableMica(HWND: int, backdrop: BackdropType = BackdropType.MICA) -> int:
    """Enable the Mica backdrop effect using the official Windows API."""
    if HWND == 0:
        raise ValueError("The parameter HWND cannot be zero")
    try:
        try:
            HWND = int(HWND)
        except ValueError:
            HWND = int(str(HWND), 16)
        build = get_windows_build()
        if build < 22000:
            return 0x32
        dwm = ctypes.windll.dwmapi
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_SYSTEMBACKDROP_TYPE = 38
        DWMWA_MICA_EFFECT = 1029
        DWMWA_MICA_EFFECT_ALT = 38
        DwmSetWindowAttribute = dwm.DwmSetWindowAttribute
        DwmExtendFrameIntoClientArea = dwm.DwmExtendFrameIntoClientArea

        class _MARGINS(ctypes.Structure):
            _fields_ = [
                ("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int),
            ]

        # Apply dark theme
        dark_mode = is_windows_dark_mode()
        DwmSetWindowAttribute(
            HWND,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(ctypes.c_int(1 if dark_mode else 0)),
            ctypes.sizeof(ctypes.c_int),
        )
        # Extend frame
        margins = _MARGINS(-1, -1, -1, -1)
        DwmExtendFrameIntoClientArea(HWND, ctypes.byref(margins))
        # Apply backdrop effect
        if build >= 22621:
            result = DwmSetWindowAttribute(
                HWND,
                DWMWA_SYSTEMBACKDROP_TYPE,
                ctypes.byref(ctypes.c_int(backdrop.value)),
                ctypes.sizeof(ctypes.c_int),
            )
        else:
            if backdrop == BackdropType.MICA_ALT:
                result = DwmSetWindowAttribute(
                    HWND,
                    DWMWA_MICA_EFFECT_ALT,
                    ctypes.byref(ctypes.c_int(2)),
                    ctypes.sizeof(ctypes.c_int),
                )
            else:
                result = DwmSetWindowAttribute(
                    HWND,
                    DWMWA_MICA_EFFECT,
                    ctypes.byref(ctypes.c_int(1)),
                    ctypes.sizeof(ctypes.c_int),
                )
        return result
    except Exception:
        return -1


def is_mica_supported() -> bool:
    """Check if Mica effects are supported on this system."""
    return get_windows_build() >= 22000
