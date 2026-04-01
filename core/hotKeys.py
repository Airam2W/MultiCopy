# Listens for global hotkeys to trigger actions like showing the overlay or copying text to the clipboard.

from pynput import keyboard
from core.clipboardManager import ClipboardManager
from utils.config import config
import threading
import time


class HotkeyManager:
    def __init__(self, on_show_overlay_callback=None):
        self.on_show_overlay = on_show_overlay_callback
        self.listener = None

    def _on_copy(self):
        threading.Thread(
            target=self._delayed_clipboard_read,
            daemon=True
        ).start()

    def _delayed_clipboard_read(self):
        time.sleep(0.05)
        text = ClipboardManager.read_clipboard()
        if text:
            ClipboardManager.add_text(text)

    def _on_show_overlay(self):
        if self.on_show_overlay:
            self.on_show_overlay()

    def start(self):
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+c': self._on_copy,
            config.show_overlay_hotkey: self._on_show_overlay
        })
        self.listener.start()
        
    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
