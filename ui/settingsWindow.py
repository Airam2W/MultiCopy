from doctest import master
from logging import root
import os
import tkinter as tk
from tkinter import ttk, filedialog
from core.clipboardManager import ClipboardManager
from core.state import state
from utils.config import config
from utils.configManager import load_config, save_config
from PIL import Image, ImageTk

KEY_MAP = {
    "control_l": "<ctrl>",
    "control_r": "<ctrl>",
    "shift_l": "<shift>",
    "shift_r": "<shift>",
    "alt_l": "<alt>",
    "alt_r": "<alt>",
    "super_l": "<cmd>",
    "super_r": "<cmd>",
}

# Icon of the settings window
ICON_RUTE = os.path.join(os.path.dirname(__file__), "../utils/settings.ico")



class SettingsWindow:
    def __init__(self, on_start_callback):
        self.on_start = on_start_callback
        self.captured_keys = set()
        self.is_recording_hotkey = False
        self.root = tk.Tk()
        self.root.title("MultiCopy Settings")
        
        self.root.iconbitmap(ICON_RUTE)

        self.root.geometry("420x750")
        self.center_window(420,750)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.force_exit)
        
        self.hotkey_captured = config.show_overlay_hotkey
        
        
        
        

        # ------------------------
        # Title
        # ------------------------
        ttk.Label(
            self.root,
            text="MultiCopy",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=(10,0))

        # ------------------------
        # Hotkey
        # ------------------------
        hotkey_frame = ttk.LabelFrame(self.root, text="Shortcut")
        hotkey_frame.pack(fill="x", padx=20, pady=10)

        self.hotkey_label = tk.Label(
            hotkey_frame,
            text=self.hotkey_captured + "  ✓" if self.hotkey_captured else "(Not set)",
            bg="#f5f5f5",
            fg="#333",
            font=("Segoe UI", 10),
            anchor="w",
            relief="solid",
            bd=1,
            padx=10,
            pady=6
        )
        self.hotkey_label.pack(fill="x", padx=10, pady=6)

        ttk.Button(
            hotkey_frame,
            text="Record hotkey",
            command=self.record_hotkey
        ).pack(pady=5)


        # ------------------------
        # Max items to store
        # ------------------------
        limit_frame = ttk.LabelFrame(self.root, text="Limits")
        limit_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(limit_frame, text="Max clipboard items:").pack(anchor="w", padx=10)

        self.max_items_spin = ttk.Spinbox(
            limit_frame,
            from_=1,
            to=100,
            width=10
        )
        self.max_items_spin.set(state.max_items)
        self.max_items_spin.pack(padx=10, pady=5)
        
         # ------------------------
        # Max items to display
        # ------------------------
        ttk.Label(limit_frame, text="Max clipboard items to display:").pack(anchor="w", padx=10)

        self.max_items_visible_spin = ttk.Spinbox(
            limit_frame,
            from_=1,
            to=100,
            width=10
        )
        self.max_items_visible_spin.set(state.max_items_visible)
        self.max_items_visible_spin.pack(padx=10, pady=5)

        # ------------------------
        # Import / Export
        # ------------------------
        io_frame = ttk.LabelFrame(self.root, text="Data")
        io_frame.pack(fill="x", padx=20, pady=10)

        self.import_btn = ttk.Button(io_frame, text="Import (.txt)  ", command=self.import_txt)
        self.import_btn.pack(side="left", padx=10, pady=5)

        self.export_btn = ttk.Button(io_frame, text="Export (.txt)  ", command=self.export_txt)
        self.export_btn.pack(side="right", padx=10, pady=5)
        
        # ------------------------
        # Clipboard preview
        # ------------------------
        clipboard_frame = ttk.LabelFrame(self.root, text="Current Clipboard")
        clipboard_frame.pack(fill="x", expand=True, padx=20, pady=(10,0))

        self.clipboard_list = tk.Listbox(
            clipboard_frame,
            height=5
        )
        self.clipboard_list.pack(fill="x", expand=True, padx=10, pady=5)
        
        self.clipboard_list.bind("<Double-Button-1>", self.edit_clipboard_item)

        self.refresh_clipboard_view()
    
        # ------------------------
        # Start
        # ------------------------
        ttk.Button(
            self.root,
            text="Start",
            command=self.start
        ).pack(pady=15)
    
    # ------------------------
    # Hotkey capture
    # ------------------------
    def record_hotkey(self):
        self.captured_keys.clear()
        self.is_recording_hotkey = True
        self.root.focus_force()
        self.hotkey_label.config(text="Press keys...")
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)

    def _on_key_press(self, event):
        if not self.is_recording_hotkey:
            return

        key = event.keysym.lower()
        key = KEY_MAP.get(key, key)

        if key not in self.captured_keys:
            self.captured_keys.add(key)
            self.hotkey_label.config(
                text="+".join(sorted(self.captured_keys))
            )

    def _on_key_release(self, event):
        if not self.is_recording_hotkey:
            return

        if len(self.captured_keys) >= 2:
            combo = "+".join(sorted(self.captured_keys))
            self.hotkey_captured = combo

            self.hotkey_label.config(text=f"{combo}  ✓")

            self.is_recording_hotkey = False
            self.root.unbind("<KeyPress>")
            self.root.unbind("<KeyRelease>")



    # ------------------------
    # Import / Export
    # ------------------------
    def import_txt(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                ClipboardManager.add_text(line.strip())

        self._mark_button_done(self.import_btn, "Import (.txt)")
        self.refresh_clipboard_view()
        save_config(state, config)

    def export_txt(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            for item in ClipboardManager.get_all():
                f.write(item + "\n")

        self._mark_button_done(self.export_btn, "Export (.txt)")
    
    def _mark_button_done(self, button, text):
            button.config(text=f"{text} ✓")
            
    def _reset_button_text(self, button, text):
        button.config(text=text)
        
    # ------------------------
    # Clipboard view
    # ------------------------
    
    def refresh_clipboard_view(self):
        self.clipboard_list.delete(0, tk.END)
        for item in ClipboardManager.get_all():
            self.clipboard_list.insert(tk.END, item)
    
    def edit_clipboard_item(self, event):
        selection = self.clipboard_list.curselection()
        if not selection:
            return

        index = selection[0]
        original = ClipboardManager.get_all()[index]

        editor = tk.Toplevel(self.root)
        editor.title("Edit clipboard item")
        self.center_item_window(editor, 400, 100)
        editor.resizable(False, False)
        editor.transient(self.root)
        editor.grab_set()

        text = tk.Text(editor, wrap="word", height=1)
        text.pack(fill="x", expand=True, padx=10, pady=10)
        text.insert("1.0", original)

        def save():
            new_text = text.get("1.0", "end").strip()
            if new_text:
                state.clipboard_items[index] = new_text
                self.refresh_clipboard_view()
            save_config(state, config)
            editor.destroy()

        ttk.Button(editor, text="Save", command=save).pack(pady=5)


    # ------------------------
    # Start
    # ------------------------
    def start(self):
        config.show_overlay_hotkey = self.hotkey_captured
        state.max_items = int(self.max_items_spin.get())
        state.max_items_visible = int(self.max_items_visible_spin.get())
        self._reset_button_text(self.import_btn, "Import (.txt)  ")
        self._reset_button_text(self.export_btn, "Export (.txt)  ")
        save_config(state, config)
        self.root.destroy()
        self.on_start()

    def run(self):
        self.root.mainloop()

    def center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def center_item_window(self, window, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def force_exit(self):
        try:
            import sys
            sys.exit(0)
        except Exception:
            pass
