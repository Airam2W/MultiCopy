# Configuration management for MultiCopy application. Handles loading and saving user settings, including hotkeys and clipboard items. Ensures that user-specific configurations are stored in a writable location, while providing a default configuration for first-time users.

import json
import os
import sys

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def get_user_config_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.expanduser("~\\AppData\\Local\\MultiCopy")
        os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, "config.json")
    else:
        return resource_path("utils/config.json")

CONFIG_FILE = get_user_config_path()

def save_config(state, config):
    data = {
        "shortcut": config.show_overlay_hotkey,
        "max_items": state.max_items,
        "max_items_visible": state.max_items_visible,
        "clipboard_items": state.clipboard_items,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_config(state, config):
    if not os.path.exists(CONFIG_FILE):
        default_path = resource_path("utils/config.json")
        try:
            with open(default_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Failed to copy default config:", e)
        return

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        config.show_overlay_hotkey = data.get("shortcut", config.show_overlay_hotkey)
        state.max_items = data.get("max_items", state.max_items)
        state.max_items_visible = data.get("max_items_visible", state.max_items_visible)

        state.clipboard_items.clear()
        state.clipboard_items.extend(data.get("clipboard_items", []))

    except Exception as e:
        print("Failed to load config:", e)