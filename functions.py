import customtkinter
import json
import os
import re
import requests
import shutil
from PIL import Image
from io import BytesIO


class AppConfig:
    version = " v1.0.5 (20250407)"
    logo_path = "assets/logo.png"
    channel_config_path = "/" + "_config_channel.json"
    date_format_display = "%d.%m.%Y"
    date_time_format = "%d.%m.%Y %H:%M:%S"
    date_format_math = "%Y-%m-%d"
    # Set window size
    win_width = 1280
    win_height = 790

    REQUIRED_APP_CONFIG = {
        "output_directory": "",
        "youtube_url": "https://www.youtube.com/",
        "youtube_watch_url": "https://www.youtube.com/watch?v=",
        "web_client": ""
    }

    REQUIRED_VIDEO_CHANNEL_CONFIG = {
        "c_max_resolution": "",
        "c_min_duration_in_minutes": "",
        "c_max_duration_in_minutes": "",
        "c_minimum_year": "",
        "c_maximum_year": "",
        "c_only_restricted": "",
        "c_skip_restricted": "",
        "c_minimum_views": "",
        "c_year_subfolders": "",
        "c_exclude_video_ids": "",
        "c_include_video_ids": "",
        "c_filter_words": ""
    }


class COLORS:
    white       = "#ffffff"
    black       = "#000000"
    dark        = "#111111"
    gray        = "#777777"
    blue        = "#7777ff"
    cyan        = "#66f2ff"
    red         = "#ff6666"
    dark_red    = "#d52e2e"
    green       = "#77ff77"
    dark_green  = "#30af30"
    orange      = "#fdbb6e"
    pink        = "#ff83a6"
    yellow      = "#fffb8c"
    violet      = "#c7a8ff"
    log_bg      = "#191919"
    separator   = "#414141"
    frame_bg    = "#131313"


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Bind events to show/hide tooltip
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Create and show the tooltip window."""
        if self.tooltip_window or not self.text:
            return

        x, y, _, height = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20  # Adjust position
        y += self.widget.winfo_rooty() + height + 10

        self.tooltip_window = customtkinter.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Remove window border
        self.tooltip_window.geometry(f"+{x}+{y}")

        label = customtkinter.CTkLabel(self.tooltip_window, text=self.text, fg_color="gray25", text_color="white", padx=10,
                             pady=5)
        label.pack()

    def hide_tooltip(self, event=None):
        """Destroy the tooltip window."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class CcConfig:
    def cc_load_config(file_path: str):
        """Loads the JSON config file or creates an empty dictionary if the file doesn't exist."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)  # Load existing config
                except json.JSONDecodeError:
                    print("❌ Error: Invalid JSON format. Resetting to default config.")
                    return {}  # Return an empty config if JSON is corrupted
        return {}  # Return an empty config if file doesn't exist


    def cc_save_config(cc_file_path: str, cc_config: str) -> None:
        """Saves the updated config dictionary back to the JSON file."""
        with open(cc_file_path, "w", encoding="utf-8") as cc_file:
            json.dump(cc_config, cc_file, indent=4, ensure_ascii=False)


    def cc_check_and_update_json_config(cc_file_path: str, cc_required_config: dict) -> None:
        """Ensures all required keys exist in the config file, adding missing ones."""
        cc_config = CcConfig.cc_load_config(cc_file_path)  # Load existing or empty config

        # Check for missing keys and add them
        missing_keys = []
        for key, default_value in cc_required_config.items():
            if key not in cc_config:
                cc_config[key] = default_value
                missing_keys.append(key)

        if missing_keys:
            CcConfig.cc_save_config(cc_file_path, cc_config)  # Save only if changes were made


class JSONConfig:
    def create_json_config(file_path, config_values=None):
        """
        Creates a JSON config file at the specified path with default or custom values.

        Args:
            file_path (str): The path where the JSON file will be created.
            config_values (dict, optional): A dictionary containing key-value pairs for the config.
                                            If None, default values are used.

        Returns:
            bool: True if the file was created successfully, False otherwise.
        """

        # Merge default config with user-defined values
        if config_values:
            AppConfig.REQUIRED_VIDEO_CHANNEL_CONFIG.update(config_values)  # Override defaults if provided

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write JSON file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(AppConfig.REQUIRED_VIDEO_CHANNEL_CONFIG, f, indent=4)

            # print(f"✅ JSON config file created at: {file_path}")
            return True

        except Exception as json_e:
            print(f"❌ Error creating JSON file: {json_e}")
            return False


    def update_json_config(file_path: str, parameter: str, new_value) -> bool:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return False

        try:
            # Load existing JSON file
            with open(file_path, "r", encoding="utf-8") as f:
                json_config = json.load(f)

            # Handle nested keys (e.g., "settings.database.host")
            keys = parameter.split(".")
            temp = json_config
            for key in keys[:-1]:  # Traverse to the second last key
                temp = temp.setdefault(key, {})  # Create dict if key doesn't exist

            # Update the final key
            temp[keys[-1]] = new_value

            # Save back to JSON file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(json_config, f, indent=4)

            # print(f"✅ Updated '{parameter}' to '{new_value}' in '{file_path}'")
            return True

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'")
        except Exception as ujson_e:
            print(f"Error: {ujson_e}")

        return False


def load_config(c_file: str):
    with open(c_file, "r") as file:
        l_config = json.load(file)
    return l_config


def find_file_by_string(directory: str, search_string: str, resolution: str, mp3: bool) -> str | None:
    if resolution=="max":
        resolution = ""
    if mp3:
        resolution = "mp3"

    if not os.path.exists(directory):
        return None

    for root, _, files in os.walk(directory):  # os.walk() traverses all subdirectories
        for filename in files:
            if search_string in filename and resolution in filename:
                return os.path.join(root, filename)  # Return full file path of the first match

    return None  # Return None if no file is found


def count_files(directory, ext):
    count = 0
    for root, dirs, files in os.walk(directory):
        count += sum(1 for file in files if file.endswith(ext))
    return count


def get_free_space(path: str) -> str:
    total, used, free = shutil.disk_usage(path)  # Get disk space (in bytes)
    # Convert bytes to GB or MB for readability
    if free >= 1_000_000_000:  # If space is at least 1GB
        formatted_space = f"{free / 1_073_741_824:.1f} GB"
    else:
        formatted_space = f"{free / 1_048_576:.0f} MB"  # Otherwise, use MB
    return formatted_space


def format_time(seconds: int) -> str:
    f_min, f_sec = divmod(seconds, 60)
    return f"{f_min}m{f_sec}s"


def clean_string_regex(text: str) -> str:
    new_text = text.replace(":", "")
    pattern = r"[^a-zA-Z0-9 ]"
    return re.sub(pattern, "", new_text)


def string_to_list(input_string: str) -> list[str]:
    return [item.strip() for item in input_string.split(",")]


def load_image_from_url(url, size=(100, 100)):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))  # Convert bytes to an image
    return customtkinter.CTkImage(light_image=image, size=size)


def destroy_elements(d_elements_to_destroy):
    """Remove all created widgets"""
    for element in d_elements_to_destroy:
        element.destroy()  # Remove widget from the UI
    d_elements_to_destroy.clear()


def grid_remove_elements(d_elements_to_destroy):
    """Remove all created widgets"""
    for element in d_elements_to_destroy:
        element.grid_remove()  # Remove widget from the UI
    d_elements_to_destroy.clear()


