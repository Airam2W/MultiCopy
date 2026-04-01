# Overlay UI for clipboard management using Tkinter.

import os

from utils.configManager import save_config
from utils.config import config
import tkinter as tk
from tkinter import ttk
from core.clipboardManager import ClipboardManager
import pyautogui
from core.state import state

ROW_WIDTH = 110
ROW_HEIGHT = 43
TOP_BAR_HEIGHT = 43

savedX = 0
savedY = 0

# Icon of the application
ICON_RUTE = os.path.join(os.path.dirname(__file__), "../utils/logo.ico")

class ClipboardOverlay:
    def __init__(self, on_open_settings=None, on_stop_listener=None):
        self.on_open_settings = on_open_settings
        self.on_stop_listener = on_stop_listener

        self.selected_index = 0
        self.item_rows = []

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.iconbitmap(ICON_RUTE)

        # Keyboard
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.confirm_selected)
        self.root.bind("<Escape>", lambda e: self.hide())

        # -------------------------
        # Top bar (gear only)
        # -------------------------

        top_bar = tk.Frame(
            self.root,
            bg="#f5f5f5",
            height=TOP_BAR_HEIGHT
        )
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        self.items_container = tk.Frame(
            self.root,
            bg="#f5f5f5",
            width=ROW_WIDTH
        )
        self.items_container.pack(fill="both", expand=True)
        self.items_container.pack_propagate(False)



        gear_btn = tk.Button(
            top_bar,
            text="⚙",
            font=("Segoe UI", 11),
            relief="flat",
            bg="#f5f5f5",
            command=self.open_settings
        )
        gear_btn.pack(padx=10, expand=True)

        # -------------------------
        # Scroll area
        # -------------------------
        

    # -------------------------
    # Overlay control
    # -------------------------
    def show_thread_safe(self):
        self.root.after(0, self.show)

    def show(self):
        self.refresh_items()
        self.center_overlay()
        self.root.deiconify()
        self.root.focus_force()

    def hide(self):
        self.root.withdraw()

    def center_overlay(self):
        self.refresh_items_overlay()

        cursor_x, cursor_y = pyautogui.position()

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = cursor_x + 12
        y = cursor_y + 12

        if x + self.overlay_width > screen_w:
            x = cursor_x - self.overlay_width - 12

        if y + self.overlay_height > screen_h:
            y = screen_h - self.overlay_height - 10
            
        global savedX, savedY
        savedX = x
        savedY = y

        self.root.geometry(
            f"{self.overlay_width}x{self.overlay_height}+{x}+{y}"
        )

        self.root.attributes("-alpha", 0.97)

        
    def refresh_items_overlay(self):
        visible_count = min(len(ClipboardManager.get_all()), state.max_items_visible)

        self.overlay_width = ROW_WIDTH
        self.overlay_height = (ROW_HEIGHT * visible_count) + TOP_BAR_HEIGHT

        self.root.geometry(
            f"{self.overlay_width}x{self.overlay_height}+{savedX}+{savedY}"
        )





    # -------------------------
    # Items
    # -------------------------
    def refresh_items(self):
        for row in self.item_rows:
            row.destroy()
        self.item_rows.clear()

        items = ClipboardManager.get_all()
        visible_items = items[:state.max_items_visible]

        if self.selected_index >= len(items):
            self.selected_index = max(0, len(items) - 1)

        for index, text in enumerate(visible_items):
            display = text.replace("\n", " ")
            if len(display) > 4:
                display = display[:4] + "..."

            selected = index == self.selected_index
            bg = "#000" if selected else "#fff"
            fg = "#fff" if selected else "#000"

            row = tk.Frame(
                self.items_container,
                bg=bg,
                width=ROW_WIDTH,
                height=ROW_HEIGHT
            )
            row.pack(fill="x")
            row.pack_propagate(False)

            label = tk.Label(
                row,
                text=display,
                anchor="w",
                padx=10,
                pady=6,
                bg=bg,
                fg=fg,
                font=("Segoe UI", 9),
            )
            label.pack(side="left", fill="x", expand=True)
            
            label.bind("<Button-1>", lambda e, i=index: self.selectMouse(i))

            del_btn = tk.Button(
                row,
                text="✖",
                bg=bg,
                fg=fg,
                relief="flat",
                command=lambda i=index: self.delete_item(i)
            )
            del_btn.pack(side="right", padx=6)

            self.item_rows.append(row)

            



    def delete_item(self, index):
        ClipboardManager.remove(index)
        self.refresh_items()
        self.refresh_items_overlay()

    # -------------------------
    # Selection
    # -------------------------
    def select(self, index):
        self.selected_index = index
        self.refresh_items()

    def confirm(self, index):
        self.selected_index = index
        self.confirm_selected()
    
    def selectMouse(self, index):
        self.select(index)
        self.confirm(index)

    def confirm_selected(self, event=None):
        items = ClipboardManager.get_all()
        if items:
            ClipboardManager.set_clipboard(items[self.selected_index])
            self.hide()
            pyautogui.hotkey("ctrl", "v")





    # -------------------------
    # Keyboard navigation
    # -------------------------
    def move_up(self, event=None):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.refresh_items()

    def move_down(self, event=None):
        if self.selected_index < len(ClipboardManager.get_all()) - 1:
            self.selected_index += 1
            if self.selected_index >= state.max_items_visible:
                self.selected_index = state.max_items_visible - 1
            self.refresh_items()

    # -------------------------
    # Gear
    # -------------------------
    def open_settings(self):
        self.hide()
        save_config(state, config)
        if self.on_stop_listener:
            self.on_stop_listener()
        if self.on_open_settings:
            self.on_open_settings()
