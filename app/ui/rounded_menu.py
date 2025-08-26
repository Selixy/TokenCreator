# ui/rounded_menu.py
import sys, ctypes

def enable_win11_round_corners(widget, pref=1):
    if sys.platform != "win32":
        return False
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    try:
        hwnd = int(widget.winId())
        val = ctypes.c_int(pref)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            ctypes.c_void_p(hwnd),
            ctypes.c_int(DWMWA_WINDOW_CORNER_PREFERENCE),
            ctypes.byref(val),
            ctypes.sizeof(val),
        )
        
        return True
    except Exception:
        return False
